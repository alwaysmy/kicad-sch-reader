"""Connectivity extraction and project-wide netlist construction.

The approach mirrors the "connectivity domain" idea used by the reviewed
LCEDA reader: wires are unioned through their exact endpoints and junction
flags, labels/power symbols name whole domains, and pins are attached by
absolute position.  Hierarchical sheets are then joined through sheet pins,
and global labels/power symbols are merged project-wide by name.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple

from .model import (
    Label,
    Net,
    PinInstance,
    PinNet,
    Project,
    SheetData,
    SheetPin,
    SymbolInstance,
)

Point = Tuple[int, int]  # quantized point key
EPS_MM = 0.001  # position match tolerance (1 um)


def _path_depth(path: str) -> int:
    """Hierarchy depth of a sheet path: '/' -> 0, '/uuid' -> 1, '/a/b' -> 2."""
    return sum(1 for seg in str(path).split("/") if seg)


@dataclass
class _LocalNet:
    sheet_path: str
    points: Set[Point] = field(default_factory=set)
    pins: List[PinNet] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    global_names: List[str] = field(default_factory=list)
    power_names: List[str] = field(default_factory=list)
    hierarchical_names: List[str] = field(default_factory=list)


class _DSU:
    def __init__(self) -> None:
        self.parent: Dict[Point, Point] = {}

    def add(self, p: Point) -> Point:
        if p not in self.parent:
            self.parent[p] = p
        return self.find(p)

    def find(self, p: Point) -> Point:
        parent = self.parent
        if p not in parent:
            parent[p] = p
        root = p
        while parent[root] != root:
            root = parent[root]
        while parent[p] != root:
            nxt = parent[p]
            parent[p] = root
            p = nxt
        return root

    def union(self, a: Point, b: Point) -> Point:
        ra, rb = self.add(a), self.add(b)
        if ra != rb:
            self.parent[rb] = ra
        return self.find(ra)


def qpoint(x: float, y: float) -> Point:
    return (int(round(x / EPS_MM)), int(round(y / EPS_MM)))


def _distance_to_segment(p: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> float:
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    cx, cy = ax + t * dx, ay + t * dy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5


def build_sheet_graph(sheet: SheetData):
    """Build a per-sheet union-find over physical connection points.

    Returns ``(dsu, pin_net_keys, nc_keys, label_keys)`` where each map key is
    the quantized point and values are the model objects attached there.
    """
    dsu = _DSU()
    positions: Dict[Point, Tuple[float, float]] = {}
    pin_keys: Dict[Point, List[PinInstance]] = {}
    nc_keys: Set[Point] = set()
    label_keys: Dict[Point, List[Label]] = {}
    geometry_keys: Set[Point] = set()
    wire_segments: List[Tuple[Tuple[float, float], Tuple[float, float]]] = []

    def ensure(p: Point, pos: Tuple[float, float]) -> Point:
        dsu.add(p)
        positions.setdefault(p, pos)
        return p

    for w in sheet.wires:
        ka, kb = qpoint(*w.p1), qpoint(*w.p2)
        ensure(ka, w.p1)
        ensure(kb, w.p2)
        dsu.union(ka, kb)
        geometry_keys.add(ka)
        geometry_keys.add(kb)
        wire_segments.append((w.p1, w.p2))

    for j in sheet.junctions:
        k = qpoint(*j.pos)
        ensure(k, j.pos)
        geometry_keys.add(k)

    for nc in sheet.no_connects:
        k = qpoint(*nc.pos)
        ensure(k, nc.pos)
        geometry_keys.add(k)
        nc_keys.add(k)

    for label in sheet.labels:
        k = qpoint(*label.pos)
        if k not in dsu.parent:
            # A label may legally sit in the middle of a wire; snap it to the
            # closest segment instead of declaring it dangling immediately.
            best = None
            best_d = 0.01
            for a, b in wire_segments:
                d = _distance_to_segment(label.pos, a, b)
                if d < best_d:
                    best_d = d
                    best = (a, b)
            if best is not None:
                k = qpoint(*label.pos)
                ensure(k, label.pos)
                dsu.union(k, qpoint(*best[0]))
                dsu.union(k, qpoint(*best[1]))
            else:
                ensure(k, label.pos)
        geometry_keys.add(k)
        label_keys.setdefault(k, []).append(label)

    # Register every pin position as a DSU node.  Pins are only *reported* as
    # connected in build_local_nets when the point also carries real geometry
    # (wire/junction/label/no-connect) or is shared by another pin (direct
    # pin-to-pin contact, e.g. a capacitor pin touching a power symbol).
    for sym in sheet.symbols:
        for pin in sym.pins:
            k = qpoint(*pin.pos)
            ensure(k, pin.pos)
            pin_keys.setdefault(k, []).append((pin, sym))

    return dsu, positions, pin_keys, nc_keys, label_keys, geometry_keys


def _attach_pin(net: _LocalNet, pin: PinInstance, sym: SymbolInstance) -> None:
    net.pins.append(
        PinNet(
            ref=sym.ref,
            pin_number=pin.number,
            pin_name=pin.name,
            pin_type=pin.electrical_type,
            sheet_path=sym.sheet_path,
            lib_id=sym.lib_id,
            value=sym.value,
            footprint=sym.footprint,
        )
    )


def build_local_nets(project: Project):
    """Return per-sheet local nets plus the maps needed for hierarchy joins."""
    local_by_sheet: Dict[str, List[_LocalNet]] = {}
    point_net: Dict[str, Dict[Point, _LocalNet]] = {}
    # (ref, pin, quantised point) -> point.  The position is part of the key:
    # unannotated power symbols all share reference "#PWR?" and pin "1", so a
    # bare (ref, pin) key would collapse them onto whichever instance was
    # stored last.
    pin_net_key: Dict[str, Dict[Tuple[str, str, Point], Optional[Point]]] = {}

    for path in project.sheet_order:
        sheet = project.sheets[path]
        dsu, positions, pin_keys, nc_keys, label_keys, geometry_keys = build_sheet_graph(sheet)

        net_of_point: Dict[Point, _LocalNet] = {}
        root_to_net: Dict[Point, _LocalNet] = {}
        for k in dsu.parent:
            root = dsu.find(k)
            if root not in root_to_net:
                root_to_net[root] = _LocalNet(sheet_path=path)
            root_to_net[root].points.add(k)
        for k in positions:
            net_of_point[k] = root_to_net[dsu.find(k)]

        # Attach pins and record which physical point every (ref, pin) belongs to.
        pin_net_key[path] = {}
        for sym in sheet.symbols:
            for pin in sym.pins:
                k = qpoint(*pin.pos)
                key = (sym.ref, pin.number, k)
                if k in nc_keys:
                    pin.no_connect = True
                    pin_net_key[path][key] = None
                    continue
                if pin.electrical_type.lower() in ("no_connect", "not_connected"):
                    # Only `no_connect`/`not_connected` pins are intentionally
                    # unconnected.  `free` pins are ERC-neutral but still
                    # electrically connectable (TVS/ESD devices use them).
                    pin.no_connect = True
                    pin_net_key[path][key] = None
                    continue
                shared_pin_point = len(pin_keys.get(k, [])) >= 2
                if k in pin_keys and (k in geometry_keys or shared_pin_point):
                    net = net_of_point.get(k)
                    if net is not None:
                        _attach_pin(net, pin, sym)
                        pin_net_key[path][key] = k
                        continue
                pin_net_key[path][key] = None

        # Attach labels to their physical net.
        for k, labels in label_keys.items():
            net = net_of_point.get(k)
            if net is None:
                continue
            for label in labels:
                net.labels.append(label.name)
                if label.kind == "global_label":
                    net.global_names.append(label.name)
                elif label.kind == "hierarchical_label":
                    net.hierarchical_names.append(label.name)

        # Hidden power-input pins (legacy libraries, "(hide yes)"): KiCad
        # connects them to the global net named after the *pin* even without
        # any geometry (verified against kicad-cli on the video demo).  Give
        # each such pin a name-only net; build_netlist() merges same power
        # names project-wide, so a matching power symbol joins the geometry.
        hidden_by_name: Dict[str, _LocalNet] = {}
        for sym in sheet.symbols:
            for pin in sym.pins:
                if not pin.hidden or (pin.electrical_type or "").lower() != "power_in":
                    continue
                if not pin.name or not pin.name.strip():
                    continue
                key = (sym.ref, pin.number, qpoint(*pin.pos))
                if pin.no_connect or pin_net_key[path].get(key) is not None:
                    continue  # explicitly no-connect, or connected geometrically
                nm = pin.name.strip()
                net = hidden_by_name.get(nm)
                if net is None:
                    net = _LocalNet(sheet_path=path)
                    net.power_names.append(nm)
                    hidden_by_name[nm] = net
                _attach_pin(net, pin, sym)
                pin_net_key[path][key] = qpoint(*pin.pos)

        # Power symbols behave like global labels named by their Value.
        # Exception: PWR_FLAG only marks "this net is power-driven" for ERC;
        # treating its value as a net name would unite every flagged rail
        # (verified against kicad-cli on the complex_hierarchy demo).
        for sym in sheet.symbols:
            if sym.is_power_symbol and sym.value and sym.value != "PWR_FLAG":
                for pin in sym.pins:
                    key = (sym.ref, pin.number, qpoint(*pin.pos))
                    k = pin_net_key[path].get(key)
                    if k is not None:
                        net = net_of_point.get(k)
                        if net is not None and sym.value:
                            net.power_names.append(sym.value)

        # Keep every domain at this stage.  Pure wire domains matter for
        # hierarchical sheet-pin joins (two sheet pins connected by a wire with
        # no component on it); final materialisation drops groups that never
        # acquired a pin or a name.
        nets = list(root_to_net.values()) + list(hidden_by_name.values())

        # KiCad connects same-name ordinary/hierarchical labels inside one
        # sheet; merge those domains before hierarchy handling.
        parent = list(range(len(nets)))

        def find(i: int) -> int:
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        groups: Dict[str, List[int]] = {}
        for i, net in enumerate(nets):
            for name in set(net.labels + net.hierarchical_names):
                if name:
                    groups.setdefault(name, []).append(i)
        for members in groups.values():
            for m in members[1:]:
                union(members[0], m)

        local_by_sheet[path] = nets
        point_net[path] = {
            k: nets[find(i)]
            for i, net in enumerate(nets)
            for k in net.points
        }

    return local_by_sheet, point_net, pin_net_key


class _NetUnion:
    def __init__(self, nets: List[_LocalNet]) -> None:
        self.parent = list(range(len(nets)))
        self.nets = nets

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def union(self, a: int, b: int) -> int:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra
        return ra


def build_netlist(project: Project) -> List[Net]:
    """Build the project-wide netlist with hierarchy and global-label merging."""
    local_by_sheet, point_net, _ = build_local_nets(project)

    flat: List[_LocalNet] = []
    index: Dict[Tuple[str, int], int] = {}
    for path, nets in local_by_sheet.items():
        for i, net in enumerate(nets):
            index[(path, i)] = len(flat)
            flat.append(net)

    union = _NetUnion(flat)

    def find_net_for(path: str, net: _LocalNet) -> Optional[int]:
        for i, n in enumerate(local_by_sheet.get(path, [])):
            if n is net:
                return union.find(index[(path, i)])
        return None

    # 0) Same-name ordinary/hierarchical labels inside one sheet are the
    #    same local net (this mirrors Eeschema's local-label semantics).
    local_label_groups: Dict[Tuple[str, str], List[int]] = {}
    for path, nets in local_by_sheet.items():
        for i, net in enumerate(nets):
            flat_i = index[(path, i)]
            for name in set(net.labels + net.hierarchical_names):
                if name:
                    local_label_groups.setdefault((path, name), []).append(flat_i)
    for members in local_label_groups.values():
        for m in members[1:]:
            union.union(members[0], m)

    # 1) Join hierarchical labels to the parent sheet pins that carry the
    #    same name at the pin's physical position.
    for parent_path in project.sheet_order:
        parent = project.sheets.get(parent_path)
        if parent is None:
            continue
        parent_point_net = point_net.get(parent_path, {})
        for ref in parent.sheets:
            child_path = ref.first_path
            child = project.sheets.get(child_path)
            if child is None:
                continue
            child_label_points: Dict[str, List[Point]] = {}
            for label in child.labels:
                if label.kind == "hierarchical_label":
                    child_label_points.setdefault(label.name, []).append(qpoint(*label.pos))
            child_point_net = point_net.get(child_path, {})
            for pin in ref.pins:
                parent_net = parent_point_net.get(qpoint(*pin.pos))
                child_nets = []
                for k in child_label_points.get(pin.name, []):
                    cn = child_point_net.get(k)
                    if cn is not None:
                        child_nets.append(cn)
                if parent_net is None or not child_nets:
                    continue
                pi = find_net_for(parent_path, parent_net)
                for cn in child_nets:
                    ci = find_net_for(child_path, cn)
                    if pi is not None and ci is not None:
                        union.union(pi, ci)

    # 2) Global labels and power symbols are global by name project-wide.
    global_map: Dict[str, List[int]] = {}
    for path, nets in local_by_sheet.items():
        for i, net in enumerate(nets):
            root_i = union.find(index[(path, i)])
            for name in set(net.global_names + net.power_names):
                global_map.setdefault(name, []).append(root_i)

    for name, members in global_map.items():
        first = members[0]
        for m in members[1:]:
            union.union(first, m)

    # 3) Materialise the merged nets.
    groups: Dict[int, Net] = {}
    for path, nets in local_by_sheet.items():
        for i, local in enumerate(nets):
            root_i = union.find(index[(path, i)])
            group = groups.get(root_i)
            if group is None:
                group = Net(name="")
                group.hier_sources = {}  # name -> set(sheet_path)
                group.label_entries = []  # (sheet depth, label name)
                groups[root_i] = group
            group.pins.extend(local.pins)
            group.labels.extend(local.labels)
            group.global_names.extend(local.global_names)
            group.power_names.extend(local.power_names)
            group.hierarchical_names.extend(local.hierarchical_names)
            for hname in local.hierarchical_names:
                group.hier_sources.setdefault(hname, set()).add(local.sheet_path)
            # Record where each ordinary label lives: the official netlist
            # exporter names merged nets after the *shallower* candidate.
            depth = _path_depth(local.sheet_path)
            for lname in set(local.labels):
                if lname:
                    group.label_entries.append((depth, lname))
            group.point_count += len(local.points)

    named_or_pinned_groups = [
        g for g in groups.values()
        if g.pins or g.labels or g.global_names or g.power_names or g.hierarchical_names
    ]

    # KiCad-compatible hierarchical naming: /<Sheetname>/<label> for child
    # sheets, /<label> for the root sheet.
    sheet_names: Dict[str, str] = {"/": ""}
    for path in project.sheet_order:
        if path == "/":
            continue
        for parent in project.sheets.values():
            for ref in parent.sheets:
                if ref.first_path == path:
                    sheet_names[path] = ref.name
                    break

    nets: List[Net] = []
    for order, group in enumerate(sorted(named_or_pinned_groups, key=lambda n: sorted(n.pins[0].ref if n.pins else ""))):
        global_set = sorted({n for n in group.global_names + group.power_names if n})
        group.global_names = sorted({n for n in group.global_names if n})
        group.power_names = sorted({n for n in group.power_names if n})
        group.hierarchical_names = sorted({n for n in group.hierarchical_names if n})
        group.sheet_paths = sorted({p.sheet_path for p in group.pins})
        if len(global_set) > 1:
            group.has_conflict = True
            group.conflict_names = global_set
        # Deterministic naming priority: power symbol value, global label,
        # hierarchical label, ordinary label, generated name.  Named nets use
        # KiCad's convention: power/global names are bare, ordinary local labels
        # get a leading "/", and hierarchical labels become /<Sheet>/<Label>.
        if global_set:
            group.name = global_set[0]
        else:
            # Depth-first naming mirrors the official exporter: a plain label
            # on a shallower sheet wins over a deeper hierarchical label
            # (e.g. parent "D9" over child HL "DOUT9" on the same net); ties
            # keep the previous hierarchical-first behaviour.
            hier_best = None
            local_best = min(group.label_entries) if group.label_entries else None
            if group.hierarchical_names:
                hname = sorted(group.hierarchical_names)[0]
                paths = sorted(group.hier_sources.get(hname, {"/"}))
                hd = min(_path_depth(x) for x in paths)
                hier_best = (hd, hname)
            if local_best is not None and (hier_best is None or local_best[0] < hier_best[0]):
                group.name = local_best[1] if local_best[1].startswith("/") else f"/{local_best[1]}"
            elif hier_best is not None:
                hname = hier_best[1]
                paths = sorted(group.hier_sources.get(hname, {"/"}))
                path = paths[0] if paths else "/"
                sheet_name = sheet_names.get(path, "")
                group.name = f"/{sheet_name}/{hname}" if sheet_name else f"/{hname}"
            else:
                group.name = f"N${order + 1}"
        nets.append(group)

    nets.sort(key=lambda n: (n.name, tuple(p.ref for p in n.pins[:2])))
    return nets


def find_pin_net(netlist: Iterable[Net], ref: str, pin_number: str) -> Optional[Net]:
    for net in netlist:
        for p in net.pins:
            if p.ref == ref and p.pin_number == pin_number:
                return net
    return None


def nets_for_ref(netlist: Iterable[Net], ref: str) -> List[Net]:
    return [net for net in netlist if any(p.ref == ref for p in net.pins)]


def net_members_by_sheet(net: Net) -> Dict[str, List[PinNet]]:
    out: Dict[str, List[PinNet]] = {}
    for p in net.pins:
        out.setdefault(p.sheet_path, []).append(p)
    return out
