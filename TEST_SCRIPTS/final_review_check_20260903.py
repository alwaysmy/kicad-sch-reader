#!/usr/bin/env python3
"""Final completeness check of architecture-review-mimox-20260903.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "architecture-review-mimox-20260903.md"

def main() -> int:
    text = DOC.read_text(encoding="utf-8")
    lines = text.splitlines()

    print(f"File: {DOC}")
    print(f"Lines: {len(lines)}")
    print(f"Signed mimox: {'mimox' in text}")
    print()

    print("=== Headings ===")
    for line in lines:
        if line.startswith("## ") or line.startswith("### "):
            print(" ", line[:100])

    p0 = sum(1 for line in lines if line.startswith("### P0-"))
    p1 = sum(1 for line in lines if line.startswith("### P1-"))
    p2 = sum(1 for line in lines if line.startswith("### P2-"))
    print()
    print(f"Issue counts: P0={p0} P1={p1} P2={p2} total={p0+p1+p2}")

    required_phrases = [
        "审查人",
        "mimox",
        "项目目标",
        "架构全景",
        "架构优点",
        "设计问题",
        "系统思维",
        "改进建议",
        "结论",
        "P0-1",
        "P0-2",
        "P0-3",
        "P0-4",
        "probe_missing_sheet",
        "verify_review_citations",
    ]
    missing = [p for p in required_phrases if p not in text]
    print(f"Required phrases missing: {missing or 'none'}")

    # Section order sanity
    order_keys = ["## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7."]
    positions = [text.find(k) for k in order_keys]
    ordered = all(positions[i] < positions[i + 1] for i in range(len(positions) - 1)) and all(p >= 0 for p in positions)
    print(f"Sections 1-7 in order: {ordered}")

    ok = (p0 >= 4 and p1 >= 6 and p2 >= 5 and not missing and ordered and "mimox" in text)
    print()
    print("RESULT:", "PASS — document complete" if ok else "FAIL — incomplete")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
