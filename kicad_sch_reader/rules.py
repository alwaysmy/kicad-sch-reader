"""Design-review rule engine.

Rules intentionally stay at the "schematic reviewer" level:

* deterministic, explainable checks that are hard to get from ERC alone
  (missing fields, dangling labels, duplicate references, single-pin nets,
  decoupling-by-net presence);
* official KiCad ERC results are incorporated separately by the CLI so the
  two data sources stay distinguishable.

Every rule returns :class:`Issue` objects; nothing is printed from this module.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Set

from .model import Issue, Net, PinNet, Project, SymbolInstance

_CAP_VALUE_RE = re.compile(r"(\d+(?:\.\d+)?\s*(?:p|n|u|µ|m)?F)", re.IGNORECASE)


def _is_capacitor(pin: PinNet) -> bool:
    return bool(_CAP_VALUE_RE.search(pin.value or "")) and not pin.lib_id.startswith("power:")


def _severity_for_pin_type(pin_type: str, has_net: bool) -> Optional[str]:
    if has_net:
        return None
    ptype = (pin_type or "unknown").lower()
    if ptype in ("power_in", "input", "output", "bidirectional", "tri_state",
                 "open_collector", "open_emitter"):
        return "error" if ptype == "power_in" else "warning"
    if ptype in ("power_out", "free", "no_connect", "not_connected"):
        return None  # unconnected power-out / explicitly free pins are normal
    return "info"


def check_duplicate_references(project: Project) -> List[Issue]:
    issues: List[Issue] = []
    seen_sheet: Dict[tuple, SymbolInstance] = {}
    seen_project: Dict[str, List[SymbolInstance]] = defaultdict(list)
    for sym in project.all_symbols():
        if not sym.ref or sym.ref.startswith("#"):
            continue
        # KiCad represents multi-unit parts as several symbol nodes sharing
        # the same reference but with different `unit` values; that is legal.
        key = (sym.sheet_path, sym.ref, sym.unit)
        if key in seen_sheet:
            other = seen_sheet[key]
            issues.append(Issue(
                code="R101",
                severity="error",
                title="同一页内重复位号",
                message=f"位号 {sym.ref}（unit {sym.unit}）在 {sym.sheet_path} 上重复（{other.lib_id} 与 {sym.lib_id}）",
                sheet_path=sym.sheet_path,
                ref=sym.ref,
            ))
        else:
            seen_sheet[key] = sym
        seen_project[(sym.ref, sym.unit)].append(sym)

    for (ref, unit), syms in seen_project.items():
        paths = sorted({s.sheet_path for s in syms})
        if len(paths) > 1:
            issues.append(Issue(
                code="R102",
                severity="warning",
                title="位号在多页重复",
                message=f"位号 {ref}（unit {unit}）出现在多页: {', '.join(paths)}（分层复用需确认是同一实例的重复放置）",
                ref=ref,
                details={"paths": ", ".join(paths)},
            ))
    return issues


def check_missing_fields(project: Project) -> List[Issue]:
    issues: List[Issue] = []
    for sym in project.all_symbols():
        if sym.is_power_symbol:
            continue
        if sym.dnp:
            continue
        if sym.on_board and not sym.footprint:
            issues.append(Issue(
                code="R201",
                severity="warning",
                title="元件缺少封装",
                message=f"{sym.ref}（{sym.lib_id}）未指定 Footprint",
                sheet_path=sym.sheet_path,
                ref=sym.ref,
            ))
        if not sym.value:
            issues.append(Issue(
                code="R202",
                severity="info",
                title="元件值/型号为空",
                message=f"{sym.ref}（{sym.lib_id}）的 Value 为空",
                sheet_path=sym.sheet_path,
                ref=sym.ref,
            ))
    return issues


def _build_pin_net_index(netlist: Iterable[Net]) -> Dict[tuple, Net]:
    out: Dict[tuple, Net] = {}
    for net in netlist:
        for p in net.pins:
            out[(p.sheet_path, p.ref, p.pin_number)] = net
    return out


def check_floating_pins(project: Project, netlist: Iterable[Net]) -> List[Issue]:
    pin_net = _build_pin_net_index(netlist)
    issues: List[Issue] = []
    for sym in project.all_symbols():
        for pin in sym.pins:
            key = (sym.sheet_path, sym.ref, pin.number)
            if key in pin_net:
                continue
            if pin.no_connect:
                continue
            sev = _severity_for_pin_type(pin.electrical_type, has_net=False)
            if sev is None:
                continue
            issues.append(Issue(
                code="R301",
                severity=sev,
                title="引脚未连接到任何网络",
                message=(
                    f"{sym.ref}.{pin.number}（{pin.name or sym.lib_id}，类型 {pin.electrical_type}）"
                    f"没有导线/标签连接，也未放置 no-connect 标记"
                ),
                sheet_path=sym.sheet_path,
                ref=sym.ref,
                pin=pin.number,
            ))
    return issues


def check_single_pin_nets(netlist: Iterable[Net]) -> List[Issue]:
    issues: List[Issue] = []
    for net in netlist:
        if net.pin_count() == 1:
            pin = net.pins[0]
            only_power = pin.lib_id.startswith("power:")
            issues.append(Issue(
                code="R302",
                severity="info" if only_power else "warning",
                title="单引脚网络",
                message=(
                    f"网络 {net.name} 只有 {pin.ref}.{pin.pin_number} 一个连接点"
                    + ("（仅为电源符号，无实际负载）" if only_power else "，请确认是否悬空或遗漏连接")
                ),
                sheet_path=pin.sheet_path,
                ref=pin.ref,
                pin=pin.pin_number,
                net=net.name,
            ))
        elif net.pin_count() == 0 and (net.labels or net.global_names or net.power_names):
            issues.append(Issue(
                code="R303",
                severity="warning",
                title="标签悬空",
                message=f"标签/电源符号 {', '.join(net.labels + net.global_names + net.power_names)} 没有连接到任何元件引脚",
                net=net.name,
            ))
    return issues


def check_net_name_conflicts(netlist: Iterable[Net]) -> List[Issue]:
    issues: List[Issue] = []
    for net in netlist:
        if net.has_conflict:
            issues.append(Issue(
                code="R401",
                severity="error",
                title="网络名冲突",
                message=(
                    f"网络被命名为多个全局网络: {', '.join(net.conflict_names)}；"
                    f"当前工具暂按 '{net.name}' 归并，请用 KiCad ERC 复核"
                ),
                net=net.name,
            ))
    return issues


def check_power_decoupling(netlist: Iterable[Net]) -> List[Issue]:
    """Per power-input pin: is there at least one capacitor on the same net?"""
    issues: List[Issue] = []
    for net in netlist:
        power_pins = [p for p in net.pins if p.pin_type.lower() == "power_in" and not p.lib_id.startswith("power:")]
        if not power_pins:
            continue
        caps = [p for p in net.pins if _is_capacitor(p)]
        if caps:
            continue
        for p in power_pins[:8]:
            issues.append(Issue(
                code="R501",
                severity="info",
                title="电源引脚网络上未发现去耦电容",
                message=(
                    f"{p.ref}.{p.pin_number}（{p.value or p.lib_id}）的电源网络 {net.name} "
                    f"上没有检测到电容；请核对是否已就近放置去耦电容"
                ),
                sheet_path=p.sheet_path,
                ref=p.ref,
                pin=p.pin_number,
                net=net.name,
            ))
    return issues


def check_hierarchical_sheet_pins(project: Project) -> List[Issue]:
    """Warn about sheet pins whose child sheet has no matching hierarchical label."""
    issues: List[Issue] = []
    for path in project.sheet_order:
        parent = project.sheets.get(path)
        if parent is None:
            continue
        for ref in parent.sheets:
            child = project.sheets.get(ref.first_path)
            child_names: Set[str] = set()
            if child is not None:
                child_names = {l.name for l in child.labels if l.kind == "hierarchical_label"}
            for pin in ref.pins:
                if child is None:
                    issues.append(Issue(
                        code="R601",
                        severity="error",
                        title="分层图纸文件缺失",
                        message=f"图纸符号 {ref.name or ref.file} 引用的 {ref.file} 未找到",
                        sheet_path=path,
                        ref=ref.name,
                    ))
                elif pin.name not in child_names:
                    issues.append(Issue(
                        code="R602",
                        severity="warning",
                        title="图纸引脚缺少对应分层标签",
                        message=f"图纸符号 {ref.name or ref.file} 的引脚 {pin.name} 在子图 {ref.file} 中没有同名 hierarchical label",
                        sheet_path=path,
                        ref=ref.name,
                        pin=pin.name,
                    ))
    return issues


def check_dnp_inventory(project: Project) -> List[Issue]:
    issues: List[Issue] = []
    for sym in project.all_symbols():
        if sym.dnp:
            issues.append(Issue(
                code="R701",
                severity="info",
                title="DNP 器件",
                message=f"{sym.ref}（{sym.value or sym.lib_id}）被标记为不焊接（DNP）",
                sheet_path=sym.sheet_path,
                ref=sym.ref,
            ))
    return issues


def erc_markers_to_issues(markers: List[dict]) -> List[Issue]:
    issues: List[Issue] = []
    for marker in markers:
        sev = str(marker.get("severity", "info")).lower()
        if sev == "exclusion":
            sev = "info"
        typ = str(marker.get("type", "ERC"))
        desc = str(marker.get("description", ""))
        title = str(marker.get("title", ""))
        sheet_path = str(marker.get("sheet_path", ""))
        ref = ""
        pin = ""
        # KiCad 10 puts a human-readable "Symbol U101 引脚 1" inside items[].
        if isinstance(marker.get("items"), list):
            for item in marker["items"]:
                if not isinstance(item, dict):
                    continue
                desc_item = str(item.get("description", ""))
                match = re.match(r"^Symbol\s+(\S+)\s+引脚\s+(\S+)", desc_item)
                if match:
                    ref, pin = match.group(1), match.group(2)
                elif not ref:
                    ref = str(item.get("ref") or item.get("reference") or "")
                if not pin:
                    pin = str(item.get("pin") or item.get("pin_number") or "")
                if ref:
                    break
        issues.append(Issue(
            code=f"ERC-{typ}",
            severity=sev,
            title=title or typ,
            message=desc or json_safe(marker),
            sheet_path=sheet_path,
            ref=ref,
            pin=pin,
        ))
    return issues


def json_safe(obj) -> str:
    try:
        import json
        return json.dumps(obj, ensure_ascii=False, default=str)[:400]
    except Exception:
        return str(obj)[:400]


def run_all_checks(
    project: Project,
    netlist: List[Net],
    erc_markers: Optional[List[dict]] = None,
) -> List[Issue]:
    issues: List[Issue] = []
    issues.extend(check_duplicate_references(project))
    issues.extend(check_missing_fields(project))
    issues.extend(check_floating_pins(project, netlist))
    issues.extend(check_single_pin_nets(netlist))
    issues.extend(check_net_name_conflicts(netlist))
    issues.extend(check_power_decoupling(netlist))
    issues.extend(check_hierarchical_sheet_pins(project))
    issues.extend(check_dnp_inventory(project))
    if erc_markers:
        issues.extend(erc_markers_to_issues(erc_markers))
    issues.sort(key=lambda i: i.sort_key())
    return issues


def severity_counts(issues: Iterable[Issue]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for issue in issues:
        counts[issue.severity] = counts.get(issue.severity, 0) + 1
    return counts
