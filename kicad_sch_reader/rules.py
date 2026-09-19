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
from typing import Dict, Iterable, List, Optional, Set, Tuple

from .model import Issue, Net, PinNet, Project, SymbolInstance

_CAP_VALUE_RE = re.compile(r"(\d+(?:\.\d+)?\s*(?:p|n|u|µ|m)?F)", re.IGNORECASE)

# Reference designators matched as <letters><digits>; anything else is left
# alone to keep the sequence check low-noise.
_REF_RE = re.compile(r"^([A-Za-z]+)(\d+)$")

# Zero-ohm detection aligned with lceda-sch-reader's audited semantics:
# a Value that contains any non-zero digit vetoes the jumpers below
# ("10R"/"50R"/"4k7" are real resistors, not wire links).
_ZERO_FULL_RE = re.compile(r"0(?:[.0]+)?\s*(?:Ω|欧|R|ohm)?", re.IGNORECASE)
_ZERO_TOKEN_RE = re.compile(r"(?:^|[^0-9.])0(?:\.0)?(?:Ω|欧|R(?![A-Za-z0-9]))")
_ZERO_CODE_RE = re.compile(r"(?:^|[^0-9A-Za-z])0000(?![0-9A-Za-z])", re.IGNORECASE)

# Polar-device pin-name normalisation (diode/LED/TVS families).
_POLAR_ANODE = {"A", "ANODE", "+", "PA"}
_POLAR_CATH = {"K", "C", "CATHODE", "-", "NK"}
_POLAR_PREFIXES = ("D", "LED", "TVS")


def is_zero_ohm_value(value) -> bool:
    """True when a component Value denotes a 0Ω link.

    Priority mirrors the audited LCEDA implementation: an explicit non-zero
    digit in the Value vetoes everything else, so "10R" can never be mistaken
    for a wire link by the token fallbacks.
    """
    v = str(value or "").strip()
    if not v:
        return False
    if _ZERO_FULL_RE.fullmatch(v):
        return True
    if re.search(r"[1-9]", v):
        return False
    return bool(_ZERO_TOKEN_RE.search(v) or _ZERO_CODE_RE.search(v))


def _polar_of(pin_name: str) -> Optional[str]:
    n = str(pin_name or "").strip().upper()
    if n in _POLAR_ANODE:
        return "anode"
    if n in _POLAR_CATH:
        return "cathode"
    return None

# Net-naming rule thresholds (built-in heuristic defaults; NOT yet
# configurable — review --config only supports enabled/severity today).
_UNNAMED_RATIO_WARN = 0.3
_UNNAMED_COUNT_WARN = 20


def _is_capacitor(pin: PinNet) -> bool:
    return bool(_CAP_VALUE_RE.search(pin.value or "")) and not (
        pin.lib_id.startswith("power:") or pin.ref.startswith("#"))


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


def _net_alias_names(net: Net) -> List[str]:
    out: List[str] = []
    for group in (net.hierarchical_names, net.global_names, net.power_names, net.labels):
        for name in group or []:
            if name and name != net.name and name not in out:
                out.append(name)
    return out


def check_single_pin_nets(netlist: Iterable[Net]) -> List[Issue]:
    issues: List[Issue] = []
    for net in netlist:
        if net.pin_count() == 1:
            pin = net.pins[0]
            only_power = pin.lib_id.startswith("power:") or pin.ref.startswith("#PWR")
            aliases = _net_alias_names(net)
            is_port = bool(net.hierarchical_names or net.global_names)
            if is_port:
                issues.append(Issue(
                    code="R302H",
                    evidence="structural",
                    severity="info",
                    title="层次/全局端口网络单点连接",
                    message=(
                        f"网络 {net.name} 有层次/全局端口别名 "
                        f"{', '.join(aliases[:6]) or net.name}；本图只有 "
                        f"{pin.ref}.{pin.pin_number} 一个连接点。"
                        f"若该端口在父图/其他子图有连接属正常形态；若全板仅此处，则当前未使用"
                    ),
                    sheet_path=pin.sheet_path,
                    ref=pin.ref,
                    pin=pin.pin_number,
                    net=net.name,
                    details={"aliases": ", ".join(aliases)},
                ))
                continue
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
        elif net.pin_count() == 0 and (net.labels or net.global_names or net.hierarchical_names or net.power_names):
            issues.append(Issue(
                code="R303",
                evidence="structural",
                severity="warning",
                title="标签悬空",
                message=(
                    "标签/层次端口/电源符号 "
                    f"{', '.join(net.labels + net.global_names + net.hierarchical_names + net.power_names)} "
                    "没有连接到任何元件引脚"
                ),
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
        power_pins = [p for p in net.pins if p.pin_type.lower() == "power_in" and not (
            p.lib_id.startswith("power:") or p.ref.startswith("#PWR"))]
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
    """DNP inventory, grouped one issue per sheet.

    A list of not-fitted parts is a review *context*, not one finding per
    part.  Grouping keeps the reviewer's attention on which DNP choices look
    unusual (an IC or a resistor that changes circuit behaviour) instead of
    drowning them in rows of test points.
    """
    per_sheet: Dict[str, List[SymbolInstance]] = defaultdict(list)
    for sym in project.all_symbols():
        if sym.dnp:
            per_sheet[sym.sheet_path].append(sym)
    issues: List[Issue] = []
    for path, syms in sorted(per_sheet.items()):
        notable = [s for s in syms if not (s.ref.startswith("TP") or s.ref.startswith("H"))]
        shown_all = ", ".join(
            f"{s.ref}({s.value or s.lib_id})" for s in syms[:16])
        extra = f" …(+{len(syms) - 16})" if len(syms) > 16 else ""
        message = (
            f"{len(syms)} 个器件标记为不焊接（DNP）: {shown_all}{extra}"
        )
        if len(notable) < len(syms):
            message += f"；其中 {len(syms) - len(notable)} 个为测试点/机械件，其余 {len(notable)} 个请确认 DNP 意图"
        issues.append(Issue(
            code="R701",
            severity="info",
            title="DNP 器件清单（按图纸汇总）",
            message=message,
            sheet_path=path,
            details={"refs": ", ".join(s.ref for s in syms),
                     "notable": ", ".join(s.ref for s in notable)},
            evidence="structural",
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
        # KiCad 10 puts a human-readable "Symbol U101 pin 1" inside items[].
        # The wording follows the KiCad UI language: zh-CN uses 引脚, en uses
        # pin — match both so ref/pin attribution survives locale changes.
        if isinstance(marker.get("items"), list):
            for item in marker["items"]:
                if not isinstance(item, dict):
                    continue
                desc_item = str(item.get("description", ""))
                match = re.match(r"^Symbol\s+(\S+)\s+(?:引脚|[Pp]in)\s+(\S+)", desc_item)
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
    against the datasheet.  Reporting is grouped one issue per component —
    a 24-unused-pin connector is one review item, not 24.  Power-input pins
    marked NC stay per-pin and escalate to warning (always suspicious).
    """
    issues: List[Issue] = []
    for path in project.sheet_order:
        sheet = project.sheets.get(path)
        if sheet is None:
            continue
        nc_points = {(round(p.pos[0], 3), round(p.pos[1], 3)) for p in sheet.no_connects}
        if not nc_points:
            continue
        per_component: Dict[Tuple[str, str], List] = defaultdict(list)
        for sym in sheet.symbols:
            for pin in sym.pins:
                key = (round(pin.pos[0], 3), round(pin.pos[1], 3))
                # The parser records no_connect on pins only when it saw an
                # explicit per-pin flag; the X symbol itself is geometric, so
                # match by position.
                if not (pin.no_connect or key in nc_points):
                    continue
                per_component[(sym.ref, sym.value or sym.lib_id)].append(pin)
        for (ref, value), pins in sorted(per_component.items()):
            power_pins = [p for p in pins
                          if (p.electrical_type or "").lower() == "power_in"]
            for p in power_pins:
                issues.append(Issue(
                    code="R304",
                    severity="warning",
                    title="电源输入引脚被 NC（逐脚确认）",
                    message=(
                        f"{ref}.{p.number}（{p.name or value}，power_in）被标记为"
                        f" no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认"
                    ),
                    sheet_path=path,
                    ref=ref,
                    pin=p.number,
                    evidence="structural",
                ))
            plain = [p for p in pins if p not in power_pins]
            if not plain:
                continue
            nums = [p.number for p in plain]
            shown = ", ".join(nums[:12])
            extra = f" …(+{len(nums) - 12})" if len(nums) > 12 else ""
            ptypes = {((p.electrical_type or "unknown").lower()) for p in plain}
            issues.append(Issue(
                code="R304",
                severity="info",
                title="NC 引脚确认清单（按器件汇总）",
                message=(
                    f"{ref}（{value}）有 {len(plain)} 个引脚被标记为 no-connect:"
                    f" {shown}{extra}（类型 {', '.join(sorted(ptypes))}）；"
                    f"请对照手册确认这些脚确实可悬空"
                ),
                sheet_path=path,
                ref=ref,
                details={"pins": ", ".join(nums)},
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
    """Report gaps in reference-designator numbering (R1,R2,R5 -> R3,R4 missing)
    and designators that do not match the <letters><digits> convention.

    Purely informational and aggregated: one issue per problem class, never
    one row per prefix.  Missing numbers are only enumerated *within the same
    hundred-block* (R201..R205 missing R203): page-hundreds numbering
    (C2xx/C3xx/C7xx on different sheets) makes cross-block gaps meaningless,
    so those are counted but not listed.
    """
    groups: Dict[str, Set[int]] = defaultdict(set)
    nonstandard: List[str] = []
    for sym in project.all_symbols():
        ref = sym.ref or ""
        if not ref or ref.startswith("#"):
            continue
        m = _REF_RE.match(ref)
        if not m:
            nonstandard.append(ref)
            continue
        groups[m.group(1)].add(int(m.group(2)))
    issues: List[Issue] = []
    if nonstandard:
        shown = ", ".join(sorted(nonstandard)[:8])
        extra = f" …(+{len(nonstandard) - 8})" if len(nonstandard) > 8 else ""
        issues.append(Issue(
            code="R103",
            severity="info",
            title="位号格式不规范",
            message=(
                f"{len(nonstandard)} 个位号不符合 字母前缀+数字 规范"
                f"（如 DA、2、R_1）: {shown}{extra}"
            ),
            details={"refs": ", ".join(sorted(nonstandard))},
            evidence="heuristic",
        ))
    gap_summaries: List[str] = []
    gap_details: List[str] = []
    for prefix in sorted(groups):
        numbers = groups[prefix]
        lo, hi = min(numbers), max(numbers)
        if lo == hi:
            continue
        missing_total = (hi - lo + 1) - len(numbers)
        if missing_total <= 0:
            continue
        # Enumerate only gaps inside hundred-blocks that actually hold parts
        # (>=2 refs present): these are plausible "deleted during iteration"
        # skips a reviewer could act on.  Empty hundred-blocks are just the
        # page-hundreds numbering scheme and carry no signal.
        near: List[int] = []
        blocks: Dict[int, Set[int]] = defaultdict(set)
        for n in numbers:
            blocks[n // 100].add(n)
        for block, present in sorted(blocks.items()):
            if len(present) < 2:
                continue
            blo, bhi = min(present), max(present)
            near.extend(n for n in range(blo, bhi + 1) if n not in numbers)
        shown = ", ".join(f"{prefix}{n}" for n in near[:8])
        extra = f" …(+{len(near) - 8})" if len(near) > 8 else ""
        near_txt = f"；段内缺号: {shown}{extra}" if near else ""
        gap_summaries.append(f"{prefix} 缺{missing_total}（{prefix}{lo}..{prefix}{hi}{near_txt}）")
        gap_details.append(f"{prefix}: {missing_total}{near_txt}")
    if gap_summaries:
        issues.append(Issue(
            code="R103",
            severity="info",
            title="位号编号不连续（汇总）",
            message=(
                f"{len(gap_summaries)} 个前缀的位号有缺号: {', '.join(gap_summaries)}。"
                f"跨页编 hundreds 的工程跨段空号属正常（按页分段编号），"
                f"段内缺号通常是迭代删除，仅供审阅时参考"
            ),
            details={"per_prefix": " | ".join(gap_details)},
            evidence="heuristic",
        ))
    return issues


def check_polar_devices(project: Project, netlist: Iterable[Net]) -> List[Issue]:
    """Polarised-device inventory (D*/LED*/TVS* designators): normalise pin
    polarity from pin names (A/K/C/+/-/ANODE/CATHODE); devices whose pins
    cannot be resolved need a datasheet check before any polarity-dependent
    review.

    Mirrors lceda-sch-reader's ``polar`` command, but triggers on the
    *designator prefix only*.  Pin-name hits alone are unreliable here:
    op-amp inputs are literally named "+"/"-" (inverting/non-inverting), so a
    pin-name trigger would flag every amplifier in the project.  Only
    unresolvable devices of the polar families are reported.
    """
    pin_net = _build_pin_net_index(netlist)
    issues: List[Issue] = []
    seen_refs: Set[Tuple[str, str]] = set()
    for sym in project.all_symbols():
        ref = sym.ref or ""
        if not ref or ref.startswith("#") or (ref, sym.value) in seen_refs:
            continue
        prefix_m = re.match(r"^[A-Za-z]+", ref.upper())
        prefix = prefix_m.group(0) if prefix_m else ""
        if prefix not in _POLAR_PREFIXES:
            continue
        seen_refs.add((ref, sym.value))
        polarised = [(p, _polar_of(p.name)) for p in sym.pins]
        unresolved = [p for p, pol in polarised if pol is None]
        if not unresolved:
            continue
        parts = []
        for p in unresolved[:6]:
            net = pin_net.get((sym.sheet_path, ref, p.number))
            net_name = net.name if net else "无网"
            parts.append(f"{p.number}({p.name or '?'})->{net_name}")
        detail = "; ".join(parts)
        issues.append(Issue(
            code="R801",
            severity="info",
            title="极性器件引脚极性未解析",
            message=(
                f"{ref}（{sym.value or sym.lib_id}）有 {len(unresolved)} 个引脚名"
                f"无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），"
                f"涉及时请查手册确认极性: {detail}"
            ),
            sheet_path=sym.sheet_path,
            ref=ref,
            evidence="structural",
        ))
    return issues


def check_net_naming(netlist: Iterable[Net]) -> List[Issue]:
    """Summarise unnamed (N$) signal nets and prompt naming the important ones.

    Thresholds are built-in heuristics (see module constants), not derived
    from any standard.
    """
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
        p.pin_type.lower() in ("power_in", "power_out")
        or p.lib_id.startswith("power:") or p.ref.startswith("#PWR")
        for p in net.pins
    )


# ---------------- R902: interface direction semantics ----------------
#
# Signal-direction words (TX/RX, MOSI/MISO, SDO/SDI, DOUT/DIN) are checked as
# *declared* evidence: net/label names and composite MCU pin names
# ("PB10/UART3TX/I2C2SCL").  Pin electrical types are NOT authoritative here
# (symbol authors mark them inconsistently) — a type conflict is info only,
# never error.  Master-view names (MOSI/MISO) keep one name across the whole
# bus, so same-family pins on one net are normal there; local-view names
# (TX/SDO/DOUT are outputs, RX/SDI/DIN are inputs) collide when two different
# chips both claim the same direction on one net.

_DIR_WORD_RE = re.compile(
    r"(?<![A-Za-z])(?:UART\d*_?)?"
    r"(?P<word>TXD|RXD|TX|RX|MOSI|MISO|SDO|SDI|DOUT|DIN)(?![A-Za-z0-9_])",
    re.IGNORECASE,
)

# The lookahead must exclude digits/underscore on purpose:
# * "RX1_P"/"RX_{1}-" are USB-C/PCIe *industry-standard pin names*, not the
#   designer's direction declaration — exempting them kills the diff-pair
#   false positives on connector names;
# * "TX_DISABLE"/"TX_FAULT"/"DIN_14" are control/config functions, not
#   direction.  A direction word must therefore end the token.

_OUT_LOCAL = {"tx", "sdo", "dout"}
_IN_LOCAL = {"rx", "sdi", "din"}
_R902_TITLES = {
    "collision_out": "接口方向语义冲突（双发送）",
    "collision_in": "接口方向语义冲突（全接收）",
    "mosi_swap": "MOSI/MISO 命名互换嫌疑",
    "type_mismatch": "引脚电气类型与命名语义不符",
}


def direction_family(text) -> Optional[str]:
    """First interface-direction family found in a net/pin name.

    Returns one of tx/rx/mosi/miso/sdo/sdi/dout/din, or None.  The optional
    UART prefix ("UART3TX", "UART_TX") is tolerated; matches must sit on
    token boundaries so "CTX"/"TXT"/"BOARDING" never fire.
    """
    m = _DIR_WORD_RE.search(str(text or ""))
    if not m:
        return None
    word = m.group("word").lower()
    return {"txd": "tx", "rxd": "rx"}.get(word, word)


def analyze_direction_group(net_name: str, members: List[dict]) -> List[dict]:
    """Shared direction-semantics analysis over one net's non-power pins.

    *members* items: {"ref", "pin", "pin_name", "pin_type" (optional str)}.
    Used verbatim by the KiCad rule engine and by the LCEDA `.epro` review.
    """
    findings: List[dict] = []

    def fmt(m: dict) -> str:
        return f"{m['ref']}.{m['pin']}({m.get('pin_name') or '?'})"

    pin_fams = [(m, direction_family(m.get("pin_name"))) for m in members]
    pin_fams = [(m, f) for m, f in pin_fams if f]
    if not pin_fams:
        return findings

    outs = [(m, f) for m, f in pin_fams if f in _OUT_LOCAL]
    ins = [(m, f) for m, f in pin_fams if f in _IN_LOCAL]
    out_refs = {m["ref"] for m, _ in outs}
    in_refs = {m["ref"] for m, _ in ins}
    if len(out_refs) >= 2:
        findings.append({"kind": "collision_out", "severity": "warning", "message":
            f"网络 {net_name} 上 {len(out_refs)} 个器件的引脚名均为发送语义"
            f"（{', '.join(fmt(m) for m, _ in sorted(outs, key=lambda x: x[0]['ref']))}）；"
            f"单向信号只应有一个驱动方，请确认哪端为发送，对端（FPGA/MCU）约束方向勿写反"})
    if len(in_refs) >= 2 and not outs:
        findings.append({"kind": "collision_in", "severity": "warning", "message":
            f"网络 {net_name} 上 {len(in_refs)} 个器件的引脚名均为接收语义且无发送语义引脚"
            f"（{', '.join(fmt(m) for m, _ in sorted(ins, key=lambda x: x[0]['ref']))}）；请确认驱动方是否缺失"})

    net_fam = direction_family(net_name)
    for m, f in pin_fams:
        if (net_fam == "mosi" and f == "miso") or (net_fam == "miso" and f == "mosi"):
            findings.append({"kind": "mosi_swap", "severity": "warning", "message":
                f"网络 {net_name}（{net_fam.upper()} 语义）连接了 {fmt(m)}"
                f"（{f.upper()} 语义）；MOSI/MISO 命名疑似互换，请核对主从数据方向"})

    for m, f in pin_fams:
        tl = str(m.get("pin_type") or "").lower()
        if f in _OUT_LOCAL and tl == "input":
            bad = "发送(TX/SDO/DOUT)", "input"
        elif f in _IN_LOCAL and tl == "output":
            bad = "接收(RX/SDI/DIN)", "output"
        else:
            continue
        findings.append({"kind": "type_mismatch", "severity": "info", "message":
            f"{fmt(m)} 引脚名为{bad[0]}语义，但符号电气类型标注为 {bad[1]}；"
            f"符号电气类型常不规范，仅提示人工核对，不作为判定依据"})
    return findings


def check_interface_direction(project: Project, netlist: Iterable[Net]) -> List[Issue]:
    """R902: interface-direction semantics over net/label names and composite
    MCU pin names.  Deliberately *not* based on pin electrical types except as
    an informational cross-check (symbol types are frequently sloppy)."""
    issues: List[Issue] = []
    for net in netlist:
        members = [{"ref": p.ref, "pin": p.pin_number, "pin_name": p.pin_name,
                    "pin_type": p.pin_type}
                   for p in net.pins
                   if not (p.ref.startswith("#") or p.lib_id.startswith("power:"))]
        if len(members) < 2:
            continue
        for f in analyze_direction_group(net.name, members):
            issues.append(Issue(
                code="R902",
                severity=f["severity"],
                title=_R902_TITLES[f["kind"]],
                message=f["message"],
                net=net.name,
                evidence="declared",
            ))
    return issues


def load_config(path) -> dict:
    """Load a review-rule config JSON (enabled/severity per rule code)."""
    import json
    from pathlib import Path as _Path
    data = json.loads(_Path(path).read_text(encoding="utf-8"))
    if not isinstance(data.get("rules", {}), dict):
        raise ValueError("config 'rules' must be an object")
    return data


def apply_config(issues: List[Issue], config: Optional[dict]) -> List[Issue]:
    """Filter/override issues per ``{"rules": {"R501": {"enabled": false,
    "severity": "warning"}}}``.  Unknown codes in the config are ignored."""
    if not config:
        return issues
    table = config.get("rules", {})
    out = []
    for issue in issues:
        entry = table.get(issue.code)
        if isinstance(entry, dict):
            if entry.get("enabled") is False:
                continue
            sev = entry.get("severity")
            if sev in ("error", "warning", "info"):
                issue.severity = sev
        elif entry is False:
            continue
        out.append(issue)
    out.sort(key=lambda i: i.sort_key())
    return out


def run_all_checks(
    project: Project,
    netlist: List[Net],
    erc_markers: Optional[List[dict]] = None,
    config: Optional[dict] = None,
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
    issues.extend(check_polar_devices(project, netlist))
    issues.extend(check_dnp_inventory(project))
    issues.extend(check_interface_direction(project, netlist))
    if erc_markers:
        issues.extend(erc_markers_to_issues(erc_markers))
    issues.sort(key=lambda i: i.sort_key())
    return apply_config(issues, config)


def severity_counts(issues: Iterable[Issue]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for issue in issues:
        counts[issue.severity] = counts.get(issue.severity, 0) + 1
    return counts
