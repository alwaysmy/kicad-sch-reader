"""Regression tests for the source-neutral Circuit IR layer."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "repos" / "lceda-sch-reader"))

from kicad_sch_reader import circuit_ir, parser  # noqa: E402
from lceda_epro_review import review_epro  # noqa: E402

MAIN = ROOT / "examples" / "Lock-In-Amplifier_MainBoard_V0.1"
POWER = ROOT / "examples" / "Lock-In-Amplifier_PowerBoard_V0.1"
EPRO = ROOT / "examples" / "LIA_DigitalBoard_RevA" / "ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro"


@unittest.skipUnless(MAIN.exists() and POWER.exists(), "KiCad example fixtures missing")
class TestCircuitIRKiCad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = circuit_ir.board_from_kicad(parser.load_project(MAIN))
        cls.power = circuit_ir.board_from_kicad(parser.load_project(POWER))

    def test_kicad_boards_have_graph_shape(self):
        for board in (self.main, self.power):
            self.assertGreater(board.component_count, 0)
            self.assertGreater(board.net_count, 0)
            self.assertTrue(all(n.name for n in board.nets))

    def test_ground_and_power_kinds_are_structural(self):
        gnd = self.main.net("GND")
        self.assertIsNotNone(gnd)
        self.assertEqual(gnd.kind, circuit_ir.NET_GROUND)
        powered = [n for n in self.main.nets if n.kind == circuit_ir.NET_POWER]
        self.assertTrue(powered)

    def test_connector_view_contains_j102(self):
        connectors = self.main.connectors()
        self.assertIn("J102", connectors)
        self.assertGreaterEqual(connectors["J102"]["pin_count"], 2)

    def test_cross_board_detected_link_never_confirmed(self):
        rows = circuit_ir.compare_boards(self.main, self.power)
        top = rows[0]
        self.assertEqual(top.a_ref, "J102")
        self.assertEqual(top.b_ref, "J103")
        self.assertAlmostEqual(top.score, 1.0)
        self.assertEqual(top.confidence, circuit_ir.CONFIDENCE_DETECTED)
        self.assertNotEqual(top.confidence, circuit_ir.CONFIDENCE_CONFIRMED)
        self.assertEqual(top.evidence.kind, circuit_ir.EVIDENCE_CALCULATED)


@unittest.skipUnless(EPRO.exists(), "LIA_DigitalBoard_RevA .epro fixture missing")
class TestCircuitIRLceda(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        report = review_epro(
            str(EPRO),
            out_md=str(Path(cls.tmp.name) / "lia.md"),
            out_json=str(Path(cls.tmp.name) / "lia.json"),
        )
        cls.board = circuit_ir.board_from_lceda(report)
        cls.report = report

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_lceda_graph_matches_report(self):
        self.assertEqual(self.board.format, "lceda")
        self.assertGreater(self.board.component_count, 0)
        # The IR collapses multi-unit designators, so it can never exceed the
        # flat component list; it must still contain every designator family.
        self.assertLessEqual(self.board.component_count, self.report["flat_component_count"])
        self.assertGreater(self.board.net_count, 0)

    def test_cbb_internal_component_reaches_parent_net(self):
        u6 = self.board.component("U6")
        self.assertIsNotNone(u6)
        self.assertEqual(u6.module_instance, "CBB1")
        self.assertEqual(self.board.pin_net("U6", "VIN"), "VCC_5V")
        # U6.SW 在 CBB 内部经 L5(电感)才到 VOUT；工具不再跨非 0Ω 器件并网。
        expected_raw = next(
            (net for key, net in self.report["pin_net_map"].items()
             if key.endswith("||U6||SW")),
            None,
        )
        self.assertEqual(self.board.pin_net("U6", "SW"), expected_raw or None)

    def test_lceda_connectors_include_usb(self):
        connectors = self.board.connectors()
        self.assertIn("USB1", connectors)
        self.assertIn("USB2", connectors)
        for ref in ("USB1", "USB2"):
            pins = connectors[ref]["pins"]
            self.assertGreaterEqual(len(pins), 4)
            self.assertTrue(any("VBUS" in str(n).upper() for n in pins.values()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
