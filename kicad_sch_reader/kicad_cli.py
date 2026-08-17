"""Bridge to the official ``kicad-cli`` executable.

``kicad-cli`` is used for authoritative ERC (JSON) and netlist/BOM exports.
The reader itself remains pure Python; if ``kicad-cli`` is unavailable every
feature except ``erc``/``bom-export``/``netlist-export`` still works.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class KicadCliError(RuntimeError):
    pass


def find_kicad_cli(explicit: Optional[str] = None) -> Optional[str]:
    if explicit:
        if Path(explicit).exists():
            return str(Path(explicit))
        raise KicadCliError(f"kicad-cli not found at {explicit}")
    env = os.environ.get("KICAD_CLI")
    if env and Path(env).exists():
        return env
    found = shutil.which("kicad-cli")
    if found:
        return found
    candidates = []
    roots = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "KiCad",
        Path(r"C:\Program Files\KiCad"),
    ]
    for root in roots:
        if root.exists():
            candidates.extend(sorted(root.glob("*/bin/kicad-cli.exe"), reverse=True))
    return str(candidates[0]) if candidates else None


def _run(args: List[str], timeout: int = 300) -> subprocess.CompletedProcess:
    exe = find_kicad_cli()
    if not exe:
        raise KicadCliError("kicad-cli executable not found (set KICAD_CLI or install KiCad)")
    proc = subprocess.run(
        [exe] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    if proc.returncode != 0 and "--exit-code-violations" not in args:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise KicadCliError(f"kicad-cli {' '.join(args)} failed: {detail}")
    return proc


def run_erc(root_sch, output_json: Optional[str] = None, severity: str = "all") -> List[dict]:
    """Run ERC and return the JSON report as a list of markers.

    *severity* may be ``all``, ``error`` or ``warning``.
    """
    tmp = output_json or str(Path(root_sch).with_suffix("").with_suffix(".erc.json"))
    args = ["sch", "erc", "--format", "json", "--severity-all", "--exit-code-violations"]
    args += ["-o", tmp, str(root_sch)]
    proc = _run(args)
    # With --exit-code-violations kicad-cli returns a non-zero code whenever
    # violations exist; that is a successful ERC run as far as we are concerned.
    del proc
    path = Path(tmp)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "markers" in data:
        return list(data["markers"])
    if isinstance(data, dict) and "sheets" in data:
        # KiCad 10 schema: violations live under sheets[].violations.
        flattened: List[dict] = []
        for sheet in data["sheets"]:
            for violation in sheet.get("violations", []):
                item = dict(violation)
                item.setdefault("sheet_path", sheet.get("path", ""))
                flattened.append(item)
        return flattened
    return []


def export_netlist(root_sch, output_file: Optional[str] = None, fmt: str = "kicadsexpr") -> Path:
    out = output_file or str(Path(root_sch).with_suffix(".net"))
    args = ["sch", "export", "netlist", "--format", fmt, "-o", out, str(root_sch)]
    proc = _run(args)
    if proc.returncode != 0:
        raise KicadCliError(proc.stderr.strip() or proc.stdout.strip())
    return Path(out)


def export_bom(root_sch, output_file: Optional[str] = None) -> Path:
    out = output_file or str(Path(root_sch).with_suffix(".bom.csv"))
    args = [
        "sch", "export", "bom",
        "--fields", "Reference,Value,Footprint,QUANTITY,DNP",
        "--labels", "Refs,Value,Footprint,Qty,DNP",
        "--group-by", "Value,Footprint",
        "--sort-field", "Reference",
        "-o", out,
        str(root_sch),
    ]
    proc = _run(args)
    if proc.returncode != 0:
        raise KicadCliError(proc.stderr.strip() or proc.stdout.strip())
    return Path(out)


def parse_erc_markers(markers: List[dict]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for m in markers:
        severity = str(m.get("severity", "unknown"))
        counts[severity] = counts.get(severity, 0) + 1
    return counts
