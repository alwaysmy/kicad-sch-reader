"""Optional native-oracle regressions (KiCad 10+, no private project files)."""
import re
import tempfile
from pathlib import Path
import unittest

from kicad_sch_reader import parser, connectivity, kicad_cli
from kicad_sch_reader.validation import reader_partitions, official_partitions, compare_partitions
from tests.synthetic_kicad import schematic


class TestOfficialTopology(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not kicad_cli.find_kicad_cli():
            raise unittest.SkipTest('official KiCad CLI is not installed')
        version=kicad_cli._run(['--version']).stdout.strip()
        match=re.match(r'(\d+)\.',version)
        if not match or int(match.group(1)) < 10:
            raise unittest.SkipTest('native topology oracle requires KiCad 10+; set KICAD_CLI')

    def compare(self, **kwargs):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'synthetic.kicad_sch';f.write_text(schematic(**kwargs))
            official=kicad_cli.export_netlist(f,str(Path(td)/'official.net'))
            p=parser.load_project(f)
            a,_=reader_partitions(p,connectivity.build_netlist(p),include_unconnected=True)
            b,_=official_partitions(official,p.root_sheet.uuid,include_unconnected=True)
            result=compare_partitions(a,b)
            self.assertTrue(result['passed'],result)

    def test_t_without_junction(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4)),((38.1,25.4),(38.1,38.1))],
                     pins=[(25.4,25.4),(38.1,38.1)],labels=[('LEFT',25.4,25.4)])

    def test_t_with_junction(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4)),((38.1,25.4),(38.1,38.1))],
                     pins=[(25.4,25.4),(38.1,38.1)],junctions=[(38.1,25.4)])

    def test_crossing_without_junction(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4)),((38.1,12.7),(38.1,38.1))],
                     pins=[(25.4,25.4),(38.1,38.1)])

    def test_crossing_with_junction(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4)),((38.1,12.7),(38.1,38.1))],
                     pins=[(25.4,25.4),(38.1,38.1)],junctions=[(38.1,25.4)])

    def test_interior_pin_without_junction(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4))],pins=[(25.4,25.4),(38.1,25.4)])

    def test_interior_pin_with_junction(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4))],pins=[(25.4,25.4),(38.1,25.4)],
                     junctions=[(38.1,25.4)])

    def test_label_at_wire_interior(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4))],pins=[(25.4,25.4),(50.8,25.4)],
                     labels=[('SIG',38.1,25.4)])

    def test_label_near_wire_does_not_snap(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4))],pins=[(25.4,25.4),(50.8,25.4)],
                     labels=[('SIG',38.1,25.405),('LEFT',25.4,25.4)])

    def test_wired_pin_retains_nc_annotation(self):
        self.compare(wires=[((25.4,25.4),(50.8,25.4))],pins=[(25.4,25.4),(50.8,25.4)],
                     nc=[(25.4,25.4)],labels=[('SIG',25.4,25.4)])

    def test_isolated_nc(self):
        self.compare(pins=[(25.4,25.4)],nc=[(25.4,25.4)])

    def test_diagonal_junction(self):
        self.compare(wires=[((25.4,25.4),(50.8,50.8)),((25.4,50.8),(50.8,25.4))],
                     pins=[(25.4,25.4),(25.4,50.8)],junctions=[(38.1,38.1)])

    def test_official_erc_violation_return_is_successful_report(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'synthetic.kicad_sch';f.write_text(schematic(pins=[(25.4,25.4)]))
            markers=kicad_cli.run_erc(f)
            self.assertTrue(markers)
            self.assertTrue(any(m.get('type')=='pin_not_connected' for m in markers))

if __name__=='__main__':unittest.main()
