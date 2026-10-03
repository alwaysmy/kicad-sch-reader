"""Small native KiCad fixture builder for optional official CLI tests."""
from uuid import uuid5, NAMESPACE_URL


def uid(text): return str(uuid5(NAMESPACE_URL, 'kicad-sch-reader/' + text))


def schematic(wires=(), pins=(), junctions=(), labels=(), nc=()):
    root=uid('root')
    forms=[f'''(kicad_sch (version 20250114) (generator "eeschema")
    (uuid "{root}") (paper "A4")
    (lib_symbols (symbol "Test:Pin" (in_bom yes) (on_board yes)
      (property "Reference" "J" (at 0 0 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Pin" (at 0 0 0) (effects (font (size 1.27 1.27))))
      (symbol "Pin_1_1" (pin passive line (at 0 0 0) (length 2.54)
       (name "P" (effects (font (size 1.27 1.27))))
       (number "1" (effects (font (size 1.27 1.27))))))))''']
    for i,(x,y) in enumerate(pins):
        ref='J'+str(i+1)
        forms.append(f'''(symbol (lib_id "Test:Pin") (at {x} {y} 0) (unit 1)
        (in_bom yes) (on_board yes) (dnp no) (uuid "{uid(ref)}")
        (property "Reference" "{ref}" (at {x} {y} 0) (effects (font (size 1.27 1.27))))
        (property "Value" "Pin" (at {x} {y} 0) (effects (font (size 1.27 1.27))))
        (pin "1" (uuid "{uid(ref+'pin')}"))
        (instances (project "synthetic" (path "/{root}" (reference "{ref}") (unit 1)))))''')
    for i,(a,b) in enumerate(wires):
        forms.append(f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid "{uid("wire"+str(i))}"))')
    for i,(x,y) in enumerate(junctions):
        forms.append(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid("junction"+str(i))}"))')
    for i,(name,x,y) in enumerate(labels):
        forms.append(f'(label "{name}" (at {x} {y} 0) (effects (font (size 1.27 1.27))) (uuid "{uid("label"+str(i))}"))')
    for i,(x,y) in enumerate(nc):
        forms.append(f'(no_connect (at {x} {y}) (uuid "{uid("nc"+str(i))}"))')
    forms.append('(sheet_instances (path "/" (page "1")))\n)')
    return '\n'.join(forms)
