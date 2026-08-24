"""Regression tests for LCEDA `.epro` CBB expansion.

The fixture is the real project under ``examples/LIA_DigitalBoard_RevA``.
When the fixture is missing (for example in a minimal CI checkout) the tests
are skipped.
"""

from __future__ import annotations

import subprocess
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
        # SHORT 桥别名保留原串，不再被覆盖为单一 canonical 名。
        self.assertIn("VCC_1V5", cbb1_ports["VOUT"]["parent_net"])
        self.assertIn("VCC_1V35_DDR", cbb1_ports["VOUT"]["parent_net"])
        vout_members = {(m["ref"], m["pin"]) for m in cbb1_ports["VOUT"]["internal_members"]}
        self.assertIn(("L5", "2"), vout_members)

    def test_trace_net_reaches_cbb_internal_devices(self):
        net_trace = self.report["trace_results"]["nets"]["VCC_1V5"]
        # 非 0Ω 的 L5(电感)保留为中间器件；工具不再把 VOUT 名传播到 U6.SW。
        self.assertTrue(any(m["ref"] == "L5" and m["module_instance"] == "CBB1"
                            for m in net_trace))
        self.assertTrue(any(m["ref"] == "CBB1" and m["pin"] == "VOUT" for m in net_trace))

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

    def test_diverse_part_names_and_duplicate_pin_keys_fixed(self):
        pm = self.report["pin_net_map"]

        def by_ref(ref):
            return {k.split("||")[2]: v for k, v in pm.items() if k.split("||")[1] == ref}

        u1 = by_ref("U1")
        self.assertGreater(len(u1), 300)
        self.assertEqual(u1.get("IO_L3P_T0_DQS_34"), "IO_L3P_T0_DQS_34")
        self.assertEqual(u1.get("DONE_0"), "FPGA_DONE")

        u3 = by_ref("U3")
        self.assertEqual(u3.get("PA13/SWDIO"), "MCU_SWDIO")
        self.assertEqual(u3.get("PA14/SWCLK"), "MCU_SWCLK")
        self.assertEqual(u3.get("PA9"), "MCU_UART_TX")
        self.assertEqual(u3.get("PB3"), "MCU_SPI_CLK")

        d10 = by_ref("D10")
        self.assertEqual(d10.get("IN#1"), "MCU_SWDIO")
        self.assertEqual(d10.get("IN#2"), "MCU_SWCLK")

        short = by_ref("SHORTe4381")
        self.assertEqual(short.get("Pin1#1"), "MCU_SPI_CS")
        self.assertEqual(short.get("Pin1#2"), "IO_L9P_T1_DQS_14")

    def test_pullup_resistor_not_merged_with_power_rail(self):
        pm = self.report["pin_net_map"]
        cbb3_vout4 = next(v for k, v in pm.items() if k.endswith("||CBB3||VOUT4"))
        self.assertEqual(cbb3_vout4, "VCC_3V3")
        bridges = {b["designator"]: b for b in self.report.get("component_bridges", [])}
        r26 = bridges.get("R26")
        self.assertIsNotNone(r26)
        self.assertFalse(r26["direct"])
        self.assertEqual(r26["kind"], "passive")
        self.assertIn("VCC_IOB0", (r26["net_a"], r26["net_b"]))
        # 1kΩ 上拉电阻另一侧不再被工具自动命名为 FPGA_DONE/VCC_IOB0；
        # 保留为未命名中间节点，由 LLM/人工判断。
        self.assertIn("", (r26["net_a"], r26["net_b"]))

    def test_lceda_reader_cli_accepts_epro(self):
        r = subprocess.run(
            [sys.executable, str(ROOT / "repos" / "lceda-sch-reader" / "lceda_reader.py"),
             "--eprj", str(EPRO), "boards"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
            cwd=str(ROOT))
        self.assertEqual(r.returncode, 0, r.stderr)
        # 上游 2026-08 重构后格式横幅移至 stderr（如
        # "[lceda_reader] 格式: 立创EDA .epro（V2 ZIP 导出）…"），
        # 且 stdout 按 [文件名] 前缀列出 boards。
        self.assertIn(".epro", r.stderr)
        self.assertIn("ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro", r.stdout)

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
