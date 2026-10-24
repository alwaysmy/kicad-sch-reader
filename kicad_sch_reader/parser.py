"""Parser for KiCad ``.kicad_sch`` files (KiCad 6..10 s-expression format).

The parser is deliberately tolerant: unknown node kinds are counted and
ignored, and malformed optional fields degrade to defaults instead of
aborting a whole-project review.
"""

from __future__ import annotations

import re
import math
from datetime import datetime
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


def _xy(node):
    if node is None or len(node) < 3:
        raise ValueError("electrical item is missing its position")
    try:
        values = [float(_text(v)) for v in node[1:4]]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid electrical coordinate: {node}") from exc
    if not all(math.isfinite(v) for v in values):
        raise ValueError(f"non-finite electrical coordinate: {node}")
    return values[0], values[1], values[2] if len(values) > 2 else 0.0


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
    if number_node is not None:
        number = _text(number_node[1]) if len(number_node) > 1 else ""
        electrical_type = first_atom
    else:
        number = first_atom
        electrical_type = sexpr.prop(node, "type", "unknown")
    name = _text(name_node[1]) if name_node is not None and len(name_node) > 1 else ""
    if not number or at_node is None:
        raise ValueError("library pin is missing its number or position")
    pos = _xy(at_node)
    hide_node = sexpr.first(node, "hide")
    hidden = "hide" in node[1:] or (hide_node is not None and
             (len(hide_node) == 1 or _text(hide_node[1]) == "yes"))
    # Empirical KiCad 10 fact (validated against kicad-cli netlist on the
    # example projects and a minimal rotation test bench): the pin `at` y
    # coordinate in the symbol definition has the opposite sign of the
    # physical connection offset used by Eeschema connectivity.
    return LibPin(number=number, name=name, electrical_type=electrical_type,
                  pos=(pos[0], -pos[1]), hidden=hidden)


def _parse_symbol_def(sym) -> Optional[LibSymbol]:
    """Parse one ``(symbol "Lib:Name" ...)`` definition node.

    Shared by embedded ``lib_symbols`` sections and standalone ``.kicad_sym``
    library files (identical internal structure).
    """
    if len(sym) < 2:
        return None
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
    # Authoritative power-symbol marker (works for project-local power
    # libraries like "myproj:GND", not just the standard "power:" lib).
    symbol.is_power = sexpr.first(sym, "power") is not None
    return symbol


def parse_lib_symbols(root) -> Dict[str, LibSymbol]:
    out: Dict[str, LibSymbol] = {}
    libs = sexpr.first(root, "lib_symbols")
    if libs is None:
        return out
    for sym in sexpr.children(libs, "symbol"):
        parsed = _parse_symbol_def(sym)
        if parsed is not None:
            out[parsed.lib_id] = parsed
    return out


def parse_kicad_sym_lib(file: Path) -> Dict[str, LibSymbol]:
    """Parse a standalone ``.kicad_sym`` project library.

    Symbols inside a library file are named WITHOUT the library nickname
    (``Audio-Jack-2_Switch_1``); schematic lib_ids carry it
    (``multichannel_mixer:Audio-Jack-2_Switch_1``).  The conventional
    nickname equals the file stem, so index each symbol under
    ``<stem>:<name>`` and additionally under its bare name as fallback for
    non-standard layouts.
    """
    nodes = sexpr.parse(file.read_text(encoding="utf-8"))
    out: Dict[str, LibSymbol] = {}
    for node in nodes:
        if not sexpr.is_node(node, "kicad_symbol_lib"):
            continue
        for sym in sexpr.children(node, "symbol"):
            parsed = _parse_symbol_def(sym)
            if parsed is None:
                continue
            out.setdefault(parsed.lib_id, parsed)
            out.setdefault(f"{file.stem}:{parsed.lib_id}", parsed)
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
    if not math.isfinite(rotation) or rotation % 90 != 0:
        raise ValueError(f"unsupported symbol rotation: {rotation}")
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
    root_uuid: str = "", project_name: str = "",
    external_libs: Optional[Dict[str, LibSymbol]] = None,
) -> Optional[SymbolInstance]:
    if not sexpr.is_node(node, "symbol"):
        return None
    lib_id_node = sexpr.first(node, "lib_id")
    lib_id = _text(lib_id_node[1]) if lib_id_node is not None and len(lib_id_node) > 1 else ""
    at_node = sexpr.first(node, "at")
    x, y, rotation = _xy(at_node)
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
    instances_node = sexpr.first(node, "instances")
    if instances_node is not None:
        matches = []
        projects = list(sexpr.children(instances_node, "project"))
        named = [p for p in projects if len(p) > 1 and _text(p[1]) == project_name]
        if named:
            projects = named
        for proj in projects:
            for item in sexpr.children(proj, "path"):
                if len(item) < 2:
                    continue
                raw = "/" + _text(item[1]).strip("/")
                # Paths carry the root UUID, followed by the entire instance
                # ancestry. Matching only the leaf aliases nested reuse.
                parts = raw.strip("/").split("/")
                if root_uuid:
                    relative = "/" + "/".join(parts[1:]) if parts[0] == root_uuid else raw
                else:
                    relative = "/" + "/".join(parts[1:])
                if relative == sheet_path or raw == sheet_path:
                    matches.append(item)
        overrides = {(sexpr.prop(p, "reference"), sexpr.prop(p, "unit", unit))
                     for p in matches}
        if len(overrides) > 1:
            raise ValueError(f"ambiguous symbol instance overrides at {sheet_path}")
        if overrides:
            reference, unit = next(iter(overrides))
            if reference:
                props["Reference"] = reference
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
    if lib is None and external_libs:
        lib = external_libs.get(lib_id)
    if lib is None:
        # A symbol defined in a project-local library we could not load
        # (wrong nickname, missing file, unshipped lib) is a degraded-input
        # condition, not file corruption: keep the instance for BOM/field
        # review, leave it pinless, and let rule RU610 surface the gap.
        symbol.lib_missing = True
        return symbol
    symbol.power = lib.is_power
    lib_pins = lib.pins_for(unit, body_style)
    pin_nodes = {_text(p[1]): p for p in sexpr.children(node, "pin") if len(p) > 1}
    if pin_nodes and not lib_pins:
        raise ValueError(f"missing pin geometry for {symbol.ref} ({lib_id}, unit {unit}, body {body_style})")
    # Placed (pin ...) records contain UUID metadata, not pin geometry or an
    # exhaustive pin inventory. The embedded library is authoritative.
    for lp in lib_pins:
        lx, ly = transform_point(lp.pos, rotation, mirror)
        pn = pin_nodes.get(lp.number)
        symbol.pins.append(PinInstance(
            number=lp.number, name=lp.name, electrical_type=lp.electrical_type,
            pos=(x + lx, y + ly), uuid=sexpr.prop(pn, "uuid") if pn else "",
            hidden=lp.hidden,
        ))
    return symbol


def parse_sheet_ref(node) -> Optional[SheetRef]:
    if not sexpr.is_node(node, "sheet"):
        return None
    at_node = sexpr.first(node, "at")
    size_node = sexpr.first(node, "size")
    uuid_node = sexpr.first(node, "uuid")
    x, y, _ = _xy(at_node)
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
        px, py, _ = _xy(pat)
        pins.append(SheetPin(name=pname, direction=direction, pos=(px, py)))

    raw_paths: List[str] = []
    path_pages: Dict[str, str] = {}
    instances = sexpr.first(node, "instances")
    if instances is not None:
        for proj in sexpr.children(instances, "project"):
            for path_node in sexpr.children(proj, "path"):
                if len(path_node) < 2:
                    continue
                raw_path = _text(path_node[1])
                raw_paths.append(raw_path)
                page_node = sexpr.first(path_node, "page")
                if page_node is not None and len(page_node) > 1:
                    path_pages[raw_path] = _text(page_node[1])
    uuid = _text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else ""
    # KiCad 10 root sheet instances store (path /<sheet_uuid> (page "N")).
    # Keep paths that really point at this sheet uuid together with their page
    # numbers; the project loader uses them as PDF page map.
    paths = [p for p in raw_paths if uuid and (p == f"/{uuid}" or p.endswith(f"/{uuid}"))]
    pages = path_pages
    first_page = next((v for v in path_pages.values() if v), "")
    return SheetRef(
        name=props.get("Sheetname", ""),
        file=props.get("Sheetfile", ""),
        pos=(x, y),
        size=(sx, sy),
        uuid=uuid,
        pins=pins,
        page=first_page,
        paths=paths,
        pages=pages,
    )


def parse_sheet_file(file: Path, sheet_path: str = "/", *,
                     root_uuid: str = "", project_name: str = "",
                     external_libs: Optional[Dict[str, LibSymbol]] = None) -> SheetData:
    text = file.read_text(encoding="utf-8")
    nodes = sexpr.parse(text)
    if len(nodes) != 1 or not sexpr.is_node(nodes[0], "kicad_sch"):
        raise ValueError(f"expected one kicad_sch document in {file}")
    root = nodes[0]

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
    paper_node = sexpr.first(root, "paper")
    sheet.paper = _text(paper_node[1]) if paper_node is not None and len(paper_node) > 1 else ""
    uuid_node = sexpr.first(root, "uuid")
    sheet.uuid = _text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else ""

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

    if sheet_path == "/":
        for instance in sexpr.children(sexpr.first(root, "sheet_instances"), "path"):
            if len(instance) > 1 and _text(instance[1]) == "/":
                page = sexpr.prop(instance, "page")
                if page.isdigit():
                    sheet.page_no = int(page)

    sheet.lib_symbols = parse_lib_symbols(root)
    instance_overrides = parse_lib_instances(root)

    for child in sexpr.children(root):
        kind = child[0]
        if kind == "symbol":
            symbol = parse_symbol_instance(child, sheet.lib_symbols, sheet_path,
                                           instance_overrides, root_uuid or sheet.uuid,
                                           project_name or file.stem,
                                           external_libs=external_libs)
            if symbol is not None:
                sheet.symbols.append(symbol)
        elif kind == "wire":
            pts = sexpr.first(child, "pts")
            xys = list(sexpr.children(pts, "xy")) if pts is not None else []
            if len(xys) != 2:
                raise ValueError(f"wire requires two endpoints in {file}")
            if len(xys) == 2:
                uuid_node = sexpr.first(child, "uuid")
                sheet.wires.append(
                    Wire(
                        p1=_xy(xys[0])[:2],
                        p2=_xy(xys[1])[:2],
                        uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "",
                    )
                )
        elif kind in ("label", "global_label", "hierarchical_label"):
            if len(child) < 2:
                continue
            at_node = sexpr.first(child, "at")
            x, y, rot = _xy(at_node)
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
                x, y, _ = _xy(at_node)
                uuid_node = sexpr.first(child, "uuid")
                sheet.junctions.append(
                    Junction(pos=(x, y), uuid=_text(uuid_node[1]) if uuid_node is not None and len(uuid_node) > 1 else "")
                )
        elif kind == "no_connect":
            at_node = sexpr.first(child, "at")
            if at_node is not None:
                x, y, _ = _xy(at_node)
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

    ``text`` layout is validated against real projects.  **The ``textbox``
    branch is unverified**: none of our current fixtures contains a textbox
    node, so the inner-``(text ...)`` layout and the relative-coordinate
    handling below are written from the KiCad file-format documentation and
    have never executed against a real file.
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


def _load_project_sym_libs(project_dir: Path) -> Dict[str, LibSymbol]:
    """Load project-local ``.kicad_sym`` libraries for external lookup.

    ``sym-lib-table`` nicknames conventionally equal the file stem
    (``multichannel_mixer`` -> ``multichannel_mixer.kicad_sym``), and symbol
    lib_ids carry the nickname as prefix, so indexing every parsed symbol by
    its full ``lib_id`` covers the standard layout without parsing the table.
    Unparsable library files are skipped (the RU610 rule will surface any
    symbol that stays unresolved).
    """
    out: Dict[str, LibSymbol] = {}
    lib_files = sorted(project_dir.glob("*.kicad_sym"))
    for lib_file in lib_files:
        try:
            out.update(parse_kicad_sym_lib(lib_file))
        except (OSError, ValueError):
            continue
    return out


def load_project(input_path) -> Project:
    root_file = resolve_root_file(input_path)
    project = Project(root=root_file.parent)
    external_libs = _load_project_sym_libs(root_file.parent)
    visited: set[str] = set()
    queue = [("/", root_file, ())]
    root_uuid = ""
    page_by_path: Dict[str, int] = {"/": 1}
    while queue:
        path, file, ancestors = queue.pop(0)
        file = file.resolve()
        if file in ancestors:
            raise ValueError(f"recursive schematic hierarchy: {file} at {path}")
        key = str(Path(path))
        if key in visited:
            continue
        visited.add(key)
        sheet = parse_sheet_file(file, path, root_uuid=root_uuid,
                                 project_name=root_file.stem,
                                 external_libs=external_libs)
        if path == "/":
            root_uuid = sheet.uuid
        if path != "/" or not sheet.page_no:
            sheet.page_no = page_by_path.get(path, 0)
        project.sheets[path] = sheet
        project.sheet_order.append(path)
        project.files.append(file.resolve())
        for ref in sheet.sheets:
            if not ref.uuid:
                raise ValueError(f"sheet reference without UUID in {file}")
            # Expand exactly the child of THIS parent instance. Stored
            # instance lists may contain paths belonging to other parents.
            child_path = f"{path.rstrip('/')}/{ref.uuid}"
            ref.paths = [child_path]
            child_file = Path(ref.file)
            candidates = [file.parent / child_file, root_file.parent / child_file]
            resolved = next((c for c in candidates if c.is_file()), candidates[0])
            raw_parent = f"/{root_uuid}{path.rstrip('/')}"
            raw_child = f"/{root_uuid}{child_path}"
            page_text = ref.pages.get(raw_child, ref.pages.get(raw_parent, "")) or ref.page
            if str(page_text).isdigit():
                page_by_path[child_path] = int(page_text)
            if child_path in visited or any(p == child_path for p, _, _ in queue):
                raise ValueError(f"duplicate sheet instance path {child_path}")
            queue.append((child_path, resolved, ancestors + (file,)))
    return project


def collect_orphans(input_path) -> List[dict]:
    """Find ``.kicad_sch`` files in the project directory tree that the root
    schematic does not reference (leftovers from earlier revisions, deleted
    sheets, copies).  The reference set comes from the load itself
    (``project.files``), which is authoritative for one project root; the
    on-disk set is every ``*.kicad_sch`` under the root directory.

    Reported evidence is filesystem-level (mtime/size) only: KiCad stores no
    internal modification time, so any "is this a leftover" judgement here is
    inference, never a file-format fact.
    """
    root_file = resolve_root_file(input_path)
    root_dir = root_file.parent
    project = load_project(root_file)
    referenced = {str(p) for p in project.files}
    orphans = []
    for f in sorted(root_dir.rglob("*.kicad_sch")):
        f = f.resolve()
        if str(f) in referenced:
            continue
        st = f.stat()
        is_archived = ".history" in f.parts
        note = ("KiCad 历史归档（.history 目录），非当前设计，通常无需处理"
                if is_archived else
                "未被当前工程根图引用的残留图纸；如 mtime 早于其余图纸，很可能是旧版副本")
        orphans.append({
            "file": str(f),
            "relative": str(f.relative_to(root_dir)),
            "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "size_bytes": st.st_size,
            "archived": is_archived,
            "note": note,
        })
    return orphans
