#!/usr/bin/env python3
"""Batch smoke + review + official-netlist cross-validation over local KiCad
projects (KiCad 10 demos + user projects spanning KiCad 6..9 file formats).

Read-only w.r.t. the projects under test. Results are written to
TEST_SCRIPTS/results/batch_<timestamp>.json / .md (timestamped, never overwritten).

Usage (from repo root)::

    python TEST_SCRIPTS/batch_kicad_review.py [--no-netlist] [--only substr]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kicad_sch_reader import connectivity, parser, rules  # noqa: E402

DEMOS = Path(r"C:\Program Files\KiCad\10.0\share\kicad\demos")

PROJECTS = [
    # --- KiCad 10 official demos (structural diversity) ---
    DEMOS / "complex_hierarchy",
    DEMOS / "multichannel",
    DEMOS / "jetson-agx-thor-baseboard",
    DEMOS / "pic_programmer",
    DEMOS / "video",
    DEMOS / "ecc83",
    # --- User projects spanning KiCad 6..9 file formats ---
    # (ADS1292R_EVM skipped: KiCad-5 legacy .sch format, out of scope.)
    Path(r"D:\MyProjects\1_MySpace\KiCadProjects\CH340E"),
    Path(r"D:\MyProjects\2_MyDesigns\4_Lightsensor\LightSensor"),
    Path(r"D:\MyProjects\2_MyDesigns\5_R2R_DAC\2022YearRedesign\R2R_DAC_16BIT"),
    Path(r"D:\MyProjects\2_MyDesigns\1夹具冶具延长线转接板测试架\测试冶具夹具\USB测试夹具"),
    Path(r"D:\MyProjects\2_MyDesigns\5_R2R_DAC\设计分Part\I2S接收实现\i2s_recv_part_rev0.2"),
]


def probe_one(project_dir: Path) -> dict:
    t0 = time.perf_counter()
    result: dict = {"project": str(project_dir), "name": project_dir.name}
    try:
        project = parser.load_project(project_dir)
        netlist = connectivity.build_netlist(project)
        issues = rules.run_all_checks(project, netlist)
        codes = Counter(i.code.split("-")[0] for i in issues)
        sev = Counter(i.severity for i in issues)
        errors = [i for i in issues if i.severity == "error"]
        versions = sorted({s.version for s in project.sheets.values()})
        texts_total = sum(len(s.texts) for s in project.sheets.values())
        title_blocks = sum(1 for s in project.sheets.values() if s.title_fields.get("title"))
        result.update({
            "ok": True,
            "file_version": versions,
            "sheets": len(project.sheets),
            "symbols": len(project.all_symbols()),
            "nets": len(netlist),
            "pin_connections": sum(len(n.pins) for n in netlist),
            "free_texts": texts_total,
            "title_blocks_with_title": title_blocks,
            "issues": len(issues),
            "issue_severity": dict(sev),
            "issue_codes": dict(codes),
            "error_samples": [f"{i.code}: {i.message[:120]}" for i in errors[:8]],
            "seconds": round(time.perf_counter() - t0, 2),
        })
    except Exception as exc:
        result.update({
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "seconds": round(time.perf_counter() - t0, 2),
        })
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-netlist", action="store_true",
                    help="skip kicad-cli official-netlist cross validation")
    ap.add_argument("--only", default="", help="run only projects whose path contains this")
    args = ap.parse_args()

    out_dir = ROOT / "TEST_SCRIPTS" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Import here so --help works without a KiCad install.
    from tests.validate_examples import validate_project

    selected = [p for p in PROJECTS if p.exists()]
    if args.only:
        selected = [p for p in selected if args.only.lower() in str(p).lower()]

    results = []
    failures = 0
    print(f"batch start: {len(selected)} projects, stamp={stamp}")
    for proj in selected:
        res = probe_one(proj)
        results.append(res)
        if not res["ok"]:
            failures += 1
            print(f"[FAIL] {proj.name}: {res['error']}")
        else:
            print(f"[ok] {proj.name}: v{','.join(res['file_version'])} "
                  f"sheets={res['sheets']} sym={res['symbols']} nets={res['nets']} "
                  f"texts={res['free_texts']} issues={res['issues']} "
                  f"errors={res['issue_severity'].get('error', 0)} ({res['seconds']}s)")
        # Persist incrementally so an interrupted run keeps partial evidence.
        (out_dir / f"batch_{stamp}.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.no_netlist:
        work = out_dir / f"netlists_{stamp}"
        work.mkdir(parents=True, exist_ok=True)
        for proj in selected:
            existing = next((r for r in results if r["project"] == str(proj)), None)
            if not existing or not existing.get("ok"):
                continue
            try:
                val = validate_project(proj, work)
                existing["netlist_check"] = {
                    "common": val["common_pins"], "official": val["official_pins"],
                    "missing": val["missing_pins"], "extra": val["extra_pins"],
                    "name_mismatches": val["name_mismatches"], "precision": val["precision"],
                    "missing_samples": [f"{k[0]}.{k[1]}" for k in val["missing_samples"]],
                    "extra_samples": [f"{k[0]}.{k[1]}" for k in val["extra_samples"]],
                    "mismatch_samples": [
                        f"{m[0][0]}.{m[0][1]}: ours={m[1]!r} official={m[2]!r}"
                        for m in val["mismatch_samples"]
                    ],
                }
                flag = "PASS" if val["missing_pins"] == 0 and val["precision"] >= 0.95 else "WEAK"
                print(f"[netlist {flag}] {proj.name}: common={val['common_pins']}/{val['official_pins']} "
                      f"missing={val['missing_pins']} precision={val['precision']}")
            except Exception as exc:
                existing["netlist_check"] = {"error": f"{type(exc).__name__}: {exc}"}
                print(f"[netlist SKIP] {proj.name}: {type(exc).__name__}: {exc}")
            finally:
                (out_dir / f"batch_{stamp}.json").write_text(
                    json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    ok_count = sum(1 for r in results if r.get("ok"))
    md = [f"# Batch KiCad review — {stamp}", "",
          f"- total: {len(results)}  ok: {ok_count}  failed: {failures}", "",
          "| project | ver | sheets | symbols | nets | texts | issues(err) | netlist check |", 
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in results:
        nc = r.get("netlist_check", {})
        ncs = (f"missing={nc['missing']} prec={nc['precision']}" if "missing" in nc
               else nc.get("error", "-"))
        md.append(
            f"| {r['name']} | {','.join(r.get('file_version', []))} | {r.get('sheets','-')} "
            f"| {r.get('symbols','-')} | {r.get('nets','-')} | {r.get('free_texts','-')} "
            f"| {r.get('issues','-')}({r.get('issue_severity',{}).get('error',0)}) | {ncs} |")
    (out_dir / f"batch_{stamp}.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nresults: {out_dir / f'batch_{stamp}.json'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
