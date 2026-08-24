"""Data model shared by parser, connectivity builder, rules and reports."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

Point = Tuple[float, float]


@dataclass
class LibPin:
    number: str
    name: str
    electrical_type: str
    pos: Point


@dataclass
class LibSymbol:
    lib_id: str
    # key = "<unit>_<body_style>" (for example "1_1")
    units: Dict[str, List[LibPin]] = field(default_factory=dict)

    def pins_for(self, unit: str, body_style: str) -> List[LibPin]:
        selected: List[LibPin] = []
        for key in (f"{unit}_{body_style}", f"{unit}_0", unit):
            if key in self.units:
                selected = self.units[key]
                break
        # Multi-unit symbols store shared power/common pins in the "0_*" unit;
        # those pins are electrically active on every placed unit.
        common: List[LibPin] = []
        for key in (f"0_{body_style}", "0_0", "0_1"):
            if key in self.units:
                common = self.units[key]
                break
        combined: Dict[str, LibPin] = {}
        for pin in common + selected:
            combined[pin.number] = pin
        if combined:
            return list(combined.values())
        # Any unit is better than nothing (rare malformed/legacy libraries).
        if self.units:
            return next(iter(self.units.values()))
        return []


@dataclass
class PinInstance:
    number: str
    name: str
    electrical_type: str
    pos: Point
    uuid: str = ""
    no_connect: bool = False
    net: Optional[str] = None


@dataclass
class SymbolInstance:
    ref: str
    value: str
    lib_id: str
    unit: str = "1"
    body_style: str = "1"
    pos: Point = (0.0, 0.0)
    rotation: float = 0.0
    mirror: str = ""
    uuid: str = ""
    in_bom: bool = True
    on_board: bool = True
    dnp: bool = False
    properties: Dict[str, str] = field(default_factory=dict)
    pins: List[PinInstance] = field(default_factory=list)
    sheet_path: str = "/"

    @property
    def footprint(self) -> str:
        return self.properties.get("Footprint", "")

    @property
    def is_power_symbol(self) -> bool:
        return self.lib_id.startswith("power:")


@dataclass
class Wire:
    p1: Point
    p2: Point
    uuid: str = ""


@dataclass
class Label:
    name: str
    pos: Point
    rotation: float = 0.0
    kind: str = "label"  # label | global_label | hierarchical_label
    shape: str = ""
    uuid: str = ""


@dataclass
class Junction:
    pos: Point
    uuid: str = ""


@dataclass
class NoConnect:
    pos: Point
    uuid: str = ""


@dataclass
class SchText:
    """Free text annotation on a page (design intent, not connectivity)."""

    content: str
    pos: Point
    rotation: float = 0.0
    kind: str = "text"  # text | textbox
    size: Tuple[float, float] = (0.0, 0.0)  # textbox width/height only
    uuid: str = ""


@dataclass
class SheetPin:
    name: str
    direction: str
    pos: Point


@dataclass
class SheetRef:
    """A hierarchical-sheet instance placed on a parent page."""

    name: str
    file: str
    pos: Point
    size: Tuple[float, float]
    uuid: str
    pins: List[SheetPin]
    paths: List[str] = field(default_factory=list)

    @property
    def first_path(self) -> str:
        return self.paths[0] if self.paths else f"/{self.uuid}"


@dataclass
class SheetData:
    path: str
    file: Path
    title: str = ""
    version: str = ""
    generator: str = ""
    # Raw title_block fields: title/date/rev/company/comment<N>.
    title_fields: Dict[str, str] = field(default_factory=dict)
    lib_symbols: Dict[str, LibSymbol] = field(default_factory=dict)
    symbols: List[SymbolInstance] = field(default_factory=list)
    wires: List[Wire] = field(default_factory=list)
    labels: List[Label] = field(default_factory=list)
    junctions: List[Junction] = field(default_factory=list)
    no_connects: List[NoConnect] = field(default_factory=list)
    sheets: List[SheetRef] = field(default_factory=list)
    texts: List[SchText] = field(default_factory=list)
    node_counts: Dict[str, int] = field(default_factory=dict)

    @property
    def is_root(self) -> bool:
        return self.path == "/"


@dataclass
class Project:
    root: Path
    sheets: Dict[str, SheetData] = field(default_factory=dict)
    files: List[Path] = field(default_factory=list)
    sheet_order: List[str] = field(default_factory=list)

    @property
    def root_sheet(self) -> Optional[SheetData]:
        return self.sheets.get("/")

    def all_symbols(self) -> List[SymbolInstance]:
        out: List[SymbolInstance] = []
        for path in self.sheet_order:
            sheet = self.sheets.get(path)
            if sheet:
                out.extend(sheet.symbols)
        return out


@dataclass
class PinNet:
    ref: str
    pin_number: str
    pin_name: str
    pin_type: str
    sheet_path: str
    lib_id: str
    value: str
    footprint: str


@dataclass
class Net:
    name: str
    code: str = ""
    sheet_paths: List[str] = field(default_factory=list)
    pins: List[PinNet] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    global_names: List[str] = field(default_factory=list)
    power_names: List[str] = field(default_factory=list)
    hierarchical_names: List[str] = field(default_factory=list)
    has_conflict: bool = False
    conflict_names: List[str] = field(default_factory=list)
    point_count: int = 0

    def pin_count(self, *, exclude_power_symbols: bool = False) -> int:
        if not exclude_power_symbols:
            return len(self.pins)
        return sum(1 for p in self.pins if not p.lib_id.startswith("power:"))

    def unique_sheet_paths(self) -> List[str]:
        return sorted({p.sheet_path for p in self.pins})


@dataclass
class Issue:
    code: str
    severity: str  # error | warning | info
    title: str
    message: str
    sheet_path: str = "/"
    ref: str = ""
    pin: str = ""
    net: str = ""
    details: Dict[str, str] = field(default_factory=dict)
    # Evidence level of the rule that raised this issue:
    #   official   - verbatim from kicad-cli ERC
    #   structural - directly checkable schematic fact (duplicate ref,
    #                floating pin, single-pin net ...)
    #   declared   - field-convention check (missing footprint/value)
    #   heuristic  - experience-based suggestion (decoupling proximity),
    #                configurable and safe to ignore after review
    evidence: str = ""

    def sort_key(self) -> tuple:
        order = {"error": 0, "warning": 1, "info": 2}
        return (order.get(self.severity, 9), self.sheet_path, self.ref or "", self.pin or "")
