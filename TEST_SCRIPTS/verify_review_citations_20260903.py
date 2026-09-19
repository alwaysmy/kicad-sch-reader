#!/usr/bin/env python3
"""Verify line-number citations used in architecture-review-mimox-20260903.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    # (file, needle, expected_line_or_range)
    ("kicad_sch_reader/connectivity.py", "group.hier_sources", 425),
    ("kicad_sch_reader/connectivity.py", "group.label_entries", 426),
    ("kicad_sch_reader/connectivity.py", "sorted(n.pins[0].ref", 461),
    ("kicad_sch_reader/connectivity.py", "best_d = 0.01", 138),
    ("kicad_sch_reader/connectivity.py", "EPS_MM = 0.001", 28),
    ("kicad_sch_reader/connectivity.py", "def find_net_for", 353),
    ("kicad_sch_reader/cli.py", "out_md = args.out_md", 464),
    ("kicad_sch_reader/cli.py", "a_net == b_net", 560),
    ("kicad_sch_reader/parser.py", "200000", 516),
    ("kicad_sch_reader/parser.py", "queue.pop(0)", 532),
    ("kicad_sch_reader/sexpr.py", "stack.pop(0)", 125),
    ("kicad_sch_reader/rules.py", "_UNNAMED_RATIO_WARN", 68),
    ("kicad_sch_reader/rules.py", "_UNNAMED_COUNT_WARN", 69),
    ("kicad_sch_reader/model.py", 'def pin_count', 242),
    ("scripts/lceda_epro_review.py", "_monkeypatch_epro_overrides", 276),
    ("kicad_sch_reader/model.py", "class Net:", 229),
    ("kicad_sch_reader/circuit_ir.py", "def compare_boards", 739),
    ("kicad_sch_reader/circuit_ir.py", "def normalize_net", 64),
]

POWER_PREFIX_SITES = []

def main():
    print("=== Line citation checks ===")
    ok = fail = 0
    for rel, needle, expected in CHECKS:
        path = ROOT / rel
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = [i + 1 for i, line in enumerate(lines) if needle in line]
        if expected in hits:
            print(f"  OK   {rel}:{expected}  ({needle[:50]})")
            ok += 1
        else:
            print(f"  FAIL {rel}  expected {expected}, hits={hits[:5]}  ({needle[:50]})")
            fail += 1

    print("\n=== power: prefix sites in package ===")
    for path in sorted((ROOT / "kicad_sch_reader").glob("*.py")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, line in enumerate(lines, 1):
            if 'startswith("power:")' in line:
                print(f"  {path.name}:{i}: {line.strip()[:110]}")
                POWER_PREFIX_SITES.append((path.name, i))

    print(f"\n=== Summary: {ok} OK, {fail} FAIL; power-prefix sites={len(POWER_PREFIX_SITES)} ===")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
