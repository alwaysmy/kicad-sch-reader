#!/usr/bin/env python3
"""Cross-validate our geometric netlist against the official kicad-cli netlist.

This is the acceptance test for the example projects under
``examples/``.  It requires KiCad's ``kicad-cli`` on PATH (or ``KICAD_CLI``).

Run from the repository root::

    python tests/validate_examples.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kicad_sch_reader import connectivity, kicad_cli, parser, sexpr  # noqa: E402


def parse_official_netlist(path: Path) -> dict:
    nodes = sexpr.parse(path.read_text(encoding="utf-8", errors="replace"))
    root = nodes[0] if nodes else []
    mapping: dict[tuple[str, str], str] = {}

    def walk(nodes):
        stack = list(reversed(nodes))
        while stack:
            node = stack.pop()
            if not isinstance(node, list) or not node:
                continue
            if node[0] == "net":
                name_node = sexpr.first(node, "name")
                net_name = str(name_node[1]) if name_node and len(name_node) > 1 else ""
                for item in sexpr.children(node, "node"):
                    ref = sexpr.first(item, "ref")
                    pin = sexpr.first(item, "pin")
                    if ref and pin:
                        mapping[(str(ref[1]), str(pin[1]))] = net_name
            else:
                stack.extend(reversed(node[1:]))

    walk([root])
    return mapping


def normalize_name(name: str) -> str:
    """Strip KiCad's hierarchical ``/Sheet/Label`` prefix."""
    if name.startswith("unconnected-"):
        return name
    return name.rsplit("/", 1)[-1]


def names_match(ours_raw: str, official_raw: str) -> bool:
    """Three-way net-name comparison against the official exporter.

    1. plain tail equality (``/Sheet/Label`` vs ``Label``);
    2. our unnamed ``N$n`` vs official single-pin ``Net-(REF-PIN)``;
    3. literal slashes inside label text are exported as ``{slash}`` —
       compare again with those unescaped (a label "P_C/BE0#" is one name,
       not a hierarchy).
    """
    a, b = normalize_name(ours_raw), normalize_name(official_raw)
    if a == b:
        return True
    if a.startswith("N$") and b.startswith("Net-"):
        return True
    fa = ours_raw.replace("{slash}", "/").rsplit("/", 1)[-1]
    fb = official_raw.replace("{slash}", "/").rsplit("/", 1)[-1]
    return fa == fb


def validate_project(project_dir: Path, work_dir: Path) -> dict:
    project = parser.load_project(project_dir)
    netlist = connectivity.build_netlist(project)
    ours = {
        (p.ref, p.pin_number): n.name
        for n in netlist for p in n.pins
    }
    net_file = work_dir / f"{project_dir.name}.net"
    kicad_cli.export_netlist(project.root_sheet.file, output_file=str(net_file))
    official = parse_official_netlist(net_file)

    # KiCad's netlist does not contain power symbols (#PWR...) as components.
    ours_real = {k: v for k, v in ours.items() if not k[0].startswith("#")}
    official_real = {k: v for k, v in official.items() if not v.startswith("unconnected-")}

    common = set(ours_real) & set(official_real)
    missing = sorted(set(official_real) - set(ours_real))
    extra = sorted(set(ours_real) - set(official_real))
    mismatches = []
    for key in sorted(common):
        a, b = ours_real[key], official_real[key]
        if not names_match(a, b):
            mismatches.append((key, a, b))

    precision = 0
    if common:
        matched = len(common) - len(mismatches)
        precision = matched / len(common)
    return {
        "project": project_dir.name,
        "ours_pins": len(ours_real),
        "official_pins": len(official_real),
        "common_pins": len(common),
        "missing_pins": len(missing),
        "extra_pins": len(extra),
        "name_mismatches": len(mismatches),
        "precision": round(precision, 4),
        "missing_samples": missing[:12],
        "extra_samples": extra[:12],
        "mismatch_samples": mismatches[:12],
    }


def main() -> int:
    examples = ROOT / "examples"
    work = ROOT / "reports" / "validation"
    work.mkdir(parents=True, exist_ok=True)
    projects = [
        examples / "Lock-In-Amplifier_MainBoard_V0.1",
        examples / "Lock-In-Amplifier_PowerBoard_V0.1",
    ]
    results = []
    failed = False
    for proj in projects:
        try:
            res = validate_project(proj, work)
            results.append(res)
            print(
                f"{res['project']}: common={res['common_pins']}/{res['official_pins']} "
                f"missing={res['missing_pins']} extra={res['extra_pins']} "
                f"name_mismatch={res['name_mismatches']} precision={res['precision']}"
            )
            # Acceptance thresholds chosen from the validated v0.1 build.
            if res["missing_pins"] > 0:
                failed = True
                print("  missing samples:", res["missing_samples"])
            if res["precision"] < 0.95:
                failed = True
                print("  mismatch samples:", res["mismatch_samples"])
        except Exception as exc:
            print(f"{proj.name}: FAILED {type(exc).__name__}: {exc}")
            failed = True

    out = work / "validation.json"
    import json
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"validation json: {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
