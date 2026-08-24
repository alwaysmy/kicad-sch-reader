"""Parser for KiCad ``.kicad_sch`` files (KiCad 6..10 s-expression format).

The parser is deliberately tolerant: unknown node kinds are counted and
ignored, and malformed optional fields degrade to defaults instead of
aborting a whole-project review.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

from . import sexpr
from .model import (
    Junction,
    Label,
    LibPin,
    LibSymbol,
    NoConnect,
    PinInstance,
    Project,
    SchText,
    SheetData,
    SheetPin,
    SheetRef,
    SymbolInstance,
    Wire,
)

_SUB_UNIT_RE = re.compile(r"_(\d+)_(\d+)$")


def _text(value) -> str:
    return sexpr.atom_text(value)


def _flag(node, name: str, default: bool) -> bool:
    item = sexpr.first(node, name)
    if item is None or len(item) < 2:
        return default
    return _text(item[1]).lower() == "yes"


def _parse_lib_pin(node) -> Optional[LibPin]:
    """Parse both KiCad 10 (``pin passive line (number "1")``) and the
    older KiCad 6..9 layout (``pin "1" (type passive) (name ...)``)."""
    if not sexpr.is_node(node, "pin"):
        return None
    number_node = sexpr.first(node, "number")
    name_node = sexpr.first(node, "name")
    type_node = sexpr.first(node, "type")
    at_node = sexpr.first(node, "at")

    first_atom = _text(node[1]) if len(node) > 1 else ""
    # KiCad 10 puts the electrical type in the second atom ("passive", "power_in"...)
    # Older files put the pin number there.
    if first_atom and not first_atom[0].isdigit() and first_atom[0] not in "+-~":
        number = _text(number_node[1]) if number_node is not None and len(number_node) > 1 else ""
        electrical_type = first_atom
    else:
        number = first_atom
        electrical_type = (
            _text(type_node[1]) if type_node is not None and len(type_node) > 1 else "unknown"
        )
    name = _text(name_node[1]) if name_node is not None and len(name_node) > 1 else ""
    pos = sexpr.xy(at_node) if at_node is not None else (0.0, 0.0, 0.0)
    # Empirical KiCad 10 fact (validated against kicad-cli netlist on the
    # example projects and a minimal rotation test bench): the pin `at` y
    # coordinate in the symbol definition has the opposite sign of the
    # physical connection offset used by Eeschema connectivity.
    return LibPin(number=number, name=name, electrical_type=electrical_type, pos=(pos[0], -pos[1]))


def parse_lib_symbols(root) -> Dict[str, LibSymbol]:
    out: Dict[str, LibSymbol] = {}
    libs = sexpr.first(root, "lib_symbols")
    if libs is None:
        return out
    for sym in sexpr.children(libs, "symbol"):
        if len(sym) < 2:
            continue
        lib_id = _text(sym[1])
        symbol = LibSymbol(lib_id=lib_id)
        for sub in sexpr.children(sym, "symbol"):
            if len(sub) < 2:
                continue
            match = _SUB_UNIT_RE.search(_text(sub[1]))
            key = f"{match.group(1)}_{match.group(2)}" if match else "0_0"
            pins = [p for p in (_parse_lib_pin(n) for n in sexpr.children(sub, "pin")) if p]
            if pins:
                symbol.units[key] = pins
        out[lib_id] = symbol
    return out


def parse_lib_instances(root) -> Dict[str, Dict[str, dict]]:
    """Parse per-sheet-instance overrides inside ``lib_symbols``.

    KiCad stores ``(instances (project ... (path /root/sheet_uuid
    (reference "C301") (unit 1))))`` in a reused child sheet's library
    symbols.  Without applying these overrides both instances keep the base
    reference (e.g. C101) and the second instance's unique designators are
    lost entirely.

    Return ``{lib_id: {sheet_path: {"reference": ..., "unit": ...}}}`` where
    sheet_path is the child instance path without the project root prefix.
    """
    out: Dict[str, Dict[str, dict]] = {}
    libs = sexpr.first(root, "lib_symbols")
    if libs is None:
        return out
    for sym in sexpr.children(libs, "symbol"):
        if len(sym) < 2:
            continue
        lib_id = _text(sym[1])
        instances = next(sexpr.find_all(sym, "instances"), None)
        if instances is None:
            continue
        per_path: Dict[str, dict] = {}
        for proj in sexpr.children(instances, "project"):
            for item in sexpr.children(proj, "path"):
                if len(item) < 2:
                    continue
                raw_path = _text(item[1])
                # KiCad path: /root_sheet_uuid/child_sheet_uuid (older files may
                # include a project name).  Our internal sheet_path is /uuid.
                leaf = raw_path.rsplit("/", 1)[-1]
                override = {}
                ref_node = sexpr.first(item, "reference")
                if ref_node is not None and len(ref_node) > 1:
                    override["reference"] = _text(ref_node[1])
                unit_node = sexpr.first(item, "unit")
                if unit_node is not None and len(unit_node) > 1:
                    override["unit"] = _text(unit_node[1])
                if leaf:
                    per_path[leaf] = override
        if per_path:
            out[lib_id] = per_path
    return out


def _mirror_of(node) -> str:
    item = sexpr.first(node, "mirror")
    if item is None:
        return ""
    return _text(item[1]) if len(item) > 1 else ""


def transform_point(p: tuple[float, float], rotation: float, mirror: str) -> tuple[float, float]:
    """KiCad instance transform: optional mirror, then clockwise rotation.

    Orientation and mirror order were verified against ``kicad-cli`` netlist
    output with a minimal symbol-rotation test bench: mirror is applied in the
    un-rotated frame and rotation stays clockwise (90 -> (y, -x)).
    """
    x, y = p
    rot = int(rotation) % 360
    if rot == 90:
        x, y = y, -x
    elif rot == 180:
        x, y = -x, -y
    elif rot == 270:
        x, y = -y, x
    # KiCad applies the mirror after the rotation, and the flag names the
    # mirroring axis: (mirror x) flips the Y coordinate (horizontal axis),
    # (mirror y) flips the X coordinate (vertical axis).
    if mirror == "x":
        y = -y
    elif mirror == "y":
        x = -x
    return (x, y)


def parse_symbol_instance(
    node, lib_symbols: Dict[str, LibSymbol], sheet_path: str = "/",
    instance_overrides: Optional[Dict[str, Dict[str, dict]]] = None,
) -> Optional[SymbolInstance]:
    if not sexpr.is_node(node, "symbol"):
        return None
    lib_id_node = sexpr.first(node, "lib_id")
    lib_id = _text(lib_id_node[1]) if lib_id_node is not None and len(lib_id_node) > 1 else ""
    at_node = sexpr.first(node, "at")
    if at_node is None:
        return None
    x, y, rotation = sexpr.xy(at_node)
    unit_node = sexpr.first(node, "unit")
    body_node = sexpr.first(node, "body_style")
    unit = _text(unit_node[1]) if unit_node is not None and len(unit_node) > 1 else "1"
    body_style = _text(body_node[1]) if body_node is not None and len(body_node) > 1 else "1"
    mirror = _mirror_of(node)

    props = {
        _text(p[1]): _text(p[2])
        for p in sexpr.children(node, "property")
        if len(p) > 2
    }
    # Per-instance overrides (KiCad sheet reuse): placed symbols in a reused
    # child sheet carry ``(instances (project ... (path /root/sheet_uuid
    # (reference "R311") (unit 1))))``.  Apply the entry whose path leaf
    # matches this sheet instance.
    instances_node = next(sexpr.find_all(node, "instances"), None)
    if instances_node is not None:
        leaf = sheet_path.rstrip("/").rsplit("/", 1)[-1] if sheet_path != "/" else ""
        for proj in sexpr.children(instances_node, "project"):
            for p in sexpr.children(proj, "path"):
                if len(p) < 2:
                    continue
                p_leaf = _text(p[1]).rstrip("/").rsplit("/", 1)[-1]
                if not leaf or p_leaf != leaf:
                    continue
                ref_node = sexpr.first(p, "reference")
                if ref_node is not None and len(ref_node) > 1:
                    props["Reference"] = _text(ref_node[1])
                unit_node = sexpr.first(p, "unit")
                if unit_node is not None and len(unit_node) > 1:
                    unit = _text(unit_node[1])
                break
    uuid_node = sexpr.first(node, "uuid")
    symbol = SymbolInstance(
        ref=props.get("Reference", ""),
        value=props.get("Value", ""),
        lib_id=lib_id,
        unit=unit,
        body_style=body_style,
        pos=(x, y),
        rotation=rotation,
        mirror=mirror,
        uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "",
        in_bom=_flag(node, "in_bom", True),
        on_board=_flag(node, "on_board", True),
        dnp=_flag(node, "dnp", False),
        properties=props,
        sheet_path=sheet_path,
    )

    lib = lib_symbols.get(lib_id)
    lib_pins = lib.pins_for(unit, body_style) if lib else []
    pin_positions: Dict[str, tuple[float, float]] = {}
    for lp in lib_pins:
        lx, ly = transform_point(lp.pos, rotation, mirror)
        pin_positions[lp.number] = (x + lx, y + ly)

    seen: set[str] = set()
    for pin_node in sexpr.children(node, "pin"):
        if len(pin_node) < 2:
            continue
        number = _text(pin_node[1])
        if not number or number in seen:
            continue
        lp = next((p for p in lib_pins if p.number == number), None)
        if lib is not None and lib_pins and lp is None:
            # Multi-unit symbols may still carry the other units' pin UUIDs in
            # the file.  Those pins are not electrically active on this unit;
            # keeping them (and defaulting to the origin) would create bogus
            # shared-pin nets.
            continue
        seen.add(number)
        if lib is None or lp is None:
            # Power symbols (and a few legacy symbols) define their connection
            # point at the instance origin.
            pos = (x, y)
            name = ""
            etype = "power_in" if lib_id.startswith("power:") else "unknown"
        else:
            pos = pin_positions.get(number, (x, y))
            name = lp.name
            etype = lp.electrical_type or "unknown"
        uuid_node = sexpr.first(pin_node, "uuid")
        symbol.pins.append(
            PinInstance(
                number=number,
                name=name,
                electrical_type=etype,
                pos=pos,
                uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "",
            )
        )
    return symbol


def parse_sheet_ref(node) -> Optional[SheetRef]:
    if not sexpr.is_node(node, "sheet"):
        return None
    at_node = sexpr.first(node, "at")
    size_node = sexpr.first(node, "size")
    uuid_node = sexpr.first(node, "uuid")
    if at_node is None:
        return None
    x, y, _ = sexpr.xy(at_node)
    sx = sexpr.to_float(size_node[1]) if size_node is not None and len(size_node) > 1 else 0.0
    sy = sexpr.to_float(size_node[2]) if size_node is not None and len(size_node) > 2 else 0.0
    props = {
        _text(p[1]): _text(p[2])
        for p in sexpr.children(node, "property")
        if len(p) > 2
    }
    pins: List[SheetPin] = []
    for p in sexpr.children(node, "pin"):
        if len(p) < 2:
            continue
        pname = _text(p[1])
        direction = _text(p[2]) if len(p) > 2 else ""
        pat = sexpr.first(p, "at")
        px, py, _ = sexpr.xy(pat) if pat is not None else (0.0, 0.0, 0.0)
        pins.append(SheetPin(name=pname, direction=direction, pos=(px, py)))

    raw_paths: List[str] = []
    instances = sexpr.first(node, "instances")
    if instances is not None:
        for proj in sexpr.children(instances, "project"):
            path_node = sexpr.first(proj, "path")
            if path_node is not None and len(path_node) > 1:
                raw_paths.append(_text(path_node[1]))
    uuid = _text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else ""
    # In KiCad 10 root sheets the instances list can contain the *root* path
    # plus a page number instead of the child-instance path.  Keep only paths
    # that really point at this sheet uuid; the project loader synthesizes the
    # rest from the parent path.
    paths = [p for p in raw_paths if uuid and (p == f"/{uuid}" or p.endswith(f"/{uuid}"))]
    return SheetRef(
        name=props.get("Sheetname", ""),
        file=props.get("Sheetfile", ""),
        pos=(x, y),
        size=(sx, sy),
        uuid=uuid,
        pins=pins,
        paths=paths,
    )


def parse_sheet_file(file: Path, sheet_path: str = "/") -> SheetData:
    text = file.read_text(encoding="utf-8", errors="replace")
    nodes = sexpr.parse(text)
    root = nodes[0] if nodes and sexpr.is_node(nodes[0], "kicad_sch") else []

    sheet = SheetData(path=sheet_path, file=file)
    for child in sexpr.children(root):
        sheet.node_counts[child[0]] = sheet.node_counts.get(child[0], 0) + 1

    version = sexpr.first(root, "version")
    generator = sexpr.first(root, "generator")
    generator_version = sexpr.first(root, "generator_version")
    sheet.version = _text(version[1]) if version is not None and len(version) > 1 else ""
    sheet.generator = _text(generator[1]) if generator is not None and len(generator) > 1 else ""
    sheet.generator = f"{sheet.generator} {_text(generator_version[1])}".strip() \
        if generator_version is not None and len(generator_version) > 1 else sheet.generator

    title_block = sexpr.first(root, "title_block")
    if title_block is not None:
        for field_node in sexpr.children(title_block):
            fname = field_node[0]
            if fname == "comment":
                # (comment <n> "<text>")
                if len(field_node) > 2:
                    sheet.title_fields[f"comment{_text(field_node[1])}"] = _text(field_node[2])
            elif len(field_node) > 1:
                sheet.title_fields[fname] = _text(field_node[1])
        sheet.title = sheet.title_fields.get("title", "")

    sheet.lib_symbols = parse_lib_symbols(root)
    instance_overrides = parse_lib_instances(root)

    for child in sexpr.children(root):
        kind = child[0]
        if kind == "symbol":
            symbol = parse_symbol_instance(child, sheet.lib_symbols, sheet_path,
                                           instance_overrides)
            if symbol is not None:
                sheet.symbols.append(symbol)
        elif kind == "wire":
            pts = sexpr.first(child, "pts")
            xys = list(sexpr.children(pts, "xy")) if pts is not None else []
            if len(xys) >= 2:
                uuid_node = sexpr.first(child, "uuid")
                sheet.wires.append(
                    Wire(
                        p1=sexpr.pair_xy(xys[0]),
                        p2=sexpr.pair_xy(xys[1]),
                        uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "",
                    )
                )
        elif kind in ("label", "global_label", "hierarchical_label"):
            if len(child) < 2:
                continue
            at_node = sexpr.first(child, "at")
            x, y, rot = sexpr.xy(at_node) if at_node is not None else (0.0, 0.0, 0.0)
            shape_node = sexpr.first(child, "shape")
            uuid_node = sexpr.first(child, "uuid")
            sheet.labels.append(
                Label(
                    name=_text(child[1]),
                    pos=(x, y),
                    rotation=rot,
                    kind=kind,
                    shape=_text(shape_node[1]) if shape_node is not None and len(shape_node) > 1 else "",
                    uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "",
                )
            )
        elif kind == "junction":
            at_node = sexpr.first(child, "at")
            if at_node is not None:
                x, y, _ = sexpr.xy(at_node)
                uuid_node = sexpr.first(child, "uuid")
                sheet.junctions.append(
                    Junction(pos=(x, y), uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "")
                )
        elif kind == "no_connect":
            at_node = sexpr.first(child, "at")
            if at_node is not None:
                x, y, _ = sexpr.xy(at_node)
                uuid_node = sexpr.first(child, "uuid")
                sheet.no_connects.append(
                    NoConnect(pos=(x, y), uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "")
                )
        elif kind == "sheet":
            ref = parse_sheet_ref(child)
            if ref is not None:
                sheet.sheets.append(ref)
        elif kind in ("text", "textbox"):
            parsed = parse_free_text(child)
            if parsed is not None:
                sheet.texts.append(parsed)
    return sheet


def parse_free_text(node) -> Optional[SchText]:
    """Parse a free-text annotation (``text`` / ``textbox`` nodes).

    KiCad 7..10 ``textbox`` wraps the string in an inner ``(text ...)`` node;
    older/other layouts keep the content as the first atom.  Both are handled
    here so page annotations survive across file versions.
    """
    if not sexpr.is_node(node, "text") and not sexpr.is_node(node, "textbox"):
        return None
    kind = node[0]
    at_node = sexpr.first(node, "at")
    x, y, rot = sexpr.xy(at_node) if at_node is not None else (0.0, 0.0, 0.0)
    uuid_node = sexpr.first(node, "uuid")
    content = ""
    if kind == "textbox":
        size_node = sexpr.first(node, "size")
        w = sexpr.to_float(size_node[1]) if size_node is not None and len(size_node) > 1 else 0.0
        h = sexpr.to_float(size_node[2]) if size_node is not None and len(size_node) > 2 else 0.0
        inner = sexpr.first(node, "text")
        if inner is not None and len(inner) > 1:
            content = _text(inner[1])
            inner_at = sexpr.first(inner, "at")
            if inner_at is not None:
                ix, iy, irot = sexpr.xy(inner_at)
                # Inner text coordinates are relative to the box origin.
                x += ix
                y += iy
                rot = irot if irot else rot
        elif len(node) > 1 and isinstance(node[1], str):
            content = node[1]
        return SchText(
            content=content,
            pos=(x, y),
            rotation=rot,
            kind="textbox",
            size=(w, h),
            uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "",
        )
    if len(node) > 1:
        content = _text(node[1])
    return SchText(
        content=content,
        pos=(x, y),
        rotation=rot,
        kind="text",
        uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "",
    )


def resolve_root_file(input_path) -> Path:
    """Accept a .kicad_sch file or a project directory and return the root sheet."""
    p = Path(input_path)
    if p.is_file():
        return p.resolve()
    if p.is_dir():
        pro_files = sorted(p.glob("*.kicad_pro"))
        if pro_files:
            root_candidate = pro_files[0].with_suffix(".kicad_sch")
            if root_candidate.exists():
                return root_candidate.resolve()
        sch_files = sorted(p.glob("*.kicad_sch"))
        if sch_files:
            # Prefer a file that contains sheet_instances (the root sheet).
            for f in sch_files:
                try:
                    nodes = sexpr.parse(f.read_text(encoding="utf-8", errors="replace")[:200000])
                    if nodes and sexpr.is_node(nodes[0], "kicad_sch") and sexpr.first(nodes[0], "sheet_instances"):
                        return f.resolve()
                except Exception:
                    continue
            return sch_files[0].resolve()
    raise FileNotFoundError(f"not a KiCad schematic or project directory: {input_path}")


def load_project(input_path) -> Project:
    root_file = resolve_root_file(input_path)
    project = Project(root=root_file.parent)
    visited: set[str] = set()
    queue: list[tuple[str, Path]] = [("/", root_file)]
    while queue:
        path, file = queue.pop(0)
        key = str(Path(path))
        if key in visited:
            continue
        visited.add(key)
        sheet = parse_sheet_file(file, path)
        project.sheets[path] = sheet
        project.sheet_order.append(path)
        project.files.append(file.resolve())
        for ref in sheet.sheets:
            child_paths = ref.paths or [f"{path.rstrip('/')}/{ref.uuid}"]
            # Normalise the ref so first_path() is correct for hierarchy joins.
            ref.paths = child_paths
            child_file = Path(ref.file)
            candidates = [root_file.parent / child_file]
            if not child_file.is_absolute():
                candidates.append(file.parent / child_file)
            resolved = next((c for c in candidates if c.exists()), candidates[0])
            for child_path in child_paths:
                if child_path not in visited:
                    queue.append((child_path, resolved))
    return project
