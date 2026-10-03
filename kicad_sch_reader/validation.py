"""Compare electrical partitions, independently of arbitrary net names.

The official exporter omits pseudo-components (#PWR...) and names genuinely
unconnected pins ``unconnected-*``. Physical pins are identified by the full
component instance path plus reference and pin number. A multi-unit component
uses its earliest numbered sheet path, as the official component record does.
"""
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

from . import sexpr


def _sheet_path(raw, root_uuid=""):
    parts = [p for p in raw.split("/") if p]
    if parts and root_uuid and parts[0] == root_uuid:
        parts = parts[1:]
    return "/" + "/".join(parts)


def official_partitions(path, root_uuid="", *, include_unconnected=False):
    text = Path(path).read_text(encoding="utf-8")
    if text.lstrip().startswith("<"):
        return _official_xml(text, root_uuid, include_unconnected)
    nodes = sexpr.parse(text)
    if len(nodes) != 1 or not sexpr.is_node(nodes[0], 'export'):
        raise ValueError('expected one official KiCad export document')
    root = nodes[0]
    paths = {}
    for comp in sexpr.children(sexpr.first(root, 'components'), 'comp'):
        ref = sexpr.prop(comp, 'ref')
        sheet = sexpr.first(comp, 'sheetpath')
        raw = sexpr.prop(sheet, 'tstamps') if sheet else ''
        if not ref or not raw or ref in paths:
            raise ValueError(f'ambiguous/missing official component identity: {ref}')
        paths[ref] = _sheet_path(raw, root_uuid)
    groups, names = [], []
    for net in sexpr.children(sexpr.first(root, 'nets'), 'net'):
        name = sexpr.prop(net, 'name')
        if not include_unconnected and name.startswith('unconnected-'):
            continue
        pins = set()
        for node in sexpr.children(net, 'node'):
            ref, pin = sexpr.prop(node, 'ref'), sexpr.prop(node, 'pin')
            if ref.startswith('#'):
                continue
            if ref not in paths or not pin:
                raise ValueError(f'unknown official pin identity: {ref}.{pin}')
            pins.add((paths[ref], ref, pin))
        if pins:
            groups.append(frozenset(pins)); names.append(name)
    return groups, names


def _official_xml(text, root_uuid, include_unconnected):
    root = ET.fromstring(text)
    if root.tag != "export":
        raise ValueError("expected official KiCad export XML")
    paths = {}
    for comp in root.findall("components/comp"):
        ref = comp.get("ref")
        sheet = comp.find("sheetpath")
        if not ref or ref in paths or sheet is None or sheet.get("tstamps") is None:
            raise ValueError(f"ambiguous/missing official component identity: {ref}")
        paths[ref] = _sheet_path(sheet.get("tstamps"), root_uuid)
    groups, names = [], []
    for net in root.findall("nets/net"):
        name = net.get("name", "")
        if not include_unconnected and name.startswith("unconnected-"):
            continue
        pins = set()
        for node in net.findall("node"):
            ref, pin = node.get("ref", ""), node.get("pin", "")
            if ref.startswith("#"):
                continue
            if ref not in paths or not pin:
                raise ValueError(f"unknown official pin identity: {ref}.{pin}")
            pins.add((paths[ref], ref, pin))
        if pins:
            groups.append(frozenset(pins)); names.append(name)
    return groups, names


def reader_partitions(project, netlist, *, include_unconnected=False):
    by_ref = defaultdict(list)
    for symbol in project.all_symbols():
        if symbol.ref and not symbol.ref.startswith('#'):
            by_ref[symbol.ref].append(symbol)
    paths = {}
    for ref, symbols in by_ref.items():
        units = set()
        for sym in symbols:
            if sym.unit in units:
                raise ValueError(f'ambiguous repeated reference/unit: {ref}.{sym.unit}')
            units.add(sym.unit)
        candidate_paths = {s.sheet_path for s in symbols}
        if len(candidate_paths) == 1:
            paths[ref] = next(iter(candidate_paths))
        else:
            # KiCad's component record uses the earliest sheet by page number,
            # not the smallest unit. Refuse ambiguous/missing page metadata
            # rather than claiming different pin identities for an equal graph.
            pages = [(project.sheets[path].page_no, path) for path in candidate_paths]
            if any(page <= 0 for page, _ in pages) or len({page for page, _ in pages}) != len(pages):
                raise ValueError(f"ambiguous sheet page order for multi-unit component {ref}")
            paths[ref] = min(pages)[1]
    groups, names = [], []
    for net in netlist:
        pins = frozenset((paths[p.ref], p.ref, p.pin_number)
                        for p in net.pins if not p.ref.startswith('#'))
        if pins:
            groups.append(pins); names.append(net.name)
    if include_unconnected:
        connected = set().union(*groups) if groups else set()
        inventory = {(paths[ref], ref, pin.number)
                     for ref, symbols in by_ref.items() for sym in symbols for pin in sym.pins}
        for pin in sorted(inventory - connected):
            groups.append(frozenset([pin])); names.append("unconnected")
    return groups, names


def compare_partitions(ours, official):
    """Exact coverage + split/short detection; never use labels as identity.

    Duplicate occurrence of a physical pin on distinct nets is an error, not
    a dictionary overwrite. Empty graphs cannot claim a verified pass.
    """
    def index(groups):
        result = {}
        for i, group in enumerate(groups):
            for pin in group:
                if pin in result:
                    raise ValueError(f'pin belongs to multiple nets: {pin}')
                result[pin] = i
        return result
    a, b = index(ours), index(official)
    missing, extra = sorted(b.keys() - a.keys()), sorted(a.keys() - b.keys())
    splits = [sorted({a[p] for p in g if p in a}) for g in official]
    shorts = [sorted({b[p] for p in g if p in b}) for g in ours]
    splits = [g for g in splits if len(g) > 1]
    shorts = [g for g in shorts if len(g) > 1]
    common = a.keys() & b.keys()
    bad_pins = [p for p in common if
                (ours[a[p]] & common) != (official[b[p]] & common)]
    return {
        'passed': bool(b) and not (missing or extra or splits or shorts),
        'ours_pins': len(a), 'official_pins': len(b), 'common_pins': len(common),
        'missing_pins': len(missing), 'extra_pins': len(extra),
        'split_nets': len(splits), 'shorted_nets': len(shorts),
        'partition_mismatch_pins': len(bad_pins),
        'missing_samples': missing[:12], 'extra_samples': extra[:12],
        'partition_mismatch_samples': sorted(bad_pins)[:12],
    }
