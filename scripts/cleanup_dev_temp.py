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
    "_v*.bat", "_v*.py", "_v*.log", "_v*.txt", "_v*_*.txt",
    "v*_*.txt", "v*.txt",
    "t9*_*.txt", "t9*.txt", "t10*_*.txt", "t10*.txt",
    "_x*.bat", "_x*.py", "_x*.txt", "_x*.log",
    "_run_all*.bat", "_run_all*.log", "_run_all*.txt", "_run_all_view*.txt",
    "_wait*.bat", "_wait*.txt", "_dec.bat", "_gitinfo.bat", "_gitinfo.txt",
    "_gitdiff.bat", "_gitdiff.txt",
    "x1_chatgpt_fetch.txt", "x2_chatgpt_body.txt", "x2_chatgpt_keywords.txt",
    "x3_webbridge.txt", "x4_webbridge.txt",
    "docs/dsh-session-*.zip",
    "_run_cleanup.bat", "_cleanup.bat", "_cleanup_run.bat", "_cleanup_log.txt",
    "_python_alive.py", "_python_alive.txt", "_run_test.bat",
    "_cleanup*.bat", "_cleanup*.txt",
    "_st.bat", "_st.txt",
    "_commit*.bat", "_commit*.log", "_hold*.bat",
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
