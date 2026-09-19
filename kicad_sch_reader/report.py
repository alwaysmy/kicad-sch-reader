"""Markdown / JSON review-report writers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .model import Issue, Net, Project, SymbolInstance
from .rules import severity_counts


def _natkey(text: str):
    import re as _re
    return [int(x) if x.isdigit() else x.lower() for x in _re.split(r"(\d+)", str(text or ""))]


def _page_map(project: Project) -> Dict[str, int]:
    """sheet_path -> PDF page number.

    KiCad stores the real per-instance page number in the root sheet's
    ``(instances (path /<uuid> (page "N")))`` records; fall back to sheet_order
    only when a project/version does not provide it.
    """
    out: Dict[str, int] = {}
    for idx, path in enumerate(project.sheet_order):
        sheet = project.sheets.get(path)
        page_no = int(getattr(sheet, "page_no", 0) or 0)
        out[path] = page_no if page_no > 0 else idx + 1
    return out


def _net_alias_list(net: Net) -> List[str]:
    out: List[str] = []
    for group in (net.hierarchical_names, net.global_names, net.power_names, net.labels):
        for name in group or []:
            if name and name != net.name and name not in out:
                out.append(name)
    return out


def _net_kind(net: Net) -> str:
    if net.power_names:
        return "power"
    if net.global_names:
        return "global_port"
    if net.hierarchical_names:
        return "hierarchical_port"
    if net.labels:
        return "local"
    return "unnamed"


def _component_kind(sym: SymbolInstance) -> str:
    ref = (sym.ref or "").upper()
    lib = (sym.lib_id or "").lower()
    if sym.is_power_symbol or ref.startswith("#PWR"):
        return "power_symbol"
    if ref.startswith("TP"):
        return "testpoint"
    if ref.startswith(("R", "C", "L", "FB", "D", "LED", "TVS", "RN")):
        return "passive"
    if "connector" in lib or "conn" in lib or ref.startswith(("J", "P", "CN")):
        return "connector"
    return "active"


def _is_cap_ref(ref: str) -> bool:
    return bool(re.match(r"^C\d", str(ref or ""), re.IGNORECASE))


def _power_rail_rows(netlist: List[Net], page_map: Dict[str, int]) -> List[dict]:
    rows = []
    for net in netlist:
        power_pins = [p for p in net.pins if (p.pin_type or "").lower() == "power_in"
                      and not (p.lib_id.startswith("power:") or p.ref.startswith("#PWR"))]
        if not power_pins:
            continue
        caps = sorted({p.ref for p in net.pins if _is_cap_ref(p.ref)})
        rows.append({
            "name": net.name,
            "page_nos": sorted({page_map.get(p.sheet_path, 0) for p in power_pins}),
            "power_pin_count": len(power_pins),
            "power_pins": [f"{p.ref}.{p.pin_number}" for p in power_pins[:12]],
            "cap_count": len(caps),
            "caps": caps,
            "decoupled": bool(caps),
        })
    rows.sort(key=lambda r: r["name"])
    return rows


def _component_rows(project: Project, page_map: Dict[str, int]) -> List[dict]:
    rows = []
    for sym in project.all_symbols():
        if not sym.ref:
            continue
        rows.append({
            "ref": sym.ref,
            "value": sym.value,
            "lib_id": sym.lib_id,
            "footprint": sym.footprint,
            "sheet_path": sym.sheet_path,
            "page_no": page_map.get(sym.sheet_path, 0),
            "kind": _component_kind(sym),
            "unit": sym.unit,
            "dnp": sym.dnp,
            "in_bom": sym.in_bom,
            "on_board": sym.on_board,
            "is_power_symbol": sym.is_power_symbol,
            "description": sym.properties.get("Description", ""),
            "datasheet": sym.properties.get("Datasheet", ""),
        })
    rows.sort(key=lambda r: _natkey(r["ref"]))
    return rows


def project_stats(project: Project, netlist: List[Net], issues: List[Issue]) -> dict:
    symbols = project.all_symbols()
    page_map = _page_map(project)
    components = _component_rows(project, page_map)
    return {
        "root": str(project.root),
        "sheet_count": len(project.sheets),
        "sheets": [
            {
                "path": p,
                "page_no": page_map.get(p, 0),
                "file": str(s.file),
                "title": s.title,
                "symbols": len(s.symbols),
                "wires": len(s.wires),
                "labels": len(s.labels),
                "junctions": len(s.junctions),
                "no_connects": len(s.no_connects),
                "hierarchical_sheets": len(s.sheets),
                "version": s.version,
                "generator": s.generator,
            }
            for p in project.sheet_order
            for s in [project.sheets[p]]
        ],
        "symbol_count": len(symbols),
        "component_count": len([c for c in components if not c["is_power_symbol"]]),
        "passive_count": len([c for c in components if c["kind"] == "passive"]),
        "testpoint_count": len([c for c in components if c["kind"] == "testpoint"]),
        "components": components,
        "power_rails": _power_rail_rows(netlist, page_map),
        "net_count": len(netlist),
        "named_net_count": sum(1 for n in netlist if not n.name.startswith("N$")),
        "pin_connection_count": sum(len(n.pins) for n in netlist),
        "issue_count": len(issues),
        "severity_counts": severity_counts(issues),
    }


def _escape_md(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def write_markdown(path, project: Project, netlist: List[Net], issues: List[Issue],
                   erc_summary: Optional[dict] = None, extra_notes: Optional[List[str]] = None) -> None:
    stats = project_stats(project, netlist, issues)
    page_map = _page_map(project)
    lines: List[str] = []
    lines.append(f"# KiCad 原理图审查报告 — {Path(path).stem}")
    lines.append("")
    lines.append(f"> 由 kicad-sch-reader 自动生成，根原理图：`{project.root}`")
    lines.append("")
    lines.append("## 1. 工程概览")
    lines.append("")
    lines.append("| 项目 | 值 |")
    lines.append("| --- | --- |")
    lines.append(f"| 图纸页数 | {stats['sheet_count']} |")
    lines.append(f"| 元件符号数 | {stats['symbol_count']} |")
    lines.append(f"| 网络数 | {stats['net_count']}（命名网络 {stats['named_net_count']}） |")
    lines.append(f"| 已解析引脚连接数 | {stats['pin_connection_count']} |")
    lines.append(f"| 发现问题总数 | {stats['issue_count']} |")
    sc = stats["severity_counts"]
    lines.append(f"| 问题分级 | error={sc.get('error', 0)} / warning={sc.get('warning', 0)} / info={sc.get('info', 0)} |")
    if erc_summary:
        label_map = {"error": "errors", "warning": "warnings",
                     "exclusion": "exclusions", "info": "infos"}
        parts = ", ".join(
            f"{label_map.get(k, k)}={v}" for k, v in sorted(erc_summary.items()))
        lines.append(f"| KiCad ERC | {parts} |")
    lines.append("")
    lines.append("### 图纸清单（页码按 KiCad 导出顺序 = PDF 页序）")
    lines.append("")
    lines.append("| PDF页 | 路径 | 文件 | 标题 | 元件 | 导线 | 标签 | 连接点 | NC | 版本/生成器 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for s in stats["sheets"]:
        lines.append(
            f"| {s.get('page_no', 0)} | `{s['path']}` | `{Path(s['file']).name}` | {_escape_md(s['title'])} | {s['symbols']} | "
            f"{s['wires']} | {s['labels']} | {s['junctions']} | {s['no_connects']} | "
            f"{s['version']} / {s['generator']} |"
        )
    lines.append("")
    lines.append("### 元件清单（位号 / Value / 封装 / 页码）")
    lines.append("")
    lines.append(f"共 {stats['component_count']} 个实体元件；其中无源件 {stats['passive_count']}、"
                 f"测试点 {stats['testpoint_count']}。电源符号 (#PWR) 不列在表内，JSON `components` 中保留全部。")
    lines.append("")
    lines.append("| PDF页 | 位号 | Value/型号 | 库 | 封装 | 图纸 | 类型 | DNP |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in stats["components"]:
        if c["is_power_symbol"]:
            continue
        lines.append(
            f"| {c['page_no']} | {_escape_md(c['ref'])} | {_escape_md(c['value'])} | "
            f"{_escape_md(c['lib_id'])} | {_escape_md(c['footprint'])} | `{c['sheet_path']}` | "
            f"{c['kind']} | {'yes' if c['dnp'] else ''} |"
        )
    lines.append("")

    lines.append("## 2. 网络清单（按名称）")
    lines.append("")
    lines.append("> 说明：同一网络的层次/全局端口别名并入同一行（例如 ADC_VREFIN 可能并入 /5V_VREF）；"
                 "JSON `nets[].hierarchical_names/aliases` 保留全部别名。")
    lines.append("")
    lines.append("| 网络 | 类型 | 别名/层次端口 | PDF页 | 引脚数 | 所在图纸 | 引脚示例 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for net in sorted(netlist, key=lambda n: (n.name,)):
        example = ", ".join(f"{p.ref}.{p.pin_number}" for p in net.pins[:6])
        if len(net.pins) > 6:
            example += ", …"
        aliases = _net_alias_list(net)
        pages = sorted({page_map.get(p, 0) for p in net.unique_sheet_paths()})
        lines.append(
            f"| {_escape_md(net.name)} | {_net_kind(net)} | {_escape_md(', '.join(aliases[:8]))} | "
            f"{', '.join(str(x) for x in pages)} | {net.pin_count()} | "
            f"{', '.join(net.unique_sheet_paths()[:4])} | {example} |"
        )
    lines.append("")
    lines.append("### 网络连接明细（全量，供逐条核对）")
    lines.append("")
    lines.append("| 网络 | PDF页 | 类型 | 连接点（ref.pin） |")
    lines.append("| --- | --- | --- | --- |")
    for net in sorted(netlist, key=lambda n: (n.name,)):
        pages = sorted({page_map.get(p, 0) for p in net.unique_sheet_paths()})
        pins = ", ".join(f"{p.ref}.{p.pin_number}" for p in net.pins)
        lines.append(f"| {_escape_md(net.name)} | {', '.join(str(x) for x in pages)} | "
                     f"{_net_kind(net)} | {pins or '—'} |")
    lines.append("")
    lines.append("### 电源网络去耦统计（按 power_in 引脚所在网络）")
    lines.append("")
    lines.append("| 电源网络 | PDF页 | power_in 引脚 | 电容数 | 电容位号 | 判定 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for rail in stats["power_rails"]:
        lines.append(
            f"| {_escape_md(rail['name'])} | {', '.join(str(x) for x in rail['page_nos'])} | "
            f"{_escape_md(', '.join(rail['power_pins']))} | {rail['cap_count']} | "
            f"{_escape_md(', '.join(rail['caps'][:20]))} | "
            f"{'OK' if rail['decoupled'] else '未发现电容'} |"
        )
    lines.append("")

    lines.append("## 3. 设计审查发现")
    lines.append("")
    if not issues:
        lines.append("未发现问题。")
    for sev, label in (("error", "错误"), ("warning", "警告"), ("info", "提示")):
        sev_issues = [i for i in issues if i.severity == sev]
        if not sev_issues:
            continue
        lines.append(f"### {label}（{len(sev_issues)}）")
        lines.append("")
        lines.append("| # | PDF页 | 位置 | 代码 | 说明 | 网络 | 依据 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for idx, issue in enumerate(sev_issues, 1):
            location = issue.sheet_path
            if issue.ref:
                location += f" / {issue.ref}"
                if issue.pin:
                    location += f".{issue.pin}"
            lines.append(
                f"| {idx} | {page_map.get(issue.sheet_path, 0)} | `{location}` | {issue.code} | "
                f"{_escape_md(issue.message)} | {_escape_md(issue.net)} | {issue.evidence} |"
            )
        lines.append("")
    if extra_notes:
        lines.append("## 4. 工具与方法说明")
        lines.append("")
        for note in extra_notes:
            lines.append(f"- {note}")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_json(path, project: Project, netlist: List[Net], issues: List[Issue],
               erc_summary: Optional[dict] = None) -> None:
    stats = project_stats(project, netlist, issues)
    payload = {
        "stats": stats,
        "sheets": stats["sheets"],
        "components": stats["components"],
        "power_rails": stats["power_rails"],
        "issues": [
            {
                "code": i.code,
                "severity": i.severity,
                "title": i.title,
                "message": i.message,
                "sheet_path": i.sheet_path,
                "ref": i.ref,
                "pin": i.pin,
                "net": i.net,
                "details": i.details,
                "evidence": i.evidence,
            }
            for i in issues
        ],
        "nets": [
            {
                "name": n.name,
                "kind": _net_kind(n),
                "aliases": _net_alias_list(n),
                "page_nos": sorted({_page_map(project).get(p, 0) for p in n.unique_sheet_paths()}),
                "sheet_paths": n.sheet_paths,
                "conflict": n.has_conflict,
                "conflict_names": n.conflict_names,
                "pins": [
                    {
                        "ref": p.ref,
                        "pin": p.pin_number,
                        "pin_name": p.pin_name,
                        "pin_type": p.pin_type,
                        "sheet_path": p.sheet_path,
                        "lib_id": p.lib_id,
                        "value": p.value,
                        "footprint": p.footprint,
                    }
                    for p in n.pins
                ],
                "labels": n.labels,
                "global_names": n.global_names,
                "hierarchical_names": n.hierarchical_names,
                "power_names": n.power_names,
            }
            for n in netlist
        ],
    }
    if erc_summary:
        payload["erc_summary"] = erc_summary
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
