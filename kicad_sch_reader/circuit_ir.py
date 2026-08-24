"""Source-format-neutral Circuit IR shared by KiCad and LCEDA analyses.

Design notes (adopted from the ChatGPT architecture review):

* parsers stay format-specific and produce native models;
* ``BoardIR`` is the single analysis-facing graph (components / nets / pins /
  connections) that both the KiCad and the LCEDA adapter emit;
* net kind is one of ``signal`` / ``power`` / ``ground`` / ``interface`` and
  is derived structurally first, then by naming convention;
* cross-board links and findings carry evidence and confidence instead of
  bare booleans, so LLM/human reviewers can distinguish *calculated* facts
  from *declared* or *inferred* facts.

The module is intentionally dependency-free: it works from a KiCad
``Project`` + netlist, and from the JSON-shaped ``report`` produced by
``scripts/lceda_epro_review.py``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from . import connectivity
from .model import Net as KiCadNet
from .model import Project as KiCadProject

# ---------------------------------------------------------------------------
# constants

NET_SIGNAL = "signal"
NET_POWER = "power"
NET_GROUND = "ground"
NET_INTERFACE = "interface"

EVIDENCE_DIRECT = "direct"
EVIDENCE_CALCULATED = "calculated"
EVIDENCE_DATASHEET = "datasheet"
EVIDENCE_DECLARED = "declared"
EVIDENCE_INFERRED = "inferred"
EVIDENCE_AI = "ai"

CONFIDENCE_CONFIRMED = "confirmed"
CONFIDENCE_DETECTED = "detected"
CONFIDENCE_CANDIDATE = "candidate"
CONFIDENCE_INFERRED = "inferred"
CONFIDENCE_DECLARED = "declared"

CONNECTOR_REF_RE = re.compile(r"^(CN|J|P|H|CON|USB)\d+", re.IGNORECASE)
CONNECTOR_KEYWORDS = ("connector", "header", "wafer", "socket", "barrel",
                      "type-c", "typec", "btb")
GROUND_NAMES = {
    "GND", "AGND", "DGND", "PGND", "SGND", "MGND", "GNDA", "GNDD",
    "EARTH", "SHIELD", "CHASSIS",
}
_POWER_NAME_RE = re.compile(
    r"^(VCC|VDD|VSS|VEE|VBUS|VBAT|PWR|VREF|VPP|AVDD|DVDD|PVDD|"
    r"VDDIO|VCORE|VTT|VAA|VIO|VPLL|VDDA|VSSA|PWREN|PGOOD)",
    re.IGNORECASE,
)


def normalize_net(name: Optional[str]) -> str:
    """Normalise a net name for cross-board comparison.

    KiCad hierarchical prefixes ``/Sheet/Name`` are reduced to their leaf,
    LCEDA ``A,B`` short-bridge aliases are reduced to the first member, and
    case / separators are ignored.  Comparison of normalized names is only
    *candidate* evidence; it never proves a physical board-to-board link.
    """
    if not name:
        return ""
    text = str(name).strip()
    if "/" in text:
        text = text.rsplit("/", 1)[-1]
    text = text.split(",")[0].strip()
    normalized = re.sub(r"[^0-9A-Za-z+#.]", "", text).upper()
    # LCEDA 的 GND 展平名通常为 DXN_0，跨工具对比时归一化为 GND。
    if normalized == "DXN_0":
        return "GND"
    return normalized


def is_connector_ref(ref: str) -> bool:
    return bool(CONNECTOR_REF_RE.match(ref or ""))


def _looks_like_connector(ref: str, lib_id: str, pin_count: int) -> bool:
    lib = (lib_id or "").lower()
    if "testpoint" in lib:
        return False
    if "conn" in lib:
        return True
    if any(key in lib for key in CONNECTOR_KEYWORDS):
        return True
    return is_connector_ref(ref) and pin_count >= 2


def _looks_like_lceda_connector(ref: str, device: str, pin_count: int) -> bool:
    device_l = (device or "").lower()
    if is_connector_ref(ref):
        return True
    if any(key in device_l for key in CONNECTOR_KEYWORDS):
        return True
    return pin_count >= 4 and bool(
        re.search(r"\d+P|PIN|HDR|BTB", device or "", re.IGNORECASE)
    )


def _is_ground_name(name: str) -> bool:
    normalized = normalize_net(name)
    return normalized in GROUND_NAMES


# ---------------------------------------------------------------------------
# IR model


@dataclass
class IRNetMember:
    """One component pin participating in a net."""

    ref: str
    pin: str
    sheet: str = ""
    pin_name: str = ""
    pin_type: str = ""
    device: str = ""
    footprint: str = ""
    module_instance: str = ""

    def to_dict(self) -> dict:
        return {
            "ref": self.ref,
            "pin": self.pin,
            "sheet": self.sheet,
            "pin_name": self.pin_name,
            "pin_type": self.pin_type,
            "device": self.device,
            "footprint": self.footprint,
            "module_instance": self.module_instance,
        }


@dataclass
class IRNet:
    """A board-scope electrical net in the universal IR."""

    name: str
    kind: str = NET_SIGNAL
    members: List[IRNetMember] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    has_conflict: bool = False
    conflict_names: List[str] = field(default_factory=list)

    @property
    def pin_count(self) -> int:
        return len(self.members)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "kind": self.kind,
            "pin_count": self.pin_count,
            "labels": list(self.labels),
            "sources": list(self.sources),
            "has_conflict": self.has_conflict,
            "conflict_names": list(self.conflict_names),
            "members": [m.to_dict() for m in self.members],
        }


@dataclass
class IRComponentPin:
    number: str
    name: str = ""
    electrical_type: str = ""
    net: Optional[str] = None
    sheet: str = ""

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "name": self.name,
            "electrical_type": self.electrical_type,
            "net": self.net,
            "sheet": self.sheet,
        }


@dataclass
class IRComponent:
    """A physical designator in board scope.

    Multi-unit symbols and CBB-internal parts are collapsed to one node keyed
    by designator; pins retain their originating sheet.
    """

    ref: str
    value: str = ""
    lib_id: str = ""
    footprint: str = ""
    sheet: str = ""
    module_instance: str = ""
    role: str = "component"
    properties: Dict[str, str] = field(default_factory=dict)
    pins: Dict[str, IRComponentPin] = field(default_factory=dict)

    @property
    def connected_pins(self) -> Dict[str, str]:
        return {p: pin.net for p, pin in self.pins.items() if pin.net}

    def add_pin(self, pin: IRComponentPin) -> None:
        # Later sheets/units win only when the earlier entry has no net.
        old = self.pins.get(pin.number)
        if old is None or (old.net is None and pin.net is not None):
            self.pins[pin.number] = pin
        elif old.sheet == "" and pin.sheet:
            self.pins[pin.number] = pin

    def to_dict(self) -> dict:
        return {
            "ref": self.ref,
            "value": self.value,
            "lib_id": self.lib_id,
            "footprint": self.footprint,
            "sheet": self.sheet,
            "module_instance": self.module_instance,
            "role": self.role,
            "properties": dict(self.properties),
            "pins": {p: pin.to_dict() for p, pin in sorted(self.pins.items())},
        }


@dataclass
class IREvidence:
    """Why a finding/link is claimed, and how much trust it deserves."""

    kind: str = EVIDENCE_CALCULATED  # direct|calculated|datasheet|declared|inferred|ai
    source: str = ""
    note: str = ""
    confidence: str = CONFIDENCE_DETECTED

    def to_dict(self) -> dict:
        return {"kind": self.kind, "source": self.source,
                "note": self.note, "confidence": self.confidence}


@dataclass
class IRFinding:
    """Universal finding object; parsers/rules emit this instead of ad-hoc dicts."""

    code: str
    severity: str  # error | warning | info
    title: str
    message: str
    sheet: str = "/"
    ref: str = ""
    pin: str = ""
    net: str = ""
    details: Dict[str, str] = field(default_factory=dict)
    evidence: IREvidence = field(default_factory=IREvidence)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "severity": self.severity,
            "title": self.title,
            "message": self.message,
            "sheet": self.sheet,
            "ref": self.ref,
            "pin": self.pin,
            "net": self.net,
            "details": dict(self.details),
            "evidence": self.evidence.to_dict(),
        }


@dataclass
class BoardIR:
    """One schematic/board project normalised into the universal IR."""

    name: str
    format: str  # kicad | lceda
    source: str
    components: List[IRComponent] = field(default_factory=list)
    nets: List[IRNet] = field(default_factory=list)
    metadata: Dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._by_ref: Dict[str, IRComponent] = {}
        for comp in self.components:
            self._by_ref.setdefault(comp.ref, comp)
        self._net_by_name: Dict[str, IRNet] = {}
        for net in self.nets:
            self._net_by_name.setdefault(net.name, net)

    @property
    def component_count(self) -> int:
        return len(self.components)

    @property
    def net_count(self) -> int:
        return len(self.nets)

    def component(self, ref: str) -> Optional[IRComponent]:
        return self._by_ref.get(ref)

    def net(self, name: str) -> Optional[IRNet]:
        return self._net_by_name.get(name)

    def pin_net(self, ref: str, pin: str) -> Optional[str]:
        comp = self._by_ref.get(ref)
        if comp is None:
            return None
        irpin = comp.pins.get(pin)
        return irpin.net if irpin else None

    def connectors(self) -> Dict[str, dict]:
        """Return the board's connector view used by cross-board checks."""
        out: Dict[str, dict] = {}
        for ref, comp in sorted(self._by_ref.items()):
            connected = comp.connected_pins
            if not connected:
                continue
            if self.format == "lceda":
                looks = _looks_like_lceda_connector(ref, comp.lib_id, len(connected))
            else:
                looks = _looks_like_connector(ref, comp.lib_id, len(connected))
            if looks and len(connected) >= 2:
                out[ref] = {
                    "ref": ref,
                    "lib_id": comp.lib_id,
                    "sheet": comp.sheet,
                    "pin_count": len(connected),
                    "pins": {
                        str(p): n for p, n in sorted(
                            connected.items(), key=lambda kv: (len(kv[0]), kv[0])
                        )
                    },
                }
        return out

    def connector_view(self) -> dict:
        return {
            "name": self.name,
            "format": self.format,
            "root": self.source,
            "connectors": self.connectors(),
        }

    def to_dict(self, *, include_members: bool = True) -> dict:
        return {
            "name": self.name,
            "format": self.format,
            "source": self.source,
            "component_count": self.component_count,
            "net_count": self.net_count,
            "metadata": {k: v for k, v in self.metadata.items()},
            "components": [c.to_dict() for c in self.components],
            "nets": [n.to_dict() for n in self.nets if include_members or n.name],
        }


@dataclass
class IRCrossLink:
    """Candidate or detected physical connection between two board connectors."""

    a_board: str
    a_format: str
    a_ref: str
    a_lib: str
    b_board: str
    b_format: str
    b_ref: str
    b_lib: str
    common_pins: int
    exact_pins: int
    diff_count: int
    score: float
    confidence: str
    diffs: List[dict] = field(default_factory=list)
    evidence: IREvidence = field(default_factory=IREvidence)

    def to_dict(self) -> dict:
        return {
            "a_board": self.a_board,
            "a_format": self.a_format,
            "a_ref": self.a_ref,
            "a_lib": self.a_lib,
            "b_board": self.b_board,
            "b_format": self.b_format,
            "b_ref": self.b_ref,
            "b_lib": self.b_lib,
            "common_pins": self.common_pins,
            "exact_pins": self.exact_pins,
            "diff_count": self.diff_count,
            "score": self.score,
            "confidence": self.confidence,
            "diffs": self.diffs,
            "evidence": self.evidence.to_dict(),
        }


@dataclass
class IRSystem:
    """Multi-board project layer: boards plus cross-board links."""

    boards: List[BoardIR] = field(default_factory=list)
    links: List[IRCrossLink] = field(default_factory=list)
    declared_links: List[Tuple[str, str, str, str]] = field(default_factory=list)

    def add_board(self, board: BoardIR) -> None:
        self.boards.append(board)

    def compare_all(self, min_common: int = 2) -> List[IRCrossLink]:
        rows: List[IRCrossLink] = []
        for i, a in enumerate(self.boards):
            for j, b in enumerate(self.boards):
                if i >= j:
                    continue
                rows.extend(compare_boards(a, b, min_common=min_common))
        rows.sort(key=lambda r: (-r.score, -r.common_pins, r.a_board, r.b_board))
        self.links = rows
        return rows

    def to_payload(self) -> dict:
        return {
            "boards": [b.connector_view() for b in self.boards],
            "connections": [r.to_dict() for r in self.links],
        }


# ---------------------------------------------------------------------------
# net classification


def classify_net(name: str, power_names: Iterable[str] = (),
                 members: Iterable[IRNetMember] = (),
                 power_predicate=None) -> str:
    """Structural first, naming convention second.

    1. exact ground names -> ``ground``;
    2. explicit power-symbol/power-pin evidence -> ``power``;
    3. connector/module members -> ``interface``;
    4. naming fallback (or caller predicate for LCEDA) -> ``power``;
    5. otherwise ``signal``.
    """
    text = str(name or "")
    if _is_ground_name(text):
        return NET_GROUND
    member_list = list(members)
    if power_names:
        return NET_POWER
    for member in member_list:
        if str(member.pin_type or "").lower().startswith("power"):
            return NET_POWER
    if any(m.module_instance for m in member_list) or any(
        is_connector_ref(m.ref) for m in member_list
    ):
        return NET_INTERFACE
    if power_predicate is not None and power_predicate(text):
        return NET_POWER
    if _POWER_NAME_RE.match(text):
        return NET_POWER
    return NET_SIGNAL


# ---------------------------------------------------------------------------
# adapters


def board_from_kicad(project: KiCadProject, netlist: Optional[List[KiCadNet]] = None,
                     name: Optional[str] = None) -> BoardIR:
    """Adapt a parsed KiCad ``Project`` into ``BoardIR``."""
    nets = netlist if netlist is not None else connectivity.build_netlist(project)
    pin_net = {
        (p.sheet_path, p.ref, p.pin_number): n.name
        for n in nets for p in n.pins
    }

    comp_by_ref: Dict[str, IRComponent] = {}
    symbol_meta: Dict[Tuple[str, str], Tuple[str, str, str]] = {}
    for sym in project.all_symbols():
        ref = sym.ref
        if not ref or ref.startswith("#"):
            continue
        comp = comp_by_ref.get(ref)
        if comp is None:
            comp = IRComponent(
                ref=ref,
                value=sym.value,
                lib_id=sym.lib_id,
                footprint=sym.footprint,
                sheet=sym.sheet_path,
                role="power_symbol" if sym.is_power_symbol else "component",
                properties=dict(sym.properties),
            )
            comp_by_ref[ref] = comp
        symbol_meta[(sym.sheet_path, ref)] = (sym.value, sym.footprint, sym.lib_id)
        for pin in sym.pins:
            net = pin_net.get((sym.sheet_path, ref, pin.number))
            comp.add_pin(IRComponentPin(
                number=pin.number,
                name=pin.name,
                electrical_type=pin.electrical_type,
                net=net,
                sheet=sym.sheet_path,
            ))

    ir_nets: List[IRNet] = []
    for net in nets:
        members = []
        for p in net.pins:
            value, footprint, _ = symbol_meta.get(
                (p.sheet_path, p.ref), ("", "", ""))
            members.append(IRNetMember(
                ref=p.ref,
                pin=p.pin_number,
                sheet=p.sheet_path,
                pin_name=p.pin_name,
                pin_type=p.pin_type,
                device=value,
                footprint=footprint,
            ))
        power_names = [n for n in (net.power_names or []) if n]
        kind = classify_net(net.name, power_names=power_names, members=members)
        ir_nets.append(IRNet(
            name=net.name,
            kind=kind,
            members=members,
            labels=list(net.labels or []),
            sources=list(net.power_names or []),
            has_conflict=net.has_conflict,
            conflict_names=list(net.conflict_names or []),
        ))

    return BoardIR(
        name=name or project.root.name,
        format="kicad",
        source=str(project.root),
        components=sorted(comp_by_ref.values(), key=lambda c: (len(c.ref), c.ref)),
        nets=ir_nets,
        metadata={"sheet_count": len(project.sheets)},
    )


def board_from_lceda(report: dict, name: Optional[str] = None,
                     power_net_patterns: Optional[List[str]] = None) -> BoardIR:
    """Adapt the JSON-shaped LCEDA review report into ``BoardIR``.

    ``report`` is the dictionary returned by
    ``scripts.lceda_epro_review.review_epro``.  Parsing of the original
    ``.epro`` remains the job of that format-specific adapter; this function
    only performs the lossless-enough normalisation to the shared graph.
    """
    pin_entries: Dict[Tuple[str, str, str], str] = {}
    for key, net in (report.get("pin_net_map") or {}).items():
        parts = str(key).split("||", 2)
        if len(parts) != 3:
            continue
        sheet, ref, pin = parts
        pin_entries[(sheet, ref, pin)] = str(net or "")

    comp_meta: Dict[str, dict] = {}
    for comp in report.get("flat_components") or []:
        ref = str(comp.get("designator") or "")
        if not ref:
            continue
        meta = comp_meta.get(ref)
        if meta is None:
            meta = {
                "value": comp.get("value") or comp.get("device_title")
                or comp.get("title") or "",
                "lib_id": comp.get("device_title") or comp.get("value")
                or comp.get("title") or "",
                "footprint": comp.get("footprint") or "",
                "sheet": comp.get("sheet") or "",
                "module_instance": comp.get("module_instance") or "",
            }
            comp_meta[ref] = meta
        elif not meta["module_instance"] and comp.get("module_instance"):
            meta["module_instance"] = comp.get("module_instance")

    extra_patterns = [re.compile(p) for p in (power_net_patterns or [])]

    def lceda_power_predicate(name: str) -> bool:
        if not name:
            return False
        try:  # optional dependency: lceda-sch-reader checkout
            from lceda_reader import POWER_NET_RE  # type: ignore
            if POWER_NET_RE.match(name):
                return True
        except Exception:
            pass
        if _POWER_NAME_RE.match(name):
            return True
        if name.split(",")[0].strip().upper() in (
            "GND", "AGND", "DGND", "VCC", "VDD", "VSS", "VBUS", "PWR", "VREF"
        ):
            return True
        return any(p.search(name) for p in extra_patterns)

    # 1) Physical designators from the review's flattened component list.
    #    The raw pin map also contains SHORT-bridge and CBB-symbol designators;
    #    those are graph *markers*, not physical parts, and are added separately.
    components: Dict[str, IRComponent] = {}
    for ref, meta in comp_meta.items():
        components[ref] = IRComponent(
            ref=ref,
            value=str(meta.get("value") or ""),
            lib_id=str(meta.get("lib_id") or ""),
            footprint=str(meta.get("footprint") or ""),
            sheet=str(meta.get("sheet") or ""),
            module_instance=str(meta.get("module_instance") or ""),
            role="module" if meta.get("module_instance") else "component",
        )

    # 2) CBB symbols are hierarchy/interface nodes in the IR graph.
    for mod in report.get("cbb_modules") or []:
        ref = str(mod.get("designator") or "")
        if not ref:
            continue
        comp = components.get(ref) or IRComponent(
            ref=ref, sheet=str(mod.get("sheet") or ""),
            lib_id=str(mod.get("module") or ""), role="module")
        comp.role = "module"
        comp.lib_id = str(mod.get("module") or comp.lib_id)
        comp.sheet = str(mod.get("sheet") or comp.sheet)
        for pin_name in mod.get("pins") or []:
            net = (mod.get("port_nets") or {}).get(pin_name)
            comp.add_pin(IRComponentPin(
                number=str(pin_name), name=str(pin_name),
                electrical_type="", net=net or None, sheet=comp.sheet,
            ))
        components[ref] = comp

    # 3) Attach canonical pin->net entries to known components.
    for (sheet, ref, pin), net in pin_entries.items():
        if ref.startswith("SHORT"):
            continue
        comp = components.get(ref)
        if comp is None:
            continue
        comp.add_pin(IRComponentPin(
            number=pin, name=pin, electrical_type="", net=net or None, sheet=sheet,
        ))

    members_by_net: Dict[str, List[IRNetMember]] = {}
    for (sheet, ref, pin), net in pin_entries.items():
        if not net or ref.startswith("SHORT"):
            continue
        meta = comp_meta.get(ref, {})
        members_by_net.setdefault(net, []).append(IRNetMember(
            ref=ref,
            pin=pin,
            sheet=sheet,
            pin_name=pin,
            device=str(meta.get("value") or ""),
            footprint=str(meta.get("footprint") or ""),
            module_instance=str(meta.get("module_instance") or ""),
        ))

    ir_nets = []
    for net_name, members in sorted(members_by_net.items()):
        kind = classify_net(
            net_name, members=members, power_predicate=lceda_power_predicate
        )
        ir_nets.append(IRNet(name=net_name, kind=kind, members=members))

    return BoardIR(
        name=name or str(report.get("board") or "lceda-board"),
        format="lceda",
        source=str(report.get("epro") or ""),
        components=sorted(components.values(), key=lambda c: (len(c.ref), c.ref)),
        nets=ir_nets,
        metadata={
            "pages": report.get("pages") or 0,
            "finding_count": len(report.get("findings") or []),
            "flat_component_count": report.get("flat_component_count") or 0,
        },
    )


# ---------------------------------------------------------------------------
# cross-board comparison


def compare_boards(a: BoardIR, b: BoardIR, min_common: int = 2) -> List[IRCrossLink]:
    """Compare connector pin-net maps of two ``BoardIR`` instances.

    Equal *normalized* net names are only candidate evidence: the same pin
    number and the same name can be accidental.  ``score == 1.0`` with at
    least two pins is reported as ``detected``, never ``confirmed``.
    """
    rows: List[IRCrossLink] = []
    for ref_a, ca in sorted(a.connectors().items()):
        for ref_b, cb in sorted(b.connectors().items()):
            common = sorted(set(ca["pins"]) & set(cb["pins"]))
            if len(common) < min_common:
                continue
            exact = 0
            diffs = []
            for pin in common:
                na = normalize_net(ca["pins"].get(pin))
                nb = normalize_net(cb["pins"].get(pin))
                if na and na == nb:
                    exact += 1
                else:
                    diffs.append({
                        "pin": pin,
                        "a_net": ca["pins"].get(pin),
                        "b_net": cb["pins"].get(pin),
                    })
            score = round(exact / len(common), 4) if common else 0.0
            confidence = CONFIDENCE_DETECTED if score >= 1.0 and exact >= 2 \
                else CONFIDENCE_CANDIDATE
            rows.append(IRCrossLink(
                a_board=a.name, a_format=a.format, a_ref=ref_a, a_lib=ca["lib_id"],
                b_board=b.name, b_format=b.format, b_ref=ref_b, b_lib=cb["lib_id"],
                common_pins=len(common), exact_pins=exact,
                diff_count=len(diffs), score=score, confidence=confidence,
                diffs=diffs[:20],
                evidence=IREvidence(
                    kind=EVIDENCE_CALCULATED,
                    source="pin-net-name comparison",
                    note="normalized net names; candidate unless score==1.0",
                    confidence=confidence,
                ),
            ))
    rows.sort(key=lambda r: (-r.score, -r.common_pins, r.a_board, r.b_board))
    return rows


def diff_boards(old: "BoardIR", new: "BoardIR") -> dict:
    """Version diff between two revisions of the same design lineage.

    Components compare by designator (value / footprint / pin-count), nets by
    name with member-set changes.  Unnamed ``N$`` nets are unstable across
    revisions, so same-member add/remove pairs are reported as
    ``nets_renamed_candidates`` instead of hard adds/removes.  The result is a
    *candidate* statement about two files — deciding that they really are
    consecutive revisions is design knowledge.
    """

    def comp_snapshot(c: IRComponent) -> dict:
        return {
            "ref": c.ref,
            "value": c.value or "",
            "lib_id": c.lib_id or "",
            "footprint": c.footprint or "",
            "pin_count": len(c.pins),
        }

    comps_old = {c.ref: c for c in old.components}
    comps_new = {c.ref: c for c in new.components}
    comps_added = [comp_snapshot(comps_new[r]) for r in sorted(set(comps_new) - set(comps_old))]
    comps_removed = [comp_snapshot(comps_old[r]) for r in sorted(set(comps_old) - set(comps_new))]
    comps_changed = []
    for ref in sorted(set(comps_old) & set(comps_new)):
        ca, cb = comp_snapshot(comps_old[ref]), comp_snapshot(comps_new[ref])
        changes = {k: [ca[k], cb[k]] for k in ("value", "lib_id", "footprint", "pin_count")
                   if ca[k] != cb[k]}
        if changes:
            comps_changed.append({"ref": ref, "changes": changes})

    def net_members(n: IRNet) -> frozenset:
        return frozenset((m.ref, m.pin) for m in n.members)

    def net_summary(n: IRNet) -> dict:
        return {"name": n.name, "pin_count": len(n.members),
                "members": sorted(f"{m.ref}.{m.pin}" for m in n.members)[:24]}

    nets_old = old._net_by_name
    nets_new = new._net_by_name
    added_names = set(nets_new) - set(nets_old)
    removed_names = set(nets_old) - set(nets_new)

    members_to_removed = {}
    for r in removed_names:
        members_to_removed.setdefault(net_members(nets_old[r]), []).append(r)
    renamed_candidates = []
    renamed_old: set = set()
    renamed_new: set = set()
    for r in sorted(added_names):
        key = net_members(nets_new[r])
        for old_name in members_to_removed.get(key, []):
            renamed_candidates.append({"old": old_name, "new": r,
                                       "member_count": len(nets_new[r].members)})
            renamed_old.add(old_name)
            renamed_new.add(r)
            break
    # Keep the inventories consistent with the summary: pairs matched as
    # rename candidates appear only under nets_renamed_candidates.
    nets_added = [net_summary(nets_new[r]) for r in sorted(added_names - renamed_new)]
    nets_removed = [net_summary(nets_old[r]) for r in sorted(removed_names - renamed_old)]

    nets_changed = []
    for name in sorted(set(nets_old) & set(nets_new)):
        mo, mn = net_members(nets_old[name]), net_members(nets_new[name])
        if mo == mn:
            continue
        gained = sorted(f"{ref}.{pin}" for ref, pin in (mn - mo))
        lost = sorted(f"{ref}.{pin}" for ref, pin in (mo - mn))
        nets_changed.append({
            "name": name,
            "gained": gained[:24],
            "lost": lost[:24],
            "gained_count": len(gained),
            "lost_count": len(lost),
        })

    return {
        "old": old.source, "new": new.source,
        "summary": {
            "components_added": len(comps_added),
            "components_removed": len(comps_removed),
            "components_changed": len(comps_changed),
            "nets_added": len(nets_added),
            "nets_removed": len(nets_removed),
            "nets_renamed_candidates": len(renamed_candidates),
            "nets_changed": len(nets_changed),
        },
        "components_added": comps_added,
        "components_removed": comps_removed,
        "components_changed": comps_changed,
        "nets_added": nets_added,
        "nets_removed": nets_removed,
        "nets_renamed_candidates": renamed_candidates,
        "nets_changed": nets_changed,
    }
