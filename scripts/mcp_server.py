#!/usr/bin/env python3
"""MCP (Model Context Protocol) stdio server wrapping kicad-sch-reader.

Exposes the KiCad/LCEDA review query surface as MCP tools so opencode (or
any MCP client) can run deterministic schematic extraction directly.

Zero third-party dependencies: implements the minimal JSON-RPC 2.0 + MCP
stdio framing (newline-delimited JSON) by hand.

Install: add to opencode.json under mcp::

    "kicad-sch-reader": {
      "type": "local",
      "command": ["python", "D:\\MyProjects\\AI\\schematics_review_tool\\scripts\\mcp_server.py"],
      "enabled": true
    }

Self-test (also used by the installer)::

    python scripts/mcp_server.py --selftest
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE / "repos" / "lceda-sch-reader"))

from kicad_sch_reader import connectivity, parser, rules  # noqa: E402
from kicad_sch_reader.circuit_ir import board_from_kicad, diff_boards  # noqa: E402


# ---------------------------------------------------------------- tool impls

def _tool_parse(project: str) -> dict:
    p = parser.load_project(project)
    nl = connectivity.build_netlist(p)
    from kicad_sch_reader.report import project_stats
    return project_stats(p, nl, [])


def _tool_review(project: str, no_erc: bool = True, config: str = "") -> dict:
    p = parser.load_project(project)
    nl = connectivity.build_netlist(p)
    markers = []
    if not no_erc:
        try:
            from kicad_sch_reader import kicad_cli
            markers = kicad_cli.run_erc(p.root_sheet.file)
        except Exception as exc:
            markers = [{"severity": "info", "type": "ERC-BYPASS",
                        "description": f"kicad-cli unavailable: {exc}"}]
    cfg = rules.load_config(config) if config else None
    issues = rules.run_all_checks(p, nl, markers, config=cfg)
    return {
        "project": str(p.root),
        "issues": [
            {
                "code": i.code, "severity": i.severity, "title": i.title,
                "message": i.message, "sheet_path": i.sheet_path,
                "ref": i.ref, "pin": i.pin, "net": i.net, "evidence": i.evidence,
            }
            for i in issues
        ],
    }


def _tool_texts(project: str, filter: str = "") -> dict:
    needle = (filter or "").lower()
    p = parser.load_project(project)
    rows = []
    for path in p.sheet_order:
        sheet = p.sheets[path]
        for t in sheet.texts:
            if needle and needle not in t.content.lower():
                continue
            rows.append({
                "sheet_path": path, "kind": t.kind, "content": t.content,
                "pos": [round(t.pos[0], 4), round(t.pos[1], 4)],
                "rotation": t.rotation,
            })
    return {"count": len(rows), "texts": rows}


def _tool_nets(project: str, name: str = "") -> dict:
    p = parser.load_project(project)
    nl = connectivity.build_netlist(p)
    needle = (name or "").lower()
    rows = []
    for net in nl:
        if needle and needle not in net.name.lower():
            continue
        rows.append({
            "name": net.name, "pin_count": net.pin_count(),
            "sheets": net.unique_sheet_paths(),
            "pins": [f"{pin.ref}.{pin.pin_number}" for pin in net.pins],
            "conflict": net.has_conflict,
        })
    return {"count": len(rows), "nets": rows}


def _tool_netfind(project: str, name: str, exact: bool = False) -> dict:
    p = parser.load_project(project)
    nl = connectivity.build_netlist(p)
    needle = name.lower()
    rows = []
    for net in nl:
        if exact:
            matched = net.name.lower() == needle
        else:
            matched = needle in net.name.lower()
        if not matched:
            continue
        rows.append({
            "name": net.name, "power_names": net.power_names,
            "conflict": net.has_conflict,
            "pins": [
                {
                    "sheet_path": pin.sheet_path, "ref": pin.ref,
                    "pin": pin.pin_number, "pin_name": pin.pin_name,
                    "pin_type": pin.pin_type, "lib_id": pin.lib_id,
                    "value": pin.value,
                }
                for pin in net.pins
            ],
        })
    return {"count": len(rows), "nets": rows}


def _tool_trace(project: str, ref: str, depth: int = 4, no_power: bool = False) -> dict:
    p = parser.load_project(project)
    nl = connectivity.build_netlist(p)
    from collections import defaultdict, deque
    ref_net = defaultdict(list)
    for net in nl:
        for pin in net.pins:
            if pin.ref:
                ref_net[pin.ref].append(net)

    def is_power(net) -> bool:
        if net.power_names:
            return True
        if any(pin.pin_type.lower() in ("power_in", "power_out") for pin in net.pins):
            return True
        if any(pin.ref.startswith("#PWR") for pin in net.pins):
            return True
        import re
        return bool(re.match(r"^(GND|AGND|DGND|VCC|VDD|VSS|VBUS|VREF|\+?-?\d+(\.\d+)?V[A-Z0-9_]*)$",
                             net.name, re.IGNORECASE))

    starts = [r for r in ref_net if r.lower() == ref.lower()]
    if not starts:
        return {"error": f"未找到位号 {ref}"}
    edges = []
    reached = set(starts)
    queue = deque((r, 0) for r in starts)
    visited = set()
    while queue:
        node, depth_i = queue.popleft()
        for net in ref_net.get(node, []):
            if no_power and is_power(net):
                continue
            if id(net) in visited:
                continue
            visited.add(id(net))
            for pin in net.pins:
                if not pin.ref:
                    continue
                edge = {"from": node, "net": net.name, "to": pin.ref, "sheet": pin.sheet_path}
                if edge not in edges:
                    edges.append(edge)
                if pin.ref not in reached:
                    reached.add(pin.ref)
                    if depth_i + 1 < depth:
                        queue.append((pin.ref, depth_i + 1))
    return {"start": starts, "reached": sorted(reached), "edges": edges}


def _tool_components(project: str, filter: str = "") -> dict:
    p = parser.load_project(project)
    needle = (filter or "").lower()
    rows = []
    for sym in p.all_symbols():
        if needle and needle not in sym.ref.lower() \
                and needle not in sym.value.lower() \
                and needle not in sym.lib_id.lower():
            continue
        rows.append({
            "ref": sym.ref, "value": sym.value, "lib_id": sym.lib_id,
            "footprint": sym.footprint, "sheet_path": sym.sheet_path,
            "unit": sym.unit, "dnp": sym.dnp, "in_bom": sym.in_bom,
            "pins": len(sym.pins),
        })
    return {"count": len(rows), "components": rows}


def _tool_diff(project_a: str, project_b: str) -> dict:
    pa = parser.load_project(project_a)
    pb = parser.load_project(project_b)
    return diff_boards(
        board_from_kicad(pa, name=Path(project_a).name),
        board_from_kicad(pb, name=Path(project_b).name),
    )


def _tool_lceda_review(epro: str, board_name: str = "",
                       trace_nets: List[str] = None,
                       trace_refs: List[str] = None) -> dict:
    import tempfile
    from scripts.lceda_epro_review import review_epro
    with tempfile.TemporaryDirectory() as td:
        md = str(Path(td) / "r.md")
        js = str(Path(td) / "r.json")
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            review_epro(epro, board_name=board_name or None,
                        trace_nets=trace_nets, trace_refs=trace_refs,
                        out_md=md, out_json=js)
        if Path(js).exists():
            data = json.loads(Path(js).read_text(encoding="utf-8"))
            return data
        return {"error": "review produced no json", "log": buf.getvalue()[:800]}


# ---------------------------------------------------------------- registry

TOOLS: Dict[str, Callable[..., Any]] = {
    "parse": _tool_parse,
    "review": _tool_review,
    "texts": _tool_texts,
    "nets": _tool_nets,
    "netfind": _tool_netfind,
    "trace": _tool_trace,
    "components": _tool_components,
    "diff": _tool_diff,
    "lceda_review": _tool_lceda_review,
}

_TOOL_META = [
    ("parse", "解析 KiCad 工程（目录或根 .kicad_sch），返回图纸/元件/网络统计", {
        "project": {"type": "string", "description": "KiCad 工程目录或根 .kicad_sch"},
        "required": ["project"]}),
    ("review", "运行设计审查（R101..R801 等规则 + 可选官方 ERC），返回全部 Issue 与证据级别", {
        "project": {"type": "string"},
        "no_erc": {"type": "boolean", "description": "跳过 kicad-cli ERC（默认 true）"},
        "config": {"type": "string", "description": "review_rules.json 路径"},
        "required": ["project"]}),
    ("texts", "导出页内自由文本/设计说明注释", {
        "project": {"type": "string"}, "filter": {"type": "string"},
        "required": ["project"]}),
    ("nets", "项目网络清单（可按名过滤）", {
        "project": {"type": "string"}, "name": {"type": "string"},
        "required": ["project"]}),
    ("netfind", "按网络名查全部引脚（N$ 网络用 exact=true）", {
        "project": {"type": "string"}, "name": {"type": "string"},
        "exact": {"type": "boolean"},
        "required": ["project", "name"]}),
    ("trace", "从位号出发按网络 BFS 链路追踪", {
        "project": {"type": "string"}, "ref": {"type": "string"},
        "depth": {"type": "integer", "default": 4},
        "no_power": {"type": "boolean"},
        "required": ["project", "ref"]}),
    ("components", "元件清单（可按位号/值/库ID过滤）", {
        "project": {"type": "string"}, "filter": {"type": "string"},
        "required": ["project"]}),
    ("diff", "两个工程版本间的元件/网络差异（候选级）", {
        "project_a": {"type": "string"}, "project_b": {"type": "string"},
        "required": ["project_a", "project_b"]}),
    ("lceda_review", "LCEDA .epro 工程审查（CBB 展开 + trace-net/ref 穿透）", {
        "epro": {"type": "string", "description": ".epro 文件路径"},
        "board_name": {"type": "string"},
        "trace_nets": {"type": "array", "items": {"type": "string"}},
        "trace_refs": {"type": "array", "items": {"type": "string"}},
        "required": ["epro"]}),
]


# ---------------------------------------------------------------- MCP framing

def _rpc(id_: Any, result: Any) -> None:
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": id_, "result": result},
                                ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _tool_call_response(id_: Any, tool: str, args: dict) -> None:
    fn = TOOLS.get(tool)
    if fn is None:
        _rpc_error(id_, -32601, f"Unknown tool: {tool}")
        return
    try:
        result = fn(**args)
        sys.stdout.write(json.dumps({
            "jsonrpc": "2.0", "id": id_,
            "result": {
                "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
                "isError": False,
            },
        }, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    except Exception as exc:
        _rpc_error(id_, -32000, f"{type(exc).__name__}: {exc}")


def _rpc_error(id_: Any, code: int, message: str) -> None:
    sys.stdout.write(json.dumps({
        "jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message},
    }, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _serve() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = msg.get("method", "")
        req_id = msg.get("id")
        params = msg.get("params") or {}
        if method == "initialize":
            _rpc(req_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "kicad-sch-reader", "version": "0.1.3"},
            })
        elif method == "notifications/initialized" or method.startswith("notifications/"):
            continue
        elif method == "tools/list":
            _rpc(req_id, {"tools": [
                {"name": name, "description": desc, "inputSchema": {
                    "type": "object", "properties": props,
                    "required": props.get("required", []),
                }}
                for name, desc, props in _TOOL_META
            ]})
        elif method == "tools/call":
            name = params.get("name", "")
            args = params.get("arguments") or {}
            _tool_call_response(req_id, name, args)
        else:
            _rpc_error(req_id, -32601, f"Method not found: {method}")


def _selftest() -> None:
    import os
    ex = os.path.join(BASE, "examples", "Lock-In-Amplifier_MainBoard_V0.1")
    reqs = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
         "params": {"name": "parse", "arguments": {"project": ex}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
         "params": {"name": "netfind", "arguments": {"project": ex, "name": "GND"}}},
    ]
    import io
    buf = io.StringIO()
    stdin_bak, stdout_bak = sys.stdin, sys.stdout
    sys.stdin = io.TextIOWrapper(io.BytesIO(("\n".join(json.dumps(r, ensure_ascii=False)
                                                       for r in reqs) + "\n").encode("utf-8")))
    sys.stdout = buf
    result = None
    try:
        _serve()
        out = buf.getvalue()
        lines = [json.loads(l) for l in out.splitlines() if l.strip()]
        ids = {m["id"]: m for m in lines}
        assert 1 in ids and "capabilities" in ids[1]["result"]
        tools = ids[2]["result"]["tools"]
        assert any(t["name"] == "parse" for t in tools), "parse tool missing"
        parse_res = json.loads(ids[3]["result"]["content"][0]["text"])
        assert parse_res["sheet_count"] >= 1, "parse result empty"
        gf = json.loads(ids[4]["result"]["content"][0]["text"])
        assert gf["count"] >= 1, "netfind GND empty"
        result = (len(tools), parse_res["sheet_count"], gf["count"])
    finally:
        sys.stdin, sys.stdout = stdin_bak, stdout_bak
    print(f"SELFTEST PASS: tools={result[0]} parse sheets={result[1]} GND nets={result[2]}")
    return result is not None


def main() -> int:
    if "--selftest" in sys.argv:
        _selftest()
        return 0
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    _serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
