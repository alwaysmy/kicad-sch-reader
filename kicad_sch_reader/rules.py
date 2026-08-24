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

# Reference designators matched as <letters><digits>; anything else is left
# alone to keep the sequence check low-noise.
_REF_RE = re.compile(r"^([A-Za-z]+)(\d+)$")

# Net-naming rule thresholds (heuristic, overridable via review config).
_UNNAMED_RATIO_WARN = 0.3
_UNNAMED_COUNT_WARN = 20


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
                evidence="structural",
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
                evidence="structural",
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
                evidence="declared",
                severity="warning",
                title="元件缺少封装",
                message=f"{sym.ref}（{sym.lib_id}）未指定 Footprint",
                sheet_path=sym.sheet_path,
                ref=sym.ref,
            ))
        if not sym.value:
            issues.append(Issue(
                code="R202",
                evidence="declared",
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
                evidence="structural",
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
                evidence="structural",
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
                evidence="structural",
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
                evidence="structural",
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
                evidence="heuristic",
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
                evidence="structural",
                        severity="error",
                        title="分层图纸文件缺失",
                        message=f"图纸符号 {ref.name or ref.file} 引用的 {ref.file} 未找到",
                        sheet_path=path,
                        ref=ref.name,
                    ))
                elif pin.name not in child_names:
                    issues.append(Issue(
                        code="R602",
                evidence="structural",
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
                evidence="structural",
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
            evidence="official",
        ))
    return issues


def json_safe(obj) -> str:
    try:
        import json
        return json.dumps(obj, ensure_ascii=False, default=str)[:400]
    except Exception:
        return str(obj)[:400]


def check_nc_pin_inventory(project: Project) -> List[Issue]:
    """Inventory every explicitly no-connect-marked pin for human confirmation.

    Mirrors the lceda-sch-reader review discipline: an X marker is a design
    *decision* ("this pin really is unused"), so each one must be confirmable
    against the datasheet.  Power-input pins marked NC are suspicious enough
    to escalate to warning; everything else stays informational.
    """
    issues: List[Issue] = []
    for path in project.sheet_order:
        sheet = project.sheets.get(path)
        if sheet is None:
            continue
        nc_points = {(round(p.pos[0], 3), round(p.pos[1], 3)) for p in sheet.no_connects}
        if not nc_points:
            continue
        for sym in sheet.symbols:
            for pin in sym.pins:
                key = (round(pin.pos[0], 3), round(pin.pos[1], 3))
                # The parser records no_connect on pins only when it saw an
                # explicit per-pin flag; the X symbol itself is geometric, so
                # match by position.
                marked_nc = pin.no_connect or key in nc_points
                if not marked_nc:
                    continue
                ptype = (pin.electrical_type or "unknown").lower()
                sev = "warning" if ptype == "power_in" else "info"
                issues.append(Issue(
                    code="R304",
                    severity=sev,
                    title="NC 引脚确认清单",
                    message=(
                        f"{sym.ref}.{pin.number}（{pin.name or sym.lib_id}，类型 {pin.electrical_type}）"
                        f"被标记为 no-connect；请对照手册确认该脚确实可悬空"
                        + ("——电源输入引脚被 NC 尤为可疑" if sev == "warning" else "")
                    ),
                    sheet_path=path,
                    ref=sym.ref,
                    pin=pin.number,
                    evidence="structural",
                ))
    return issues


def check_title_blocks(project: Project) -> List[Issue]:
    """Flag incomplete title blocks (title/date/rev/company)."""
    issues: List[Issue] = []
    keys = ("title", "date", "rev", "company")
    for path in project.sheet_order:
        fields = project.sheets[path].title_fields if path in project.sheets else {}
        missing = [k for k in keys if not (fields.get(k) or "").strip()]
        if len(missing) == len(keys):
            issues.append(Issue(
                code="R603",
                severity="warning",
                title="标题栏完全空缺",
                message=f"图纸 {path} 的 title_block 缺少全部关键字段（title/date/rev/company）",
                sheet_path=path,
                details={"missing": ", ".join(missing)},
                evidence="declared",
            ))
        elif missing:
            issues.append(Issue(
                code="R603",
                severity="info",
                title="标题栏字段缺失",
                message=f"图纸 {path} 的标题栏缺少: {', '.join(missing)}",
                sheet_path=path,
                details={"missing": ", ".join(missing)},
                evidence="declared",
            ))
    return issues


def check_reference_sequences(project: Project) -> List[Issue]:
    """Report gaps in reference-designator numbering (R1,R2,R5 -> R3,R4 missing).

    Purely informational: gaps usually mean deleted parts during iteration,
    which is fine — but a fresh reviewer should know the numbering is not
    contiguous before using ranges like "R1..R12 are the gain resistors".
    """
    groups: Dict[str, Set[int]] = defaultdict(set)
    for sym in project.all_symbols():
        m = _REF_RE.match(sym.ref or "")
        if not m:
            continue
        groups[m.group(1)].add(int(m.group(2)))
    issues: List[Issue] = []
    for prefix in sorted(groups):
        numbers = groups[prefix]
        lo, hi = min(numbers), max(numbers)
        missing = [n for n in range(lo, hi + 1) if n not in numbers]
        if not missing:
            continue
        shown = ", ".join(f"{prefix}{n}" for n in missing[:8])
        extra = f" …(+{len(missing) - 8})" if len(missing) > 8 else ""
        issues.append(Issue(
            code="R103",
            severity="info",
            title="位号编号不连续",
            message=(
                f"{prefix} 序列在 {prefix}{lo}..{prefix}{hi} 内缺号 {len(missing)} 个: "
                f"{shown}{extra}（通常是迭代删除所致，仅供审阅时参考）"
            ),
            details={"missing": shown},
            evidence="heuristic",
        ))
    return issues


def check_net_naming(netlist: Iterable[Net]) -> List[Issue]:
    """Summarise unnamed (N$) signal nets and prompt naming the important ones."""
    nets = list(netlist)
    unnamed = [n for n in nets if re.match(r"^N\$", n.name)
               and not _is_power_like(n)]
    if not unnamed:
        return []
    named_signal_count = sum(1 for n in nets if not re.match(r"^N\$", n.name))
    ratio = len(unnamed) / max(1, named_signal_count + len(unnamed))
    if len(unnamed) < _UNNAMED_COUNT_WARN and ratio < _UNNAMED_RATIO_WARN:
        return []
    biggest = sorted(unnamed, key=lambda n: -n.pin_count())[:5]
    detail = "; ".join(f"{n.name}({n.pin_count()} 脚)" for n in biggest)
    issues = [Issue(
        code="R402",
        severity="info",
        title="存在较多未命名网络",
        message=(
            f"项目有 {len(unnamed)} 个未命名网络（N$，占网络总数 {ratio:.0%}）；"
            f"关键信号建议命名以便跨页追踪与复查。最大的几个: {detail}"
        ),
        net=", ".join(n.name for n in biggest[:3]),
        evidence="heuristic",
    )]
    return issues


def _is_power_like(net: Net) -> bool:
    return bool(net.power_names) or all(
        p.pin_type.lower() in ("power_in", "power_out") or p.lib_id.startswith("power:")
        for p in net.pins
    )


def run_all_checks(
    project: Project,
    netlist: List[Net],
    erc_markers: Optional[List[dict]] = None,
) -> List[Issue]:
    issues: List[Issue] = []
    issues.extend(check_duplicate_references(project))
    issues.extend(check_reference_sequences(project))
    issues.extend(check_missing_fields(project))
    issues.extend(check_floating_pins(project, netlist))
    issues.extend(check_nc_pin_inventory(project))
    issues.extend(check_single_pin_nets(netlist))
    issues.extend(check_net_name_conflicts(netlist))
    issues.extend(check_net_naming(netlist))
    issues.extend(check_power_decoupling(netlist))
    issues.extend(check_hierarchical_sheet_pins(project))
    issues.extend(check_title_blocks(project))
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
