#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多工程跨板检查（KiCad + LCEDA .epro 混合）。

把每个工程统一成 BoardView:
  board:
    name / format / root / connectors:
      ref -> {lib_id, sheet, pin_count, pins: {pin: net}, nets: {net: [pins]}}

然后对任意两块板的连接器做逐 pin 网络比较，输出候选 BoardConnection。
同名网络逐 pin 一致只是候选证据，不自动确认为物理连接。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "repos" / "lceda-sch-reader"))

from kicad_sch_reader import connectivity, parser  # noqa: E402
from lceda_epro_review import review_epro  # noqa: E402

CONNECTOR_RE = re.compile(r"^(CN|J|P|H|CON|USB)\d+", re.IGNORECASE)
CONNECTOR_KEYWORDS = ("connector", "header", "wafer", "socket", "barrel", "type-c", "typec", "btb")


def normalize_net(name: Optional[str]) -> str:
    if not name:
        return ""
    name = str(name).strip()
    # KiCad hierarchical prefix: /Sheet/Name -> Name.
    if "/" in name:
        name = name.rsplit("/", 1)[-1]
    # LCEDA SHORT 别名取第一个，且统一大小写/下划线。
    name = name.split(",")[0].strip()
    return re.sub(r"[^0-9A-Za-z+#.]", "", name).upper()


def _is_connector_ref(ref: str) -> bool:
    return bool(CONNECTOR_RE.match(ref or ""))


def load_kicad_board(project_dir) -> dict:
    project = parser.load_project(project_dir)
    netlist = connectivity.build_netlist(project)
    pin_net = {
        (p.sheet_path, p.ref, p.pin_number): n.name
        for n in netlist
        for p in n.pins
    }
    components = {}
    for sym in project.all_symbols():
        if not sym.ref or sym.ref.startswith("#"):
            continue
        components.setdefault(sym.ref, {"lib_id": sym.lib_id, "sheet": sym.sheet_path,
                                        "pins": defaultdict(dict)})
        for pin in sym.pins:
            components[sym.ref]["pins"][pin.number] = pin_net.get(
                (sym.sheet_path, sym.ref, pin.number), None)

    connectors = {}
    for ref, comp in components.items():
        lib_lower = comp["lib_id"].lower()
        pins = {p: n for p, n in comp["pins"].items() if n}
        looks_connector = (
            ("testpoint" not in lib_lower)
            and (("conn" in lib_lower) or any(k in lib_lower for k in CONNECTOR_KEYWORDS)
                 or (_is_connector_ref(ref) and len(pins) >= 2))
        )
        if looks_connector and pins:
            connectors[ref] = {
                "ref": ref,
                "lib_id": comp["lib_id"],
                "sheet": comp["sheet"],
                "pin_count": len(pins),
                "pins": {str(p): n for p, n in sorted(pins.items(), key=lambda kv: (len(kv[0]), kv[0]))},
            }
    return {
        "name": project.root.name,
        "format": "kicad",
        "root": str(project.root),
        "connectors": connectors,
    }


def load_lceda_board(epro_path, board_name=None) -> dict:
    # review_epro is deterministic; put its JSON into a temp dir to avoid
    # polluting reports during repeated runs.
    with tempfile.TemporaryDirectory() as tmp:
        report = review_epro(
            str(epro_path),
            board_name=board_name,
            out_md=str(Path(tmp) / "x.md"),
            out_json=str(Path(tmp) / "x.json"),
        )
    pin_map = report["pin_net_map"]
    # pin_net_map keys: "sheet||ref||pin"
    comp_pins: Dict[str, Dict[str, Dict[str, Optional[str]]]] = defaultdict(
        lambda: defaultdict(dict))
    sheets = {}
    for key, net in pin_map.items():
        parts = key.split("||", 2)
        if len(parts) != 3:
            continue
        sheet, ref, pin = parts
        comp_pins[ref][sheet][pin] = net or None
        sheets.setdefault(ref, sheet)

    connectors = {}
    for ref, by_sheet in comp_pins.items():
        # Flatten same ref across sheets (multi-unit connectors are rare).
        pins: Dict[str, Optional[str]] = {}
        for pin_map in by_sheet.values():
            for pin, net in pin_map.items():
                if net:
                    pins[pin] = net
        if not pins:
            continue
        comp = next((c for c in report["flat_components"] if c.get("designator") == ref), {})
        device = (comp.get("device_title") or comp.get("value") or comp.get("title") or "")
        looks_connector = (
            _is_connector_ref(ref)
            or any(k in device.lower() for k in CONNECTOR_KEYWORDS)
            or (len(pins) >= 4 and re.search(r"\d+P|PIN|HDR|BTB", device, re.IGNORECASE))
        )
        if looks_connector and len(pins) >= 2:
            connectors[ref] = {
                "ref": ref,
                "lib_id": device or ref,
                "sheet": sheets.get(ref, ""),
                "pin_count": len(pins),
                "pins": {str(p): n for p, n in sorted(pins.items(), key=lambda kv: (len(kv[0]), kv[0]))},
            }
    return {
        "name": report["board"],
        "format": "lceda",
        "root": report["epro"],
        "connectors": connectors,
    }


def compare_connectors(a: dict, b: dict, min_common=2) -> List[dict]:
    rows = []
    for ref_a, ca in sorted(a["connectors"].items()):
        for ref_b, cb in sorted(b["connectors"].items()):
            common = sorted(set(ca["pins"]) & set(cb["pins"]))
            if len(common) < min_common:
                continue
            exact = 0
            diffs = []
            for pin in common:
                na = normalize_net(ca["pins"].get(pin))
                nb = normalize_net(cb["pins"].get(pin))
                if na and na == nb:
                    exact += 1
                else:
                    diffs.append({"pin": pin, "a_net": ca["pins"].get(pin), "b_net": cb["pins"].get(pin)})
            score = round(exact / len(common), 4) if common else 0.0
            confidence = "detected" if score >= 1.0 and exact >= 2 else "candidate"
            rows.append({
                "a_board": a["name"],
                "a_format": a["format"],
                "a_ref": ref_a,
                "a_lib": ca["lib_id"],
                "b_board": b["name"],
                "b_format": b["format"],
                "b_ref": ref_b,
                "b_lib": cb["lib_id"],
                "common_pins": len(common),
                "exact_pins": exact,
                "diff_count": len(diffs),
                "score": score,
                "confidence": confidence,
                "diffs": diffs[:20],
            })
    rows.sort(key=lambda r: (-r["score"], -r["common_pins"], r["a_board"], r["b_board"]))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="多工程跨板连接器候选检查（KiCad/LCEDA 混合）")
    ap.add_argument("--kicad", action="append", default=[], help="KiCad 工程目录，可重复")
    ap.add_argument("--lceda", action="append", default=[], help="LCEDA .epro 文件，可重复")
    ap.add_argument("--lceda-board", help="LCEDA 板名（默认自动选择 LIA/锁定）")
    ap.add_argument("--min-common", type=int, default=2)
    ap.add_argument("--out-json")
    ap.add_argument("--out-md")
    args = ap.parse_args(argv)

    boards = []
    for path in args.kicad:
        boards.append(load_kicad_board(path))
    for path in args.lceda:
        boards.append(load_lceda_board(path, board_name=args.lceda_board))

    all_rows = []
    for i, a in enumerate(boards):
        for j, b in enumerate(boards):
            if i >= j:
                continue
            all_rows.extend(compare_connectors(a, b, min_common=args.min_common))

    payload = {
        "boards": [
            {"name": b["name"], "format": b["format"], "root": b["root"],
             "connectors": b["connectors"]}
            for b in boards
        ],
        "connections": all_rows,
    }

    out_json = Path(args.out_json or ROOT / "reports" / "multi_project_cross_check.json")
    out_md = Path(args.out_md or ROOT / "reports" / "multi_project_cross_check.md")
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 多工程跨板检查报告", ""]
    for b in boards:
        lines.append(f"- `{b['name']}` [{b['format']}] — 连接器 {len(b['connectors'])} 个")
    lines.append("")
    lines.append("| A | B | 一致 pin | 共同 pin | score | confidence | 差异示例 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in all_rows:
        diffs = "; ".join(f"{d['pin']}: {d['a_net']} != {d['b_net']}" for d in row["diffs"][:3])
        lines.append(
            f"| {row['a_board']} {row['a_ref']} ({row['a_lib']}) | "
            f"{row['b_board']} {row['b_ref']} ({row['b_lib']}) | "
            f"{row['exact_pins']} | {row['common_pins']} | {row['score']} | "
            f"{row['confidence']} | {diffs} |"
        )
    lines.append("")
    lines.append("> 说明：同名网络逐 pin 一致仍只是候选证据；只有用户声明或工程 metadata")
    lines.append("> 声明连接器对插后才应视为 confirmed。")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"boards={len(boards)} connections={len(all_rows)}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    for row in all_rows[:15]:
        print(f"[{row['confidence']}] {row['a_board']}.{row['a_ref']} <-> "
              f"{row['b_board']}.{row['b_ref']} score={row['score']} "
              f"exact={row['exact_pins']}/{row['common_pins']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
