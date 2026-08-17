#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多工程跨板检查（KiCad + LCEDA .epro 混合）。

每个工程先适配为共享 Circuit IR ``kicad_sch_reader.circuit_ir.BoardIR``，
再对其连接器视图做逐 pin 网络比较，输出候选 ``IRCrossLink``。
同名网络逐 pin 一致只是候选证据，不自动确认为物理连接。
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "repos" / "lceda-sch-reader"))

from kicad_sch_reader import circuit_ir, parser  # noqa: E402
from lceda_epro_review import review_epro  # noqa: E402


def load_kicad_board(project_dir) -> circuit_ir.BoardIR:
    project = parser.load_project(project_dir)
    return circuit_ir.board_from_kicad(project)


def load_lceda_board(epro_path, board_name=None) -> circuit_ir.BoardIR:
    # review_epro is deterministic; put its JSON into a temp dir to avoid
    # polluting reports during repeated runs.
    with tempfile.TemporaryDirectory() as tmp:
        report = review_epro(
            str(epro_path),
            board_name=board_name,
            out_md=str(Path(tmp) / "x.md"),
            out_json=str(Path(tmp) / "x.json"),
        )
    return circuit_ir.board_from_lceda(report)


def compare_connectors(a: circuit_ir.BoardIR, b: circuit_ir.BoardIR,
                       min_common=2) -> list:
    return circuit_ir.compare_boards(a, b, min_common=min_common)


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

    system = circuit_ir.IRSystem(boards=boards)
    all_rows = system.compare_all(min_common=args.min_common)

    payload = {
        "boards": [b.connector_view() for b in boards],
        "connections": [row.to_dict() for row in all_rows],
    }

    out_json = Path(args.out_json or ROOT / "reports" / "multi_project_cross_check.json")
    out_md = Path(args.out_md or ROOT / "reports" / "multi_project_cross_check.md")
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 多工程跨板检查报告", ""]
    for b in boards:
        lines.append(f"- `{b.name}` [{b.format}] — 连接器 {len(b.connectors())} 个")
    lines.append("")
    lines.append("| A | B | 一致 pin | 共同 pin | score | confidence | evidence | 差异示例 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in all_rows:
        diffs = "; ".join(f"{d['pin']}: {d['a_net']} != {d['b_net']}" for d in row.diffs[:3])
        lines.append(
            f"| {row.a_board} {row.a_ref} ({row.a_lib}) | "
            f"{row.b_board} {row.b_ref} ({row.b_lib}) | "
            f"{row.exact_pins} | {row.common_pins} | {row.score} | "
            f"{row.confidence} | {row.evidence.kind} | {diffs} |"
        )
    lines.append("")
    lines.append("> 说明：同名网络逐 pin 一致仍只是候选证据；只有用户声明或工程 metadata")
    lines.append("> 声明连接器对插后才应视为 confirmed。")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"boards={len(boards)} connections={len(all_rows)}")
    print(f"json={out_json}")
    print(f"md={out_md}")
    for row in all_rows[:15]:
        print(f"[{row.confidence}] {row.a_board}.{row.a_ref} <-> "
              f"{row.b_board}.{row.b_ref} score={row.score} "
              f"exact={row.exact_pins}/{row.common_pins}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
