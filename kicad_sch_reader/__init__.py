"""kicad-sch-reader — pure-Python KiCad schematic reader and design-review tool."""

from .parser import load_project, parse_sheet_file, resolve_root_file
from .connectivity import build_netlist
from . import rules, report

__version__ = "0.1.0"
__all__ = ["load_project", "parse_sheet_file", "resolve_root_file", "build_netlist", "rules", "report", "__version__"]
