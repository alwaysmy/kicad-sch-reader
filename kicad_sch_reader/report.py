"""Markdown / JSON review-report writers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .model import Issue, Net, Project
from .rules import severity_counts


def project_stats(project: Project, netlist: List[Net], issues: List[Issue]) -> dict:
    symbols = project.all_symbols()
    return {
        "root": str(project.root),
        "sheet_count": len(project.sheets),
        "sheets": [
            {
                "path": p,
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
        lines.append(f"| KiCad ERC | {erc_summary} |")
    lines.append("")
    lines.append("### 图纸清单")
    lines.append("")
    lines.append("| 路径 | 文件 | 标题 | 元件 | 导线 | 标签 | 连接点 | NC | 版本/生成器 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for s in stats["sheets"]:
        lines.append(
            f"| `{s['path']}` | `{Path(s['file']).name}` | {_escape_md(s['title'])} | {s['symbols']} | "
            f"{s['wires']} | {s['labels']} | {s['junctions']} | {s['no_connects']} | "
            f"{s['version']} / {s['generator']} |"
        )
    lines.append("")

    lines.append("## 2. 网络清单（按名称）")
    lines.append("")
    lines.append("| 网络 | 引脚数 | 所在图纸 | 引脚示例 |")
    lines.append("| --- | --- | --- | --- |")
    for net in sorted(netlist, key=lambda n: (n.name,)):
        example = ", ".join(f"{p.ref}.{p.pin_number}" for p in net.pins[:6])
        if len(net.pins) > 6:
            example += ", …"
        lines.append(
            f"| {_escape_md(net.name)} | {net.pin_count()} | {', '.join(net.unique_sheet_paths()[:4])} | {example} |"
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
        lines.append("| # | 位置 | 代码 | 说明 | 网络 | 依据 |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for idx, issue in enumerate(sev_issues, 1):
            location = issue.sheet_path
            if issue.ref:
                location += f" / {issue.ref}"
                if issue.pin:
                    location += f".{issue.pin}"
            lines.append(
                f"| {idx} | `{location}` | {issue.code} | {_escape_md(issue.message)} "
                f"| {_escape_md(issue.net)} | {issue.evidence} |"
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
                "power_names": n.power_names,
            }
            for n in netlist
        ],
    }
    if erc_summary:
        payload["erc_summary"] = erc_summary
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
