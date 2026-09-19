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


class TestRuleGrouping(unittest.TestCase):
    """Grouped reporting for high-noise rules (R103/R304/R701) + bilingual
    ERC pin attribution.  Uses in-memory synthetic projects."""

    @staticmethod
    def _project(symbols, no_connects=()):
        from kicad_sch_reader.model import NoConnect, Project, SheetData
        sheet = SheetData(path="/", file=Path("synthetic.kicad_sch"))
        sheet.symbols = list(symbols)
        sheet.no_connects = [NoConnect(pos=p) for p in no_connects]
        proj = Project(root=Path("."))
        proj.sheets["/"] = sheet
        proj.sheet_order = ["/"]
        return proj

    @staticmethod
    def _sym(ref, value="1k", pins=(), dnp=False):
        from kicad_sch_reader.model import SymbolInstance
        return SymbolInstance(ref=ref, value=value, lib_id="Device:R",
                              pins=list(pins), dnp=dnp)

    def test_r103_gap_aggregated_to_one_issue(self):
        from kicad_sch_reader import rules
        syms = [self._sym(r) for r in ("C201", "C202", "C204", "C701")]
        issues = rules.check_reference_sequences(self._project(syms))
        gap_issues = [i for i in issues if i.title.startswith("位号编号不连续")]
        self.assertEqual(len(gap_issues), 1, "one aggregate row, not one per prefix")
        msg = gap_issues[0].message
        self.assertIn("C203", msg)          # in-block gap is enumerated
        self.assertNotIn("C301", msg)       # cross-block empties are not
        self.assertIn("497", msg)           # total missing count inside span

    def test_r304_grouped_per_component(self):
        from kicad_sch_reader import rules
        from kicad_sch_reader.model import PinInstance
        j101 = self._sym("J101", value="Conn", pins=[
            PinInstance(number="1", name="Pin_1", electrical_type="passive", pos=(10.0, 0.0)),
            PinInstance(number="2", name="Pin_2", electrical_type="passive", pos=(20.0, 0.0)),
            PinInstance(number="3", name="Pin_3", electrical_type="passive", pos=(30.0, 0.0)),
        ])
        u1 = self._sym("U1", value="Reg", pins=[
            PinInstance(number="4", name="EN", electrical_type="power_in", pos=(40.0, 0.0)),
        ])
        issues = rules.check_nc_pin_inventory(
            self._project([j101, u1], no_connects=[(10.0, 0.0), (20.0, 0.0), (40.0, 0.0)]))
        by_title = {(i.ref, i.title) for i in issues}
        grouped = [i for i in issues if i.ref == "J101"]
        self.assertEqual(len(grouped), 1, "connector NC pins collapse to one row")
        self.assertIn("2 个引脚", grouped[0].message)
        self.assertIn("1, 2", grouped[0].message)
        power = [i for i in issues if i.ref == "U1"]
        self.assertEqual(len(power), 1)
        self.assertEqual(power[0].severity, "warning")
        self.assertEqual(power[0].pin, "4")

    def test_r701_grouped_per_sheet(self):
        from kicad_sch_reader import rules
        syms = [self._sym("TP201", dnp=True), self._sym("TP202", dnp=True),
                self._sym("R5", value="1k", dnp=True)]
        issues = rules.check_dnp_inventory(self._project(syms))
        self.assertEqual(len(issues), 1)
        self.assertIn("3 个器件", issues[0].message)
        self.assertIn("2 个为测试点", issues[0].message)

    def test_erc_pin_attribution_bilingual(self):
        from kicad_sch_reader import rules
        base = {"severity": "warning", "type": "t", "description": "d", "title": "T"}
        for wording in ("Symbol U101 pin 5", "Symbol U101 引脚 5"):
            issues = rules.erc_markers_to_issues(
                [dict(base, items=[{"description": wording}])])
            self.assertEqual(len(issues), 1)
            self.assertEqual(issues[0].ref, "U101", wording)
            self.assertEqual(issues[0].pin, "5", wording)


class TestInterfaceDirection(unittest.TestCase):
    """R902: interface-direction semantics (naming-based; pin electrical
    types are reference-only and must never escalate severity)."""

    @staticmethod
    def _net(name, members, labels=()):
        from kicad_sch_reader.model import Net, PinNet
        pins = [PinNet(ref=m[0], pin_number=m[1], pin_name=m[2],
                       pin_type=m[3], sheet_path="/", lib_id="Device:R",
                       value="1k", footprint="") for m in members]
        return Net(name=name, pins=pins, labels=list(labels))

    def test_tx_tx_collision_warns(self):
        from kicad_sch_reader import rules
        net = self._net("MCU_UART_TX", [
            ("U1", "3", "UART3TX", "output"),
            ("U2", "5", "TXD", "output")])
        issues = rules.check_interface_direction(None, [net])
        kinds = [i.title for i in issues if i.code == "R902"]
        self.assertTrue(any("双发送" in t for t in kinds), kinds)
        for i in issues:
            self.assertNotEqual(i.severity, "error")  # declared evidence only

    def test_healthy_tx_to_rx_pair_passes(self):
        from kicad_sch_reader import rules
        net = self._net("MCU_UART_TX", [
            ("U1", "3", "PB10/UART3TX", "output"),
            ("U2", "5", "UART_RX", "input")])
        issues = rules.check_interface_direction(None, [net])
        self.assertEqual([i for i in issues if i.code == "R902"], [])

    def test_mosi_miso_swap_warns(self):
        from kicad_sch_reader import rules
        net = self._net("SPI_MOSI", [
            ("U1", "1", "MOSI", "output"),
            ("U2", "2", "MISO", "input")])
        issues = rules.check_interface_direction(None, [net])
        self.assertTrue(any("互换" in i.message for i in issues if i.code == "R902"))

    def test_type_conflict_stays_info(self):
        from kicad_sch_reader import rules
        net = self._net("DBG_UART_TX", [
            ("U1", "3", "TXD", "input"),
            ("U2", "5", "RX", "input")])
        issues = rules.check_interface_direction(None, [net])
        r902 = [i for i in issues if i.code == "R902"]
        self.assertTrue(r902)
        self.assertTrue(all(i.severity == "info" for i in r902))

    def test_direction_family_boundaries(self):
        from kicad_sch_reader.rules import direction_family as fam
        self.assertEqual(fam("MCU_UART_TX"), "tx")
        self.assertEqual(fam("PB10/UART3TX"), "tx")
        self.assertEqual(fam("/ADC_MISO"), "miso")
        self.assertIsNone(fam("IO_L1N_T0_D01_DIN_14"))  # config func, not direction
        self.assertIsNone(fam("TX_DISABLE"))            # control signal
        self.assertIsNone(fam("USBC1_RX1_P"))           # industry pin name (diff pair)
        self.assertIsNone(fam("MGTPRXN0_216"))   # RX inside token blocked
        self.assertIsNone(fam("CTX_BUFFER"))     # TX inside token blocked
        self.assertIsNone(fam("VCM_2V5"))


class TestAssessmentFixes(unittest.TestCase):
    """Regression tests for the 2026-09-17 SRB assessment fixes."""

    @classmethod
    def setUpClass(cls):
        cls.project = parser.load_project(MAINBOARD)
        cls.netlist = connectivity.build_netlist(cls.project)

    def test_report_exports_components_and_page_index(self):
        from kicad_sch_reader import report
        stats = report.project_stats(self.project, self.netlist, [])
        self.assertGreater(len(stats["components"]), 100)
        by_ref = {c["ref"]: c for c in stats["components"]}
        self.assertIn("J101", by_ref)
        self.assertTrue(by_ref["J101"]["value"])
        self.assertEqual(stats["sheets"][0]["page_no"], 1)

    def test_netfind_matches_hierarchical_alias(self):
        r = self.run_cli("netfind", str(MAINBOARD), "AFE_OUT_N")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("== GND ==", r.stdout)
        self.assertIn("AFE_OUT_N", r.stdout)

    def test_hierarchical_single_pin_is_info_not_warning(self):
        from kicad_sch_reader import rules
        from kicad_sch_reader.model import Net, PinNet
        net = Net(
            name="/ADC Channel Switch/PGIA_IN2+_CH2",
            hierarchical_names=["PGIA_IN2+_CH2"],
            pins=[PinNet(ref="U802", pin_number="5", pin_name="S1", pin_type="passive",
                         sheet_path="/4b194535", lib_id="Emoe:Switch", value="SW",
                         footprint="")],
        )
        issues = rules.check_single_pin_nets([net])
        self.assertEqual([i.code for i in issues], ["R302H"])
        self.assertEqual(issues[0].severity, "info")
        self.assertIn("层次/全局端口别名", issues[0].message)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "kicad-sch-reader.py"), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120, cwd=str(ROOT))
