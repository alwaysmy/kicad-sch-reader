#!/usr/bin/env python3
"""Console entry point for the kicad-sch-reader package."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kicad_sch_reader.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
