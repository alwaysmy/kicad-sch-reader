#!/usr/bin/env python3
"""Probe: missing hierarchical child sheet file — does load_project crash or warn?"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ROOT_SCH = """(kicad_sch
  (version 20231120)
  (generator eeschema)
  (uuid aaaaaaaa-0000-0000-0000-000000000001)
  (paper "A4")
  (lib_symbols)
  (sheet
    (at 10 10)
    (size 20 20)
    (uuid aaaaaaaa-0000-0000-0000-000000000002)
    (property "Sheetname" "Child" (at 10 10 0))
    (property "Sheetfile" "missing_child.kicad_sch" (at 10 12 0))
    (pin "SIG" input (at 30 15 180)
      (uuid aaaaaaaa-0000-0000-0000-000000000003)
    )
    (instances
      (project "demo"
        (path "/aaaaaaaa-0000-0000-0000-000000000001"
          (page "2")
        )
      )
    )
  )
  (sheet_instances
    (path "/" (page "1"))
  )
)
"""


def main() -> int:
    from kicad_sch_reader import parser
    from kicad_sch_reader.rules import run_all_checks
    from kicad_sch_reader import connectivity

    tmp = Path(tempfile.mkdtemp(prefix="kicad_miss_"))
    try:
        root = tmp / "proj"
        root.mkdir()
        (root / "demo.kicad_sch").write_text(ROOT_SCH, encoding="utf-8")
        try:
            project = parser.load_project(root)
            print("LOAD OK sheets=", sorted(project.sheets))
            netlist = connectivity.build_netlist(project)
            issues = run_all_checks(project, netlist)
            r601 = [i for i in issues if i.code == "R601"]
            print(f"R601 count={len(r601)}")
            for i in r601:
                print(" ", i.severity, i.message)
        except Exception as exc:
            print(f"LOAD FAILED: {type(exc).__name__}: {exc}")
            print("=> R601 cannot fire; load_project crashes on missing child file")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
