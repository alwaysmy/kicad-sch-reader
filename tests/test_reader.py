"""Unit tests for the pure-Python reader.

Run with ``python -m unittest tests.test_reader`` from the repository root.
The example projects are used as fixtures, exactly as requested by the
project acceptance criteria.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kicad_sch_reader import connectivity, parser  # noqa: E402
from kicad_sch_reader.rules import run_all_checks  # noqa: E402

EXAMPLES = ROOT / "examples"
MAINBOARD = EXAMPLES / "Lock-In-Amplifier_MainBoard_V0.1"
POWERBOARD = EXAMPLES / "Lock-In-Amplifier_PowerBoard_V0.1"


class TestMainBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = parser.load_project(MAINBOARD)
        cls.netlist = connectivity.build_netlist(cls.project)

    def test_hierarchy_is_loaded(self):
        self.assertEqual(len(self.project.sheets), 5)  # root + 4 referenced child sheets
        self.assertEqual(len(self.project.root_sheet.sheets), 4)

    def test_netlist_has_power_nets(self):
        names = {n.name for n in self.netlist}
        for expected in {"GND", "+5VA", "-5VA", "+5VP", "+3.3V", "+12VA", "-12VA"}:
            self.assertIn(expected, names)

    def test_hierarchical_net_is_merged(self):
        adc = [n for n in self.netlist if n.name == "ADC_CS" or n.name.endswith("/ADC_CS")]
        self.assertEqual(len(adc), 1, "ADC_CS should be one project-wide net")
        pins = {(p.sheet_path, p.ref) for p in adc[0].pins}
        self.assertIn(("/", "J101"), pins)
        self.assertTrue(any("843e73eb" in path for path, _ in pins))

    def test_no_duplicate_issue_for_multi_unit_parts(self):
        issues = run_all_checks(self.project, self.netlist)
        duplicate_same_sheet = [i for i in issues if i.code == "R101"]
        self.assertEqual(duplicate_same_sheet, [])


class TestPowerBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = parser.load_project(POWERBOARD)
        cls.netlist = connectivity.build_netlist(cls.project)

    def test_flat_project(self):
        self.assertEqual(len(self.project.sheets), 1)
        self.assertGreaterEqual(len(self.project.all_symbols()), 200)

    def test_ground_and_vbus_merged(self):
        names = {n.name: n for n in self.netlist}
        self.assertIn("GND", names)
        self.assertIn("VBUS", names)
        self.assertGreaterEqual(names["GND"].pin_count(), 40)
        self.assertGreaterEqual(names["VBUS"].pin_count(), 10)

    def test_rules_run(self):
        issues = run_all_checks(self.project, self.netlist)
        self.assertGreaterEqual(len(issues), 1)


class TestCLIFeatures(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "kicad-sch-reader.py"), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120, cwd=str(ROOT))

    def test_netfind_exact_n_dollar(self):
        r = self.run_cli("netfind", str(MAINBOARD), "N$124", "--exact")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("== N$124 ==", r.stdout)
        self.assertNotIn("AFE_OUT_P", r.stdout)

    def test_bridges_exports_r_pack_pairs(self):
        r = self.run_cli("--json", "bridges", str(MAINBOARD))
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = json.loads(r.stdout)
        rn301 = [row for row in rows if row["ref"] == "RN301"]
        self.assertTrue(rn301)
        channels = {row["channel"] for row in rn301}
        self.assertGreaterEqual(channels, {1, 2, 3})


class TestRotationLab(unittest.TestCase):
    """Pin-position transform verified against kicad-cli with a synthetic file."""

    @classmethod
    def setUpClass(cls):
        fixture = ROOT / "tests" / "fixtures" / "mini.kicad_sch"
        if not fixture.exists():
            raise unittest.SkipTest("mini.kicad_sch fixture missing")
        sheet = parser.parse_sheet_file(fixture, "/")
        cls.symbols = {s.ref: s for s in sheet.symbols}

    def test_rot0(self):
        pins = {p.number: p.pos for p in self.symbols["C1"].pins}
        self.assertAlmostEqual(pins["1"][0], 0.0)
        self.assertAlmostEqual(pins["1"][1], -2.54)
        self.assertAlmostEqual(pins["2"][1], 2.54)

    def test_rot90_and_mirrors(self):
        base = {ref: s.pos for ref, s in self.symbols.items()}
        c2 = {p.number: p.pos for p in self.symbols["C2"].pins}
        self.assertAlmostEqual(c2["1"][0] - base["C2"][0], -2.54)
        self.assertAlmostEqual(c2["2"][0] - base["C2"][0], 2.54)
        c5 = {p.number: p.pos for p in self.symbols["C5"].pins}
        self.assertAlmostEqual(c5["1"][0] - base["C5"][0], -2.54)
        c6 = {p.number: p.pos for p in self.symbols["C6"].pins}
        self.assertAlmostEqual(c6["1"][0] - base["C6"][0], 2.54)

    def test_rot180_and_270(self):
        base = {ref: s.pos for ref, s in self.symbols.items()}
        c3 = {p.number: p.pos for p in self.symbols["C3"].pins}
        self.assertAlmostEqual(c3["1"][1] - base["C3"][1], 2.54)
        c4 = {p.number: p.pos for p in self.symbols["C4"].pins}
        self.assertAlmostEqual(c4["1"][0] - base["C4"][0], 2.54)
        self.assertAlmostEqual(c4["2"][0] - base["C4"][0], -2.54)


if __name__ == "__main__":
    unittest.main(verbosity=2)
