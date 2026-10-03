#!/usr/bin/env python3
"""Strict official-netlist partition validation. Private projects stay external.

python tests/validate_examples.py /path/to/project --work-dir /tmp/validation
Requires a matching official KiCad CLI (KICAD_CLI may select its executable).
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from kicad_sch_reader import connectivity, kicad_cli, parser
from kicad_sch_reader.validation import official_partitions, reader_partitions, compare_partitions


def validate_project(project_dir: Path, work_dir: Path) -> dict:
    project = parser.load_project(project_dir)
    nets = connectivity.build_netlist(project)
    work_dir.mkdir(parents=True, exist_ok=True)
    target = work_dir / (project.root_sheet.file.stem + '.net')
    kicad_cli.export_netlist(project.root_sheet.file, str(target))
    ours, _ = reader_partitions(project, nets, include_unconnected=True)
    official, _ = official_partitions(target, project.root_sheet.uuid, include_unconnected=True)
    return dict(project=project.root_sheet.file.stem, **compare_partitions(ours, official))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('projects', nargs='+', type=Path)
    ap.add_argument('--work-dir', type=Path, required=True)
    args = ap.parse_args()
    results = []
    for p in args.projects:
        try:
            result = validate_project(p, args.work_dir)
        except Exception as exc:
            result = {'project': p.name, 'passed': False, 'error': str(exc)}
        results.append(result)
        print(json.dumps(result, ensure_ascii=False))
    args.work_dir.mkdir(parents=True, exist_ok=True)
    (args.work_dir / 'validation.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(r['passed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
