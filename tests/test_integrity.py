"""Self-contained connectivity/completeness regressions; no private fixtures."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from kicad_sch_reader import connectivity as c, parser, sexpr, kicad_cli
from kicad_sch_reader.model import *


def project(sheet):
    return Project(root=Path('.'), sheets={sheet.path: sheet}, sheet_order=[sheet.path])


def sym(ref, pos, path='/'):
    return SymbolInstance(ref=ref, value='test', lib_id='Test:Pin', sheet_path=path,
                          pins=[PinInstance('1','P','passive',pos)])


def members(nets):
    return {frozenset((p.sheet_path,p.ref,p.pin_number) for p in n.pins) for n in nets if n.pins}


LIB = '''(lib_symbols (symbol "Test:Pin" (symbol "Pin_1_1"
 (pin passive line (at 0 0 0) (length 1)
 (name "P" (effects (font (size 1 1))))
 (number "1" (effects (font (size 1 1))))))))'''
PLACED = '''(symbol (lib_id "Test:Pin") (at 10 10 0) (unit 1)
 (property "Reference" "R0") (property "Value" "test") (uuid "sym")
 (pin "1" (uuid "pin")) {instances})'''


class GeometryIntegrity(unittest.TestCase):
    def sheet(self, wires, positions):
        return SheetData(path='/', file=Path('synthetic.kicad_sch'),
                         wires=[Wire(*w) for w in wires],
                         symbols=[sym('R'+str(i+1),p) for i,p in enumerate(positions)])

    def test_t_endpoint_without_junction_stays_separate(self):
        s=self.sheet([((0,0),(10,0)),((5,0),(5,5))],[(0,0),(5,5)])
        self.assertEqual(len(members(c.build_netlist(project(s)))),2)

    def test_explicit_junction_connects_crossing_interiors(self):
        s=self.sheet([((0,0),(10,0)),((5,-5),(5,5))],[(0,0),(5,5)])
        s.junctions=[Junction((5,0))]
        self.assertEqual(len(members(c.build_netlist(project(s)))),1)

    def test_crossing_without_junction_stays_separate(self):
        s=self.sheet([((0,0),(10,0)),((5,-5),(5,5))],[(0,0),(5,5)])
        self.assertEqual(len(members(c.build_netlist(project(s)))),2)

    def test_wire_interior_pin_without_junction_is_not_connected(self):
        s=self.sheet([((0,0),(10,0))],[(0,0),(5,0)])
        nets=c.build_netlist(project(s))
        self.assertEqual(sum(len(n.pins) for n in nets),1)
        self.assertEqual(len(members(nets)),1)

    def test_nearby_label_must_not_snap(self):
        s=self.sheet([((0,0),(10,0))],[(0,0)])
        s.labels=[Label('NEAR',(5,0.005))]
        self.assertNotEqual(c.find_pin_net(c.build_netlist(project(s)),'R1','1').name,'/NEAR')

    def test_nc_marker_does_not_remove_wired_pin(self):
        s=self.sheet([((0,0),(10,0))],[(0,0),(10,0)])
        s.no_connects=[NoConnect((0,0))]
        nets=c.build_netlist(project(s))
        self.assertEqual(sum(len(n.pins) for n in nets),2)
        self.assertTrue(s.symbols[0].pins[0].no_connect)

    def test_isolated_nc_is_not_connected(self):
        s=self.sheet([],[(0,0)])
        s.no_connects=[NoConnect((0,0))]
        self.assertEqual(members(c.build_netlist(project(s))),set())


class ParseIntegrity(unittest.TestCase):
    def parse_text(self,text):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'test.kicad_sch'; p.write_text(text,encoding='utf-8')
            return parser.parse_sheet_file(p)

    def test_quoted_parentheses_are_atoms(self):
        self.assertEqual(sexpr.parse('(x "(" ")")'),[['x','(',')']])

    def test_bad_syntax_raises(self):
        for s in ['(x "unterminated)',')','(x))','(x']:
            with self.subTest(s=s),self.assertRaises(ValueError): sexpr.parse(s)

    def test_non_schematic_rejected(self):
        for s in ['', '(foo)', '(kicad_sch)(foo)']:
            with self.subTest(s=s),self.assertRaises(ValueError):self.parse_text(s)

    def test_missing_library_does_not_invent_origin_pins(self):
        with self.assertRaises(ValueError):
            self.parse_text('(kicad_sch '+PLACED.format(instances='')+')')

    def test_missing_instance_pin_records_do_not_drop_library_pins(self):
        placed=PLACED.format(instances='').replace('(pin "1" (uuid "pin"))','')
        s=self.parse_text('(kicad_sch '+LIB+placed+')')
        self.assertEqual([p.number for p in s.symbols[0].pins],['1'])

    def test_nested_instance_uses_full_path(self):
        node=sexpr.parse(PLACED.format(instances='''(instances (project "test"
          (path "/root/A/leaf" (reference "R101") (unit 1))
          (path "/root/B/leaf" (reference "R201") (unit 1))))'''))[0]
        lib=parser.parse_lib_symbols(sexpr.parse('(kicad_sch '+LIB+')')[0])
        a=parser.parse_symbol_instance(node,lib,'/A/leaf')
        b=parser.parse_symbol_instance(node,lib,'/B/leaf')
        self.assertEqual((a.ref,b.ref),('R101','R201'))


class ERCIntegrity(unittest.TestCase):
    def test_execution_failure_is_not_empty_success(self):
        with tempfile.TemporaryDirectory() as td:
            with patch.object(kicad_cli,'_run',return_value=subprocess.CompletedProcess([],3,'','load failed')):
                with self.assertRaises(kicad_cli.KicadCliError):
                    kicad_cli.run_erc(Path(td)/'bad.kicad_sch')

    def test_stale_report_not_reused(self):
        with tempfile.TemporaryDirectory() as td:
            output=Path(td)/'result.json';output.write_text('{"sheets":[]}')
            with patch.object(kicad_cli,'_run',return_value=subprocess.CompletedProcess([],0,'','')):
                with self.assertRaises(kicad_cli.KicadCliError):
                    kicad_cli.run_erc(Path(td)/'bad.kicad_sch',str(output))


class PartitionIntegrity(unittest.TestCase):
    def test_swapped_unnamed_groups_are_not_100_percent(self):
        from kicad_sch_reader.validation import compare_partitions
        a,b,c,d=[('/',ref,'1') for ref in ['R1','R2','R3','R4']]
        r=compare_partitions([{a,b},{c,d}],[{a,c},{b,d}])
        self.assertFalse(r['passed'])
        self.assertEqual((r['split_nets'],r['shorted_nets']),(2,2))
        self.assertEqual(r['partition_mismatch_pins'],4)

    def test_exact_partition_accepts_reordered_nets(self):
        from kicad_sch_reader.validation import compare_partitions
        a,b,c=[('/',ref,'1') for ref in ['R1','R2','R3']]
        self.assertTrue(compare_partitions([{a,b},{c}],[{c},{b,a}])['passed'])

    def test_missing_and_extra_fail(self):
        from kicad_sch_reader.validation import compare_partitions
        a,b,c=[('/',ref,'1') for ref in ['R1','R2','R3']]
        r=compare_partitions([{a,c}],[{a,b}])
        self.assertFalse(r['passed'])
        self.assertEqual((r['missing_pins'],r['extra_pins']),(1,1))

    def test_pin_cannot_be_on_two_nets(self):
        from kicad_sch_reader.validation import compare_partitions
        with self.assertRaises(ValueError):compare_partitions([{1},{1}],[{1}])

    def test_empty_is_not_verified(self):
        from kicad_sch_reader.validation import compare_partitions
        self.assertFalse(compare_partitions([],[])['passed'])

class HierarchyIntegrity(unittest.TestCase):
    def test_reused_nested_sheet_expands_once_per_parent(self):
        def ref(name,filename,uuid,paths):
            return f'''(sheet (at 0 0) (size 10 10) (uuid "{uuid}")
              (property "Sheetname" "{name}") (property "Sheetfile" "{filename}")
              (instances (project "root" {paths})))'''
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            root='(kicad_sch (uuid "root") '+ref('A','middle.kicad_sch','A','')+ref('B','middle.kicad_sch','B','')+')'
            middle='(kicad_sch (uuid "middle") '+ref('Leaf','leaf.kicad_sch','leaf','(path "/root/A/leaf" (page "4")) (path "/root/B/leaf" (page "5"))')+')'
            placed=PLACED.format(instances='''(instances (project "root"
              (path "/root/A/leaf" (reference "R101") (unit 1))
              (path "/root/B/leaf" (reference "R201") (unit 1))))''')
            leaf='(kicad_sch (uuid "source-leaf") '+LIB+placed+'(label "SIG" (at 10 10 0)))'
            for n,s in [('root',root),('middle',middle),('leaf',leaf)]:p.joinpath(n+'.kicad_sch').write_text(s)
            pr=parser.load_project(p/'root.kicad_sch');ns=c.build_netlist(pr)
            self.assertEqual(set(pr.sheets),{'/','/A','/B','/A/leaf','/B/leaf'})
            self.assertEqual({s.ref for s in pr.all_symbols()},{'R101','R201'})
            self.assertEqual({n.name for n in ns},{'/A/Leaf/SIG','/B/Leaf/SIG'})
            self.assertEqual(pr.sheets['/A/leaf'].page_no,4)
            self.assertEqual(pr.sheets['/B/leaf'].page_no,5)
            from kicad_sch_reader.circuit_ir import board_from_kicad
            board=board_from_kicad(pr,ns)
            self.assertEqual(board.pin_net('R101','1'),'/A/Leaf/SIG')
            self.assertEqual(board.pin_net('R201','1'),'/B/Leaf/SIG')

    def test_recursive_file_fails_instead_of_infinite_expansion(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'cycle.kicad_sch'
            f.write_text('(kicad_sch (uuid "root") (sheet (at 0 0) (uuid "child") (property "Sheetfile" "cycle.kicad_sch")))')
            with self.assertRaisesRegex(ValueError,'recursive'):parser.load_project(f)

    def test_ambiguous_ir_net_name_is_not_first_match(self):
        from kicad_sch_reader.circuit_ir import BoardIR,IRNet
        b=BoardIR('test','kicad','',nets=[IRNet('/SIG'),IRNet('/SIG')])
        with self.assertRaisesRegex(ValueError,'ambiguous'):b.net('/SIG')
        self.assertEqual(len(b.nets_named('/SIG')),2)

    def test_duplicate_unit_cannot_silently_collapse_in_ir(self):
        from kicad_sch_reader.circuit_ir import board_from_kicad
        s=SheetData(path='/',file=Path('synthetic'),symbols=[sym('R1',(0,0)),sym('R1',(10,0))])
        with self.assertRaisesRegex(ValueError,'ambiguous'):board_from_kicad(project(s))


class AdditionalERCIntegrity(unittest.TestCase):
    def report_runner(self, code, payload):
        def run(args):
            Path(args[args.index('-o')+1]).write_text(json.dumps(payload))
            return subprocess.CompletedProcess(args,code,'','')
        return run

    def test_valid_empty_and_violation_reports(self):
        cases=[(0,{'sheets':[]},0),(5,{'sheets':[{'path':'/','violations':[{'type':'pin_not_connected'}]}]},1)]
        for code,payload,count in cases:
            with self.subTest(code=code),patch.object(kicad_cli,'_run',side_effect=self.report_runner(code,payload)):
                self.assertEqual(len(kicad_cli.run_erc('synthetic.kicad_sch')),count)

    def test_invalid_report_schema_is_failure(self):
        for payload in [{}, {'sheets':[{}]}, {'markers':[1]}]:
            with self.subTest(payload=payload),patch.object(kicad_cli,'_run',side_effect=self.report_runner(0,payload)):
                with self.assertRaises(kicad_cli.KicadCliError):kicad_cli.run_erc('synthetic.kicad_sch')

    def test_failed_execution_does_not_replace_existing_report(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'existing.json';f.write_text('keep me')
            with patch.object(kicad_cli,'_run',side_effect=self.report_runner(3,{'sheets':[]})):
                with self.assertRaises(kicad_cli.KicadCliError):kicad_cli.run_erc('bad.kicad_sch',str(f))
            self.assertEqual(f.read_text(),'keep me')

    def test_report_json_records_incomplete_erc(self):
        from kicad_sch_reader.report import write_json
        s=SheetData(path='/',file=Path('synthetic'))
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'report.json'
            write_json(f,project(s),[],[],erc_status={'status':'failed','error':'bad input'})
            self.assertEqual(json.loads(f.read_text())['erc_status']['status'],'failed')


class MalformedGeometryIntegrity(unittest.TestCase):
    def test_bad_coordinates_do_not_become_zero(self):
        for text in ['(kicad_sch (wire (pts (xy bad 0) (xy 1 0))))',
                     '(kicad_sch (label "SIG"))',
                     '(kicad_sch (wire (pts (xy 0 0))))']:
            with tempfile.TemporaryDirectory() as td:
                p=Path(td)/'bad.kicad_sch';p.write_text(text)
                with self.assertRaises(ValueError):parser.load_project(p)

    def test_unknown_symbol_rotation_fails(self):
        with self.assertRaises(ValueError):parser.transform_point((1,2),45,'')

    def test_nc_conflict_remains_visible_to_pure_python_review(self):
        from kicad_sch_reader.rules import check_wired_no_connects
        s=SheetData(path='/',file=Path('synthetic'),symbols=[sym('R1',(0,0)),sym('R2',(10,0))],
                    wires=[Wire((0,0),(10,0))],no_connects=[NoConnect((0,0))])
        p=project(s);nets=c.build_netlist(p)
        self.assertEqual([i.code for i in check_wired_no_connects(p,nets)],['R305'])

    def test_hidden_electrical_nc_stack_is_not_a_network(self):
        pins=[PinInstance(str(i),'NC','no_connect',(0,0),hidden=True) for i in range(4)]
        s=SheetData(path='/',file=Path('synthetic'),symbols=[SymbolInstance('U1','IC','Test:IC',pins=pins)])
        self.assertEqual(c.build_netlist(project(s)),[])


class ScopedNameIntegrity(unittest.TestCase):
    def test_literal_slash_cannot_collide_with_hierarchy_separator(self):
        root=SheetData(path='/',file=Path('root'))
        root.sheets=[SheetRef('A/B','flat',(0,0),(1,1),'flat',[],paths=['/flat']),
                     SheetRef('A','a',(0,0),(1,1),'a',[],paths=['/a'])]
        middle=SheetData(path='/a',file=Path('a'))
        middle.sheets=[SheetRef('B','nested',(0,0),(1,1),'nested',[],paths=['/a/nested'])]
        flat=SheetData(path='/flat',file=Path('flat'),symbols=[sym('R1',(0,0),'/flat')],labels=[Label('S/G',(0,0))])
        nested=SheetData(path='/a/nested',file=Path('nested'),symbols=[sym('R2',(0,0),'/a/nested')],labels=[Label('S/G',(0,0))])
        p=Project(root=Path('.'),sheets={x.path:x for x in [root,middle,flat,nested]},sheet_order=['/','/a','/flat','/a/nested'])
        self.assertEqual({n.name for n in c.build_netlist(p)}, {'/A{slash}B/S{slash}G','/A/B/S{slash}G'})


class MultiUnitValidationIntegrity(unittest.TestCase):
    def multi_unit(self, root_page=1, child_page=2):
        a=sym('U1',(0,0));a.unit='2'
        b=sym('U1',(0,0),'/child');b.unit='1';b.pins[0].number='2'
        root=SheetData(path='/',file=Path('root'),symbols=[a],page_no=root_page)
        child=SheetData(path='/child',file=Path('child'),symbols=[b],page_no=child_page)
        return Project(root=Path('.'),sheets={'/':root,'/child':child},sheet_order=['/','/child'])

    def test_canonical_sheet_uses_page_order_not_unit(self):
        from kicad_sch_reader.validation import reader_partitions
        p=self.multi_unit()
        groups,_=reader_partitions(p,[],include_unconnected=True)
        self.assertEqual(set().union(*groups),{('/','U1','1'),('/','U1','2')})
        p=self.multi_unit(5,2)
        groups,_=reader_partitions(p,[],include_unconnected=True)
        self.assertEqual(set().union(*groups),{('/child','U1','1'),('/child','U1','2')})

    def test_ambiguous_multiunit_page_order_fails_explicitly(self):
        from kicad_sch_reader.validation import reader_partitions
        for pages in [(0,2),(1,1)]:
            with self.subTest(pages=pages),self.assertRaisesRegex(ValueError,'page order'):
                reader_partitions(self.multi_unit(*pages),[],include_unconnected=True)

    def test_board_diff_refuses_duplicate_net_names(self):
        from kicad_sch_reader.circuit_ir import BoardIR,IRNet,diff_boards
        a=BoardIR('old','kicad','',nets=[IRNet('/SIG'),IRNet('/SIG')])
        b=BoardIR('new','kicad','',nets=[IRNet('/SIG')])
        with self.assertRaisesRegex(ValueError,'ambiguous'):diff_boards(a,b)


class RootPageIntegrity(unittest.TestCase):
    def test_root_page_number_is_not_forced_to_one(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'root.kicad_sch'
            f.write_text('(kicad_sch (sheet_instances (path "/" (page "5"))))')
            self.assertEqual(parser.load_project(f).root_sheet.page_no,5)

if __name__=='__main__':unittest.main()
