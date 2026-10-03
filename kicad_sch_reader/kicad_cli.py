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
import tempfile
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
    accepted = {0, 5} if "--exit-code-violations" in args else {0}
    if proc.returncode not in accepted:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise KicadCliError(f"kicad-cli {' '.join(args)} failed: {detail}")
    return proc


def run_erc(root_sch, output_json: Optional[str] = None, severity: str = "all") -> List[dict]:
    """Run ERC and return the JSON report as a list of markers.

    *severity* may be ``all``, ``error`` or ``warning``.
    """
    if severity not in {"all", "error", "warning"}:
        raise ValueError(f"invalid ERC severity: {severity}")
    # A fresh temporary destination prevents reusing a report from an earlier
    # invocation, and does not write sidecars into the source project.
    with tempfile.TemporaryDirectory(prefix="kicad-erc-") as td:
        path = Path(td) / "report.json"
        args = ["sch", "erc", "--format", "json", f"--severity-{severity}",
                "--exit-code-violations", "-o", str(path), str(root_sch)]
        proc = _run(args)
        if proc.returncode not in (0, 5):
            raise KicadCliError(f"ERC execution failed ({proc.returncode}): {proc.stderr or proc.stdout}")
        if not path.is_file():
            raise KicadCliError("ERC produced no fresh JSON report")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list) and all(isinstance(v, dict) for v in data):
                markers = data
            elif isinstance(data, dict) and isinstance(data.get("markers"), list):
                markers = data["markers"]
            elif isinstance(data, dict) and isinstance(data.get("sheets"), list):
                markers = []
                for sheet in data["sheets"]:
                    violations = sheet["violations"]
                    if not isinstance(violations, list):
                        raise ValueError("violations must be a list")
                    for violation in violations:
                        item = dict(violation)
                        item.setdefault("sheet_path", sheet.get("path", ""))
                        markers.append(item)
            else:
                raise ValueError("unrecognized ERC report schema")
            if not all(isinstance(v, dict) for v in markers):
                raise ValueError("ERC markers must be objects")
            if proc.returncode == 5 and not markers:
                raise ValueError("ERC reports violations but contains no markers")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            raise KicadCliError(f"invalid ERC JSON report: {exc}") from exc
        if output_json is not None:
            Path(output_json).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        return markers


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
