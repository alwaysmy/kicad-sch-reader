#!/usr/bin/env python3
"""Remove development scratch files that match temporary naming patterns.

Safe by design: only deletes files/directories matching explicit patterns;
project fixtures (examples/, repos/, reports/) are never touched.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

PATTERNS = [
    "_s*.bat", "_s*.py", "_s*_*.txt", "_s*.log",
    "_t*.bat", "_t*.py", "_t*.log", "_t*.txt", "_t*.json",
    "t9*_*.txt", "t9*.txt", "t10*_*.txt", "t10*.txt",
    "_run_cleanup.bat", "_cleanup.bat", "_cleanup_run.bat", "_cleanup_log.txt",
    "_python_alive.py", "_python_alive.txt", "_run_test.bat",
]

KEEP = {
    "scripts", "tests", "examples", "reports", "repos", "docs",
    ".git", "kicad_sch_reader",
}


def main() -> int:
    removed = []
    for pattern in PATTERNS:
        for path in ROOT.glob(pattern):
            if path.is_file():
                try:
                    path.unlink()
                    removed.append(str(path.relative_to(ROOT)))
                except OSError as exc:
                    print(f"skip {path}: {exc}", file=sys.stderr)
    for path in sorted(ROOT.iterdir()):
        if path.is_dir() and path.name not in KEEP and path.name.startswith("_"):
            import shutil
            shutil.rmtree(path, ignore_errors=True)
            removed.append(str(path.relative_to(ROOT)))
    print("removed:\n" + "\n".join(removed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
