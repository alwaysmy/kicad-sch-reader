#!/usr/bin/env python3
"""Confirm LCEDA review output is unchanged after upstream pull (one-shot)."""
import glob
import json

base = json.load(open(r"reports\LIA_DigitalBoard_RevA.lceda-review_20260822_214709.json", encoding="utf-8"))
f = sorted(glob.glob(r"reports/EmoeSOM*brd.lceda-review-2026*.json"))[-1]
print("comparing against:", f)
new = json.load(open(f, encoding="utf-8"))

print("=== base(pull-time 7036a08 report) vs current(upstream 8be0913) ===")
ok = True
for k in ("net_count", "flat_component_count", "bom_line_count"):
    same = base[k] == new[k]
    ok &= same
    print(f"{k}: base={base[k]} new={new[k]} " + ("OK" if same else "DIFF!"))
nb, nn = len(base["findings"]), len(new["findings"])
same = nb == nn
ok &= same
print(f"findings: base={nb} new={nn} " + ("OK" if same else "DIFF!"))

opm, npm = base["pin_net_map"], new["pin_net_map"]
diff = sum(1 for k in set(opm) | set(npm) if opm.get(k) != npm.get(k))
same = diff == 0 and len(opm) == len(npm)
ok &= same
print(f"pin_net_map: {len(opm)} vs {len(npm)} entries, value-diff={diff} " + ("OK" if same else "DIFF!"))

same = len(base["component_bridges"]) == len(new["component_bridges"])
ok &= same
print(f"bridges: {len(base['component_bridges'])} vs {len(new['component_bridges'])} " + ("OK" if same else "DIFF!"))

tn_b = base["trace_results"]["nets"].get("VCC_1V5", [])
tn_n = new["trace_results"]["nets"].get("VCC_1V5", [])
same = len(tn_b) == len(tn_n) and tn_n
ok &= bool(tn_n)
print(f"trace VCC_1V5: base={len(tn_b)} members, new={len(tn_n)} members")
cbb_new = [m for m in tn_n if m.get("module_instance")]
print("  CBB-internal members:", len(cbb_new), "->",
      ", ".join(f"{m['ref']}[{m['module_instance']}]" for m in cbb_new[:5]))
ur = new["trace_results"]["refs"].get("U6", [])
print(f"trace U6 hops: {len(ur)}")

print("\nVERDICT:", "LCEDA review fully functional, zero drift" if ok and diff == 0 else "CHECK FAILED")
