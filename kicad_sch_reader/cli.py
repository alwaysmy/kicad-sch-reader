"""Command-line interface for kicad-sch-reader.

Usage examples::

    python kicad-sch-reader.py review D:\\path\\to\\project
    python kicad-sch-reader.py components project --json
    python kicad-sch-reader.py trace U1 project --no-power --depth 3
    python kicad-sch-reader.py netfind +15V project
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from . import connectivity, kicad_cli, parser, report, rules
from .model import Issue, Net, Project


def _setup_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _print_json(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def _project(args) -> Project:
    return parser.load_project(args.input)


def _netlist(project: Project) -> List[Net]:
    return connectivity.build_netlist(project)


def cmd_parse(args) -> None:
    project = _project(args)
    netlist = _netlist(project)
    stats = report.project_stats(project, netlist, [])
    if args.json:
        _print_json(stats)
        return
    print(f"project: {stats['root']}")
    print(f"sheets: {stats['sheet_count']}  symbols: {stats['symbol_count']}  nets: {stats['net_count']}")
    for s in stats["sheets"]:
        print(f"  {s['path']:24s} {Path(s['file']).name:48s} {s['title']}  "
              f"sym={s['symbols']} wires={s['wires']} labels={s['labels']} nc={s['no_connects']}")


def cmd_sheets(args) -> None:
    project = _project(args)
    rows = []
    for path in project.sheet_order:
        sheet = project.sheets[path]
        row = {
            "path": path,
            "file": str(sheet.file),
            "title": sheet.title,
            "title_fields": dict(sheet.title_fields),
            "version": sheet.version,
            "generator": sheet.generator,
            "symbols": len(sheet.symbols),
            "wires": len(sheet.wires),
            "labels": len(sheet.labels),
            "junctions": len(sheet.junctions),
            "no_connects": len(sheet.no_connects),
            "hierarchical_sheets": [
                {"name": r.name, "file": r.file, "path": r.first_path, "pins": len(r.pins)}
                for r in sheet.sheets
            ],
        }
        rows.append(row)
        if not args.json:
            print(f"{path:24s} {Path(sheet.file).name:48s} {sheet.title}")
            tb = sheet.title_fields
            extras = [f"{k}={tb[k]}" for k in ("date", "rev", "company") if tb.get(k)]
            if extras:
                print(f"    title_block: {'; '.join(extras)}")
            for r in sheet.sheets:
                print(f"    sheet {r.name} -> {r.file} ({r.first_path})")
    if args.json:
        _print_json(rows)


def cmd_texts(args) -> None:
    """导出各页自由文本注释（设计说明/注意事项），供设计意图审查对照。

    文本内容是否与电路一致需人工或 LLM 对照器件手册核实——本命令只负责
    把"审查对象"完整捞出来，不做自动判定。
    """
    project = _project(args)
    needle = getattr(args, "filter", "") or ""
    rows = []
    for path in project.sheet_order:
        sheet = project.sheets[path]
        for t in sheet.texts:
            if needle and needle.lower() not in t.content.lower():
                continue
            row = {
                "sheet_path": path,
                "kind": t.kind,
                "content": t.content,
                "pos": [round(t.pos[0], 4), round(t.pos[1], 4)],
                "rotation": t.rotation,
            }
            if t.kind == "textbox":
                row["size"] = [round(t.size[0], 4), round(t.size[1], 4)]
            rows.append(row)
            if not args.json:
                content = t.content.replace("\n", "\\n")
                if len(content) > 90:
                    content = content[:90] + "…"
                print(f"{path:24s} [{t.kind:7s}] ({t.pos[0]:8.2f},{t.pos[1]:8.2f}) {content}")
    if args.json:
        _print_json(rows)


def cmd_components(args) -> None:
    project = _project(args)
    rows = []
    for sym in project.all_symbols():
        if args.filter and args.filter.lower() not in sym.ref.lower() \
                and args.filter.lower() not in sym.value.lower() \
                and args.filter.lower() not in sym.lib_id.lower():
            continue
        row = {
            "ref": sym.ref,
            "value": sym.value,
            "lib_id": sym.lib_id,
            "footprint": sym.footprint,
            "sheet_path": sym.sheet_path,
            "unit": sym.unit,
            "dnp": sym.dnp,
            "in_bom": sym.in_bom,
            "on_board": sym.on_board,
            "pins": len(sym.pins),
            "uuid": sym.uuid,
        }
        rows.append(row)
        if not args.json:
            print(f"{sym.sheet_path:28s} {sym.ref:12s} {sym.value:16s} {sym.lib_id:42s} "
                  f"{sym.footprint:36s} pins={len(sym.pins)} {'DNP' if sym.dnp else ''}")
    if args.json:
        _print_json(rows)


def cmd_pins(args) -> None:
    project = _project(args)
    netlist = _netlist(project)
    pin_net = {
        (p.sheet_path, p.ref, p.pin_number): n.name
        for n in netlist for p in n.pins
    }
    rows = []
    for sym in project.all_symbols():
        if args.ref and sym.ref.lower() != args.ref.lower():
            continue
        for pin in sym.pins:
            net = pin_net.get((sym.sheet_path, sym.ref, pin.number))
            row = {
                "sheet_path": sym.sheet_path,
                "ref": sym.ref,
                "pin": pin.number,
                "pin_name": pin.name,
                "pin_type": pin.electrical_type,
                "net": net,
                "no_connect": pin.no_connect,
                "pos": [round(pin.pos[0], 4), round(pin.pos[1], 4)],
            }
            rows.append(row)
            if not args.json:
                nc = "NC" if pin.no_connect else (net or "<floating>")
                print(f"{sym.sheet_path:28s} {sym.ref:12s}.{pin.number:4s} "
                      f"{pin.name:8s} {pin.electrical_type:12s} -> {nc}")
    if args.json:
        _print_json(rows)


def cmd_bridges(args) -> None:
    """导出两脚中间器件桥接对（排阻 Rk.1/Rk.2、0Ω、磁珠等）。

    不自动合并网络；输出两侧网络与 direct 标记，供脚本或 LLM 判断。
    """
    project = _project(args)
    netlist = _netlist(project)
    pin_net = {
        (p.sheet_path, p.ref, p.pin_number): n.name
        for n in netlist for p in n.pins
    }
    rows = []
    by_ref: Dict[str, list] = defaultdict(list)
    for sym in project.all_symbols():
        if sym.ref and not sym.ref.startswith("#"):
            by_ref[sym.ref].append(sym)
    for ref, syms in by_ref.items():
        pins = {}
        for sym in syms:
            for pin in sym.pins:
                key = (sym.sheet_path, pin.number)
                pins[key] = {"number": pin.number, "name": pin.name,
                             "sheet": sym.sheet_path,
                             "net": pin_net.get((sym.sheet_path, sym.ref, pin.number))}
        items = list(pins.values())
        direct = bool(re.search(r"0000|0R|0Ω", str(syms[0].value), re.I))
        lib_id = syms[0].lib_id or ""

        def add_row(a, b, channel=None):
            rows.append({
                "ref": ref,
                "lib_id": lib_id,
                "value": syms[0].value,
                "sheet_path": syms[0].sheet_path,
                "pin_a": a["number"], "pin_a_name": a["name"], "net_a": a["net"],
                "pin_b": b["number"], "pin_b_name": b["name"], "net_b": b["net"],
                "direct": direct,
                **({"channel": channel} if channel else {}),
            })

        if len(items) == 2:
            add_row(items[0], items[1])
            continue
        # R_Pack：pin name 形如 R1.1/R1.2 ...，按通道配对输出。
        if "r_pack" in lib_id.lower() or any(
            re.match(r"R\d+\.([12])$", str(p["name"] or "")) for p in items
        ):
            sides: Dict[int, dict] = defaultdict(dict)
            for p in items:
                m = re.match(r"R(\d+)\.([12])$", str(p["name"] or ""))
                if m:
                    sides[int(m.group(1))][m.group(2)] = p
            for channel in sorted(sides):
                if "1" in sides[channel] and "2" in sides[channel]:
                    add_row(sides[channel]["1"], sides[channel]["2"], channel=channel)

    rows.sort(key=lambda r: (not r["direct"], r["ref"], str(r.get("channel") or 0)))
    if args.json:
        _print_json(rows)
        return
    for r in rows:
        tag = "direct" if r["direct"] else "passive"
        print(f"{r['ref']:8s} {r['pin_a']:>3s}({r['pin_a_name'] or ''})={r['net_a'] or '<float>'} "
              f"<-> {r['pin_b']:>3s}({r['pin_b_name'] or ''})={r['net_b'] or '<float>'}  [{tag}]")


def cmd_nets(args) -> None:
    project = _project(args)
    netlist = _netlist(project)
    rows = []
    for net in netlist:
        if args.name and args.name.lower() not in net.name.lower():
            continue
        if args.sheet and not any(p.sheet_path == args.sheet for p in net.pins):
            continue
        row = {
            "name": net.name,
            "pin_count": net.pin_count(),
            "sheet_paths": net.sheet_paths,
            "pins": [f"{p.ref}.{p.pin_number}" for p in net.pins],
            "labels": net.labels,
            "global_names": net.global_names,
            "power_names": net.power_names,
            "hierarchical_names": net.hierarchical_names,
            "conflict": net.has_conflict,
        }
        rows.append(row)
        if not args.json:
            members = ", ".join(f"{p.ref}.{p.pin_number}" for p in net.pins[:12])
            if len(net.pins) > 12:
                members += f", …(+{len(net.pins) - 12})"
            print(f"{net.name:24s} pins={net.pin_count():3d} sheets={','.join(net.unique_sheet_paths()):32s} {members}")
    if args.json:
        _print_json(rows)


def cmd_netfind(args) -> None:
    project = _project(args)
    netlist = _netlist(project)
    if getattr(args, "exact", False):
        matches = [n for n in netlist if n.name.lower() == args.name.lower()]
    else:
        matches = [n for n in netlist if args.name.lower() in n.name.lower()]
    if args.json:
        _print_json([
            {
                "name": n.name,
                "pins": [
                    {
                        "sheet_path": p.sheet_path,
                        "ref": p.ref,
                        "pin": p.pin_number,
                        "pin_name": p.pin_name,
                        "lib_id": p.lib_id,
                        "value": p.value,
                    }
                    for p in n.pins
                ],
                "power_names": n.power_names,
                "conflict": n.has_conflict,
            }
            for n in matches
        ])
        return
    for net in matches:
        print(f"== {net.name} ==")
        for p in net.pins:
            print(f"  {p.sheet_path:28s} {p.ref}.{p.pin_number}  {p.lib_id}  {p.value}")


def cmd_find(args) -> None:
    project = _project(args)
    rows = []
    for sym in project.all_symbols():
        if sym.ref.lower() != args.ref.lower():
            continue
        row = {
            "sheet_path": sym.sheet_path,
            "ref": sym.ref,
            "value": sym.value,
            "lib_id": sym.lib_id,
            "footprint": sym.footprint,
            "dnp": sym.dnp,
            "pins": [
                {"pin": p.number, "name": p.name, "type": p.electrical_type}
                for p in sym.pins
            ],
        }
        rows.append(row)
        if not args.json:
            print(f"{sym.sheet_path} {sym.ref} {sym.value} {sym.lib_id} {sym.footprint}")
    if args.json:
        _print_json(rows)


def _is_power_net(net: Net, extra_patterns=None) -> bool:
    # 优先使用结构证据而不是名字猜测：电源符号、电源引脚。
    if net.power_names:
        return True
    if any(p.pin_type.lower() in ("power_in", "power_out") for p in net.pins):
        return True
    if any(p.ref.startswith("#PWR") for p in net.pins):
        return True
    if re.match(r"^(GND|AGND|DGND|VCC|VDD|VSS|VBUS|PWR_|VREF|REF|\+?-?\d+(\.\d+)?V[A-Z0-9_]*)$",
                net.name, re.IGNORECASE):
        return True
    for pattern in (extra_patterns or []):
        try:
            if re.search(pattern, net.name, re.IGNORECASE):
                return True
        except re.error:
            continue
    return False


def cmd_trace(args) -> None:
    project = _project(args)
    netlist = _netlist(project)
    ref_net: Dict[str, List[Net]] = defaultdict(list)
    for net in netlist:
        for p in net.pins:
            if p.ref:
                ref_net[p.ref].append(net)
    start_refs = [r for r in ref_net if r.lower() == args.ref.lower()]
    if not start_refs:
        print(f"未找到位号 {args.ref}")
        return
    edges = []
    reached = set(start_refs)
    queue = deque((r, 0) for r in start_refs)
    visited_nets = set()
    max_depth = args.depth
    while queue:
        ref, depth = queue.popleft()
        for net in ref_net.get(ref, []):
            if args.no_power and _is_power_net(net, getattr(args, "power_net", None)):
                continue
            if id(net) in visited_nets:
                continue
            visited_nets.add(id(net))
            for p in net.pins:
                if not p.ref:
                    continue
                edge = {"from": ref, "net": net.name, "to": p.ref, "sheet_path": p.sheet_path}
                if edge not in edges:
                    edges.append(edge)
                if p.ref not in reached:
                    reached.add(p.ref)
                    if depth + 1 < max_depth:
                        queue.append((p.ref, depth + 1))
    if args.json:
        _print_json({"start": start_refs, "reached": sorted(reached), "edges": edges})
        return
    print(f"trace {args.ref}: reached {len(reached)} components")
    for e in edges:
        print(f"  {e['from']:12s} --[{e['net']}]--> {e['to']}  ({e['sheet_path']})")


def _erc_summary_dict(markers: List[dict]) -> dict:
    counts: Dict[str, int] = defaultdict(int)
    for m in markers:
        counts[str(m.get("severity", "unknown"))] += 1
    return dict(counts)


def cmd_review(args) -> None:
    project = _project(args)
    netlist = _netlist(project)
    markers: List[dict] = []
    erc_note = None
    if not args.no_erc:
        try:
            markers = kicad_cli.run_erc(project.root_sheet.file)
            erc_note = f"KiCad ERC 已运行: {_erc_summary_dict(markers)}"
        except Exception as exc:  # pragma: no cover - depends on local KiCad install
            erc_note = f"KiCad ERC 未运行（{type(exc).__name__}: {exc}）"
    issues = rules.run_all_checks(project, netlist, markers)

    name = project.root.parent.name or project.root_sheet.file.stem
    out_md = args.out_md or str(Path.cwd() / f"{name}.review.md")
    out_json = args.out_json or str(Path(out_md).with_suffix(".json"))
    notes = [
        "网络表由纯 Python 几何连通域构建（导线端点 + 连接点 + 标签 + 电源符号），并完成分层图纸与全局标签合并。",
        "悬空/单引脚等判定基于本工具解析结果；KiCad ERC 结果（如已运行）以 ERC-* 代码单独列出。",
        "报告中的 info 级发现需要人工结合设计意图判断，不代表设计错误。",
    ]
    if erc_note:
        notes.insert(1, erc_note)
    report.write_markdown(out_md, project, netlist, issues, erc_summary=_erc_summary_dict(markers) if markers else None,
                          extra_notes=notes)
    report.write_json(out_json, project, netlist, issues,
                      erc_summary=_erc_summary_dict(markers) if markers else None)
    counts = rules.severity_counts(issues)
    print(f"review done: issues={len(issues)} ({counts})")
    print(f"markdown: {out_md}")
    print(f"json:     {out_json}")
    if args.json:
        _print_json({"issues": len(issues), "counts": counts, "markdown": str(out_md), "json": str(out_json)})


def cmd_erc(args) -> None:
    root_sch = parser.resolve_root_file(args.input)
    out = args.out or str(Path(root_sch).with_suffix(".erc.json"))
    markers = kicad_cli.run_erc(root_sch, output_json=out)
    if args.json:
        _print_json({"output": out, "counts": _erc_summary_dict(markers), "markers": markers})
        return
    print(f"ERC markers: {len(markers)} {_erc_summary_dict(markers)}")
    print(f"json: {out}")
    for m in markers[:50]:
        print(f"  [{m.get('severity', '?')}] {m.get('type', '')}: {str(m.get('description', ''))[:160]}")


def cmd_export_netlist(args) -> None:
    root_sch = parser.resolve_root_file(args.input)
    path = kicad_cli.export_netlist(root_sch, output_file=args.out, fmt=args.format)
    print(f"netlist: {path}")


def cmd_export_bom(args) -> None:
    root_sch = parser.resolve_root_file(args.input)
    path = kicad_cli.export_bom(root_sch, output_file=args.out)
    print(f"bom: {path}")


def cmd_link_check(args) -> None:
    """Find candidate connector pairs between two KiCad projects.

    Same net name on both sides is only a *candidate* proof of board-to-board
    connectivity; the physical connector choice is design knowledge.
    """
    project_a = _project_named(args.input_a)
    project_b = _project_named(args.input_b)
    netlist_a = _netlist(project_a)
    netlist_b = _netlist(project_b)

    def connector_map(project, netlist):
        out = {}
        for sym in project.all_symbols():
            is_connector = ("connector" in sym.lib_id.lower() or "conn" in sym.lib_id.lower()) \
                and "testpoint" not in sym.lib_id.lower()
            if not is_connector and not (sym.ref and sym.ref[0] in "JPH" and len(sym.pins) >= 2):
                continue
            if not sym.ref or sym.ref.startswith("#"):
                continue
            pins = {}
            for pin in sym.pins:
                net = next((n.name for n in netlist if any(
                    p.ref == sym.ref and p.pin_number == pin.number for p in n.pins)), "")
                pins[pin.number] = net or None
            connected = {k: v for k, v in pins.items() if v}
            if connected:
                out[sym.ref] = {
                    "ref": sym.ref,
                    "lib_id": sym.lib_id,
                    "sheet": sym.sheet_path,
                    "pin_count": len(sym.pins),
                    "pins": pins,
                    "connected_count": len(connected),
                }
        return out

    ca = connector_map(project_a, netlist_a)
    cb = connector_map(project_b, netlist_b)
    rows = []
    for ref_a, a in sorted(ca.items()):
        for ref_b, b in sorted(cb.items()):
            common_pins = sorted(set(a["pins"]) & set(b["pins"]))
            if not common_pins:
                continue
            exact = 0
            diffs = []
            for pin in common_pins:
                if a["pins"].get(pin) and a["pins"][pin] == b["pins"][pin]:
                    exact += 1
                else:
                    diffs.append((pin, a["pins"].get(pin), b["pins"].get(pin)))
            rows.append({
                "a_ref": ref_a, "a_lib": a["lib_id"], "a_sheet": a["sheet"],
                "b_ref": ref_b, "b_lib": b["lib_id"], "b_sheet": b["sheet"],
                "common_pins": len(common_pins),
                "exact_pins": exact,
                "diff_count": len(diffs),
                "diffs": [{"pin": d[0], "a_net": d[1], "b_net": d[2]} for d in diffs[:12]],
            })
    rows.sort(key=lambda r: (-r["exact_pins"], -r["common_pins"], r["a_ref"], r["b_ref"]))
    if args.json:
        _print_json({"project_a": str(project_a.root), "project_b": str(project_b.root),
                     "connector_pairs": rows})
        return
    print(f"A: {project_a.root}")
    print(f"B: {project_b.root}")
    print("")
    if not rows:
        print("未找到可比较的连接器对")
        return
    for r in rows:
        mark = "√" if r["diff_count"] == 0 and r["exact_pins"] >= 2 else "?"
        print(f"[{mark}] {r['a_ref']} ({r['a_lib']}, {r['a_sheet']}) <-> "
              f"{r['b_ref']} ({r['b_lib']}, {r['b_sheet']})  "
              f"exact={r['exact_pins']}/{r['common_pins']} diff={r['diff_count']}")
        for d in r["diffs"][:5]:
            print(f"      pin {d['pin']}: {d['a_net']} != {d['b_net']}")


def _project_named(path):
    return parser.load_project(path)


def cmd_validate(args) -> None:
    """Smoke-test the reader on a project and report structural invariants."""
    project = _project(args)
    netlist = _netlist(project)
    issues = rules.run_all_checks(project, netlist)
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    ok = len(errors) == 0
    result = {
        "ok": ok,
        "root": str(project.root),
        "sheets": len(project.sheets),
        "symbols": len(project.all_symbols()),
        "nets": len(netlist),
        "pin_connections": sum(len(n.pins) for n in netlist),
        "errors": len(errors),
        "warnings": len(warnings),
        "issues": len(issues),
    }
    if args.json:
        _print_json(result)
        return
    print(f"validate: {'PASS' if ok else 'FAIL'} {result}")
    if errors:
        for i in errors[:20]:
            print(f"  ERROR {i.code} {i.message}")


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="kicad-sch-reader", description="KiCad schematic reader and design-review tool")
    ap.add_argument("--json", action="store_true", help="emit structured JSON where supported")
    ap.add_argument("--kicad-cli", dest="kicad_cli_path", help="path to kicad-cli executable")
    sub = ap.add_subparsers(dest="command", required=True)

    def add_input(p, help_text="KiCad 工程目录或根 .kicad_sch 文件"):
        p.add_argument("input", help=help_text)

    def add_json(p):
        p.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="emit structured JSON")

    p = sub.add_parser("parse", help="解析工程并输出结构统计")
    add_json(p)
    add_input(p)
    p.set_defaults(func=cmd_parse)

    p = sub.add_parser("sheets", help="列出图纸与分层结构")
    add_json(p)
    add_input(p)
    p.set_defaults(func=cmd_sheets)

    p = sub.add_parser("texts", help="导出页内自由文本注释（设计意图审查用）")
    add_json(p)
    add_input(p)
    p.add_argument("filter", nargs="?", default="", help="按文本内容过滤")
    p.set_defaults(func=cmd_texts)

    p = sub.add_parser("components", help="列出元件")
    add_json(p)
    add_input(p)
    p.add_argument("filter", nargs="?", default="", help="按位号/值/库ID过滤")
    p.set_defaults(func=cmd_components)

    p = sub.add_parser("pins", help="引脚级网络表")
    add_json(p)
    add_input(p)
    p.add_argument("ref", nargs="?", default="", help="仅显示某位号")
    p.set_defaults(func=cmd_pins)

    p = sub.add_parser("bridges", help="导出两脚中间器件桥接对（排阻/0Ω/磁珠等）")
    add_json(p)
    add_input(p)
    p.set_defaults(func=cmd_bridges)

    p = sub.add_parser("nets", help="项目网络清单")
    add_json(p)
    add_input(p)
    p.add_argument("name", nargs="?", default="", help="按网络名过滤")
    p.add_argument("--sheet", default="", help="按图纸路径过滤")
    p.set_defaults(func=cmd_nets)

    p = sub.add_parser("netfind", help="按名称查找网络及其全部引脚")
    add_json(p)
    add_input(p)
    p.add_argument("name")
    p.add_argument("--exact", action="store_true",
                   help="精确匹配网络名（推荐用于 N$xxx 未命名网络）")
    p.set_defaults(func=cmd_netfind)

    p = sub.add_parser("find", help="按位号反查元件")
    add_json(p)
    add_input(p)
    p.add_argument("ref")
    p.set_defaults(func=cmd_find)

    p = sub.add_parser("trace", help="从位号出发沿网络做 BFS 链路追踪")
    add_json(p)
    add_input(p)
    p.add_argument("ref")
    p.add_argument("--depth", type=int, default=4)
    p.add_argument("--no-power", action="store_true", help="跳过电源/地网络")
    p.add_argument("--power-net", action="append", default=[], help="补充电源网络命名正则")
    p.set_defaults(func=cmd_trace)

    p = sub.add_parser("review", help="运行设计审查并生成 Markdown/JSON 报告")
    add_json(p)
    add_input(p)
    p.add_argument("--out-md", default="")
    p.add_argument("--out-json", default="")
    p.add_argument("--no-erc", action="store_true", help="不调用 kicad-cli ERC")
    p.set_defaults(func=cmd_review)

    p = sub.add_parser("erc", help="调用 kicad-cli 执行 ERC")
    add_json(p)
    add_input(p)
    p.add_argument("-o", "--out", default="")
    p.set_defaults(func=cmd_erc)

    p = sub.add_parser("export-netlist", help="用 kicad-cli 导出官方网表")
    add_json(p)
    add_input(p)
    p.add_argument("-o", "--out", default="")
    p.add_argument("--format", default="kicadsexpr")
    p.set_defaults(func=cmd_export_netlist)

    p = sub.add_parser("export-bom", help="用 kicad-cli 导出 BOM CSV")
    add_json(p)
    add_input(p)
    p.add_argument("-o", "--out", default="")
    p.set_defaults(func=cmd_export_bom)

    p = sub.add_parser("validate", help="解析冒烟测试（结构不变量检查）")
    add_json(p)
    add_input(p)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("link-check", help="两个工程间连接器对候选核对")
    add_json(p)
    p.add_argument("input_a")
    p.add_argument("input_b")
    p.set_defaults(func=cmd_link_check)
    return ap


def main(argv: Optional[List[str]] = None) -> int:
    _setup_stdout()
    ap = build_arg_parser()
    args = ap.parse_args(argv)
    if getattr(args, "kicad_cli_path", None):
        os.environ["KICAD_CLI"] = args.kicad_cli_path
    try:
        args.func(args)
        return 0
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
