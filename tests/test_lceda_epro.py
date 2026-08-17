"""Regression tests for LCEDA `.epro` CBB expansion.

The fixture is the real project under ``examples/LIA_DigitalBoard_RevA``.
When the fixture is missing (for example in a minimal CI checkout) the tests
are skipped.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "repos" / "lceda-sch-reader"))

from lceda_epro_review import review_epro  # noqa: E402

EPRO = ROOT / "examples" / "LIA_DigitalBoard_RevA" / "ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro"


@unittest.skipUnless(EPRO.exists(), "LIA_DigitalBoard_RevA .epro fixture missing")
class TestCbbExpansion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.report = review_epro(
            str(EPRO),
            out_md=str(Path(cls.tmp.name) / "lia.review.md"),
            out_json=str(Path(cls.tmp.name) / "lia.review.json"),
            trace_nets=["VCC_1V5", "VCC_1V0"],
            trace_refs=["U6"],
        )

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_four_cbb_instances_found(self):
        self.assertEqual(len(self.report["cbb_modules"]), 4)
        refs = {m["designator"] for m in self.report["cbb_modules"]}
        self.assertEqual(refs, {"CBB1", "CBB2", "CBB3", "CBB4"})

    def test_cbb_internal_designators_overridden(self):
        designators = {c["designator"] for c in self.report["flat_components"]}
        # CBB1 TPS563201 internal components got board-level designators via
        # INSTANCE/*.eins; the raw CBB page uses U1/L1/C1...
        for ref in ("U6", "L5", "C37", "C38", "R32"):
            self.assertIn(ref, designators)
        # CBB2/CBB4 Type-C connectors got USB1/USB2.
        self.assertIn("USB1", designators)
        self.assertIn("USB2", designators)

    def test_cbb_ports_have_parent_nets_and_internal_members(self):
        detail = {d["instance"]: d for d in self.report["cbb_detail"]}
        cbb1_ports = {p["name"]: p for p in detail["CBB1"]["ports"]}
        self.assertEqual(cbb1_ports["VIN"]["parent_net"], "VCC_5V")
        self.assertEqual(cbb1_ports["VOUT"]["parent_net"], "VCC_1V5")
        vout_members = {(m["ref"], m["pin"]) for m in cbb1_ports["VOUT"]["internal_members"]}
        self.assertIn(("U6", "SW"), vout_members)
        self.assertIn(("L5", "2"), vout_members)

    def test_trace_net_reaches_cbb_internal_devices(self):
        net_trace = self.report["trace_results"]["nets"]["VCC_1V5"]
        self.assertTrue(any(m["ref"] == "U6" and m["pin"] == "SW" and m["module_instance"] == "CBB1"
                            for m in net_trace))
        self.assertTrue(any(m["ref"] == "L5" and m["module_instance"] == "CBB1"
                            for m in net_trace))

    def test_trace_ref_crosses_cbb_boundary(self):
        edges = self.report["trace_results"]["refs"]["U6"]
        # U6 VIN is on the CBB child page and should reach the parent-side
        # CBB symbol pin and board-level components on VCC_5V.
        self.assertTrue(any(e["from_ref"] == "U6" and e["from_pin"] == "VIN" for e in edges))
        self.assertTrue(any(e["to_module_instance"] == "" and e["to_ref"] != "U6" for e in edges))

    def test_no_cbb_unconnected_or_duplicate_errors(self):
        codes = {f["code"] for f in self.report["findings"]}
        self.assertNotIn("CBB_PIN_UNCONNECTED", codes)
        self.assertNotIn("DUPLICATE_DESIGNATOR", codes)

    def test_cbb_pin_type_warnings_preserved(self):
        rows = [
            (f["ref"], f["message"])
            for f in self.report["findings"]
            if f["code"] == "CBB_PIN_TYPE_SUSPECT"
        ]
        self.assertTrue(any(ref == "CBB1.VOUT" for ref, _ in rows))
        self.assertTrue(any("D+" in (ref + msg) for ref, msg in rows))


if __name__ == "__main__":
    unittest.main(verbosity=2)
