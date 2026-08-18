#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LCEDA Professional `.epro`（ZIP 导出）工程审查器。

该脚本以 lceda-sch-reader 的解析/连通域函数为基础，补齐 `.epro` 导出格式
与 CBB（复用模块）展开逻辑，并对 LIA_DigitalBoard_RevA 做板级设计审查。

只读：仅读取 .epro 压缩包，不修改任何工程文件。
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
import sys
import zipfile
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE / "repos" / "lceda-sch-reader"))

import lceda_reader  # noqa: E402


# ---------------------------------------------------------------- .epro backend

class EproDB:
    """Minimal LCEDA `.epro` backend implementing the methods used by
    lceda_reader's parser/connectivity functions."""

    def __init__(self, epro_path):
        self.path = Path(epro_path)
        self.zip = zipfile.ZipFile(self.path)
        self.obj = json.loads(self.zip.read("project.json"))
        self.devices: Dict[str, dict] = self.obj.get("devices", {})
        self.symbols: Dict[str, dict] = self.obj.get("symbols", {})
        self.boards: Dict[str, dict] = self.obj.get("boards", {})
        self.schematics: Dict[str, dict] = self.obj.get("schematics", {})
        self._names = set(self.zip.namelist())
        self._page_index: Dict[str, Tuple[str, int]] = {}  # unique_title -> (schematic uuid, page id)
        self._override_cache: Dict[str, list] = {}
        self._symbol_pin_cache: Dict[str, dict] = {}
        self._records_cache: Dict[str, list] = {}
        self._build_page_index()
        self._load_overrides()

    # -- project index -----------------------------------------------------
    def _build_page_index(self):
        for board_name, board in self.boards.items():
            sch_uuid = board.get("schematic")
            if not sch_uuid:
                continue
            sch = self.schematics.get(sch_uuid, {})
            for page in sch.get("sheets", []):
                page_name = page.get("display_title") or page.get("name") or str(page.get("id"))
                self._page_index[f"{board_name}::{page_name}"] = (sch_uuid, int(page["id"]))
        # CBB modules also appear as schematics without board entry; register
        # them under their own name so they can be loaded independently.
        for sch_uuid, sch in self.schematics.items():
            sch_name = sch.get("name", sch_uuid)
            for page in sch.get("sheets", []):
                page_name = page.get("display_title") or page.get("name") or str(page.get("id"))
                self._page_index[f"CBBMOD::{sch_name}::{page_name}"] = (sch_uuid, int(page["id"]))

    def _load_overrides(self):
        self.eins_entries = []
        for name in self._names:
            if not name.startswith("INSTANCE/") or not name.endswith(".eins"):
                continue
            try:
                data = self.zip.read(name).decode("utf-8", errors="replace")
                forms = [json.loads(line) for line in data.splitlines() if line.strip()]
                override = next((f for f in forms if f and f[0] == "OVERRIDE"), None)
                if override and len(override) >= 3 and isinstance(override[1], list) and len(override[1]) >= 2:
                    target = override[1]
                    self.eins_entries.append((
                        target[0],
                        target[1],
                        target[2] if len(target) > 2 else "$1",
                        override[2],
                    ))
            except Exception:
                continue

    # -- lceda_reader-compatible API ----------------------------------------
    def schematics(self):
        return [(name, name, name) for name in self.boards]

    def schem_map(self):
        return {name: (name, name) for name in self.boards}

    def sheets(self, doc_type=1):
        rows = []
        for board_name, board in self.boards.items():
            sch_uuid = board.get("schematic")
            sch = self.schematics.get(sch_uuid, {})
            for page in sch.get("sheets", []):
                title = f"{board_name}::{page.get('display_title') or page.get('name') or page['id']}"
                rows.append((page.get("uuid"), title, board_name, 1))
        return rows

    def decompress(self, ds):
        return ds

    def sheet_records(self, title, doc_type=1):
        if title in self._records_cache:
            return self._records_cache[title]
        key = self._page_index.get(title)
        if key is None:
            return None
        sch_uuid, page_id = key
        fname = f"SHEET/{sch_uuid}/{page_id}.esch"
        if fname not in self._names:
            return None
        text = self.zip.read(fname).decode("utf-8", errors="replace")
        records = []
        for line in text.splitlines():
            try:
                records.append(json.loads(line))
            except Exception:
                continue
        # Apply instance overrides for CBB child pages when this page was
        # registered through register_cbb_page().
        overrides = self._override_cache.get(title)
        if overrides:
            records = self._apply_overrides(records, overrides)
        self._records_cache[title] = records
        return records

    def register_cbb_page(self, title: str, sch_uuid: str, page_id: int, overrides: Optional[dict] = None):
        self._page_index[title] = (sch_uuid, int(page_id))
        if overrides:
            self._override_cache[title] = overrides

    def _apply_overrides(self, records, overrides):
        """Override ATTR values for CBB child component ids."""
        out = []
        used = set()
        for rec in records:
            if rec and rec[0] == "ATTR" and len(rec) >= 5:
                comp_id = rec[2]
                attr_name = rec[3]
                if comp_id in overrides and attr_name in overrides[comp_id]:
                    rec = list(rec)
                    rec[4] = overrides[comp_id][attr_name]
                    used.add((comp_id, attr_name))
            out.append(rec)
        # Add overrides that have no existing ATTR record.
        for comp_id, attrs in overrides.items():
            for attr_name, value in attrs.items():
                if (comp_id, attr_name) in used:
                    continue
                out.append(["ATTR", f"ovr_{comp_id}_{attr_name}", comp_id, attr_name, value, 0, 0, None, None, 0, "st1", 0])
        return out

    def symbol_of_device(self, device_uuid):
        if not device_uuid:
            return None
        dev = self.devices.get(device_uuid)
        if isinstance(dev, dict) and isinstance(dev.get("attributes"), dict):
            return dev["attributes"].get("Symbol")
        return None

    def device_map(self):
        out = {}
        for uuid, dev in self.devices.items():
            if not isinstance(dev, dict):
                continue
            attrs = dev.get("attributes") or {}
            title = dev.get("title") or ""
            desc = attrs.get("Description") or dev.get("description") or ""
            out[uuid] = (title, attrs.get("Supplier Part") or "", desc)
        return out

    def device_attrs(self, device_uuid):
        dev = self.devices.get(device_uuid)
        if isinstance(dev, dict):
            return dict(dev.get("attributes") or {})
        return {}

    def symbol_pins(self, symbol_uuid):
        """Parse a SYMBOL/<uuid>.esym body into lceda_reader's dict shape."""
        if not symbol_uuid:
            return None
        if symbol_uuid in self._symbol_pin_cache:
            return self._symbol_pin_cache[symbol_uuid]
        fname = f"SYMBOL/{symbol_uuid}.esym"
        if fname not in self._names:
            return None
        text = self.zip.read(fname).decode("utf-8", errors="replace")
        pins, names, numbers, pin_types = {}, {}, {}, {}
        bbox = None
        cur_part = None
        symbol_type = None
        origin_x = origin_y = 0.0
        for line in text.splitlines():
            try:
                a = json.loads(line)
            except Exception:
                continue
            if not isinstance(a, list) or len(a) < 2:
                continue
            if a[0] == "HEAD" and len(a) > 1 and isinstance(a[1], dict):
                symbol_type = a[1].get("symbolType")
                origin_x = float(a[1].get("originX", 0) or 0)
                origin_y = float(a[1].get("originY", 0) or 0)
            elif a[0] == "PART" and len(a) > 2 and isinstance(a[2], dict):
                cur_part = a[1]
                b = a[2].get("BBOX")
                if b and len(b) == 4:
                    bbox = [min(b[0], b[2]), min(b[1], b[3]), max(b[0], b[2]), max(b[1], b[3])]
            elif a[0] == "PIN" and len(a) >= 8:
                # .esym HEAD.originX/Y is the symbol-local origin; instance
                # coordinates are origin-relative, so subtract it.
                pins[a[1]] = {"id": a[1], "x": (a[4] or 0) - origin_x,
                              "y": (a[5] or 0) - origin_y,
                              "rot": a[7] if a[7] is not None else 0,
                              "part": cur_part, "name": None, "number": None, "pin_type": None}
            elif a[0] == "ATTR" and len(a) >= 5 and a[2] in pins:
                if a[3] == "NAME":
                    names[a[2]] = a[4]
                elif a[3] == "NUMBER":
                    numbers[a[2]] = str(a[4])
                elif a[3] == "Pin Type":
                    pin_types[a[2]] = a[4]
        for pid, p in pins.items():
            p["name"] = names.get(pid)
            p["number"] = numbers.get(pid)
            p["pin_type"] = pin_types.get(pid)
        result = {"pins": list(pins.values()), "bbox": bbox,
                  "parts": sorted({p["part"] for p in pins.values()}),
                  "symbol_type": symbol_type}
        self._symbol_pin_cache[symbol_uuid] = result
        return result


# ---------------------------------------------------------------- CBB flattening

def board_name_for_symbol(db: EproDB, symbol_uuid: str) -> Optional[str]:
    sym = db.symbols.get(symbol_uuid)
    if not isinstance(sym, dict):
        return None
    title = sym.get("title")
    if title in db.boards:
        return title
    for board_name, board in db.boards.items():
        sch = db.schematics.get(board.get("schematic"), {})
        if sch.get("name") == title:
            return board_name
    return None


def overrides_for_instance(db: EproDB, main_sch_uuid: str, parent_cid: str) -> dict:
    for target_sch, target_inst, target_unit, payload in db.eins_entries:
        if target_sch != main_sch_uuid:
            continue
        inst = target_inst[1:] if target_inst.startswith("$") else target_inst
        if inst.endswith(parent_cid):
            return db._load_override_payload(target_sch, target_inst, target_unit) or payload
    return {}


def _load_override_payload(self, sch, inst, unit):
    # implemented as method below; placeholder replaced in class monkey-patch
    return {}


def _monkeypatch_epro_overrides():
    def load_payload(self, sch_uuid, inst, unit):
        for name in self._names:
            if not name.startswith("INSTANCE/") or not name.endswith(".eins"):
                continue
            try:
                decoded = base64.urlsafe_b64decode(name.split("/")[-1][:-5]).decode("utf-8", errors="replace")
            except Exception:
                continue
            if decoded.startswith(f"{sch_uuid}_{inst}_{unit}"):
                data = self.zip.read(name).decode("utf-8", errors="replace")
                for line in data.splitlines():
                    try:
                        f = json.loads(line)
                    except Exception:
                        continue
                    if f and f[0] == "OVERRIDE" and len(f) >= 3:
                        return f[2]
        return {}

    EproDB._load_override_payload = load_payload


_monkeypatch_epro_overrides()


def _cbb_module_pages(db: EproDB, board_name: str):
    sch_uuid = db.boards.get(board_name, {}).get("schematic")
    sch = db.schematics.get(sch_uuid, {})
    return sch_uuid, sch.get("sheets", [])


def _iter_main_pages(db: EproDB, board_name: str):
    return [
        (title, sch_uuid, page_id)
        for title, (sch_uuid, page_id) in db._page_index.items()
        if title.startswith(f"{board_name}::")
    ]


def _collect_pinmap(db: EproDB, title: str):
    sheet = lceda_reader.parse_sheet(db, title)
    if sheet is None:
        return None, None, None, None
    comp_pins, wires, pt_wires, endp = lceda_reader._collect_pinmap_data(db, sheet, title)
    pinmap = lceda_reader.resolve_nets_by_domain(db, sheet, comp_pins, wires, pt_wires, endp)
    return sheet, comp_pins, pinmap, endp


def _pin_direct_nets(comp_pins, endp):
    """返回 {(designator, pin_key): 该引脚物理端点上的网络名}。

    pin_key 对重名引脚为 name#number。该映射用于让 pin_net_map 保留“本引脚
    自己命中的网络名”，而不是被全局 alias 组覆盖成另一侧名字。
    """
    out = {}
    for key, plist in (comp_pins or {}).items():
        des = key if isinstance(key, str) else key[0]
        for p in plist:
            ax, ay = p.get("x"), p.get("y")
            if ax is None or ay is None:
                continue
            net = (endp or {}).get((ax, ay))
            if net is None:
                for ox in (-1, 0, 1):
                    for oy in (-1, 0, 1):
                        net = (endp or {}).get((ax + ox, ay + oy))
                        if net:
                            break
                    if net:
                        break
            out[(des, p.get("key") or p["pin"])] = net or ""
    return out


def _fmt_component(db, c):
    dev_uuid = c.get("device_uuid") or ""
    dev = db.devices.get(dev_uuid, {}) if dev_uuid else {}
    attrs = dev.get("attributes", {}) if isinstance(dev, dict) else {}
    return {
        "designator": c.get("designator"),
        "cid": c.get("cid"),
        "title": c.get("title"),
        "symbol_uuid": c.get("symbol_uuid"),
        "device_uuid": dev_uuid,
        "device_title": dev.get("title", "") if isinstance(dev, dict) else "",
        "value": attrs.get("Value") or attrs.get("LCSC Part Name") or c.get("attrs", {}).get("Name"),
        "footprint": attrs.get("Footprint") or c.get("attrs", {}).get("Footprint"),
        "reuse": c.get("attrs", {}).get("Reuse Block") if isinstance(c.get("attrs"), dict) else None,
        "uid": c.get("attrs", {}).get("Unique ID") if isinstance(c.get("attrs"), dict) else None,
    }


# ---------------------------------------------------------------- review rules

POWER_RE = lceda_reader.POWER_NET_RE


def review_epro(epro_path, board_name=None, out_md=None, out_json=None,
                trace_nets=None, trace_refs=None, trace_skip_power=False,
                power_net_patterns=None):
    db = EproDB(epro_path)
    if not db.boards:
        if db.schematics:
            raise SystemExit(
                f".epro 中 project.json 没有 boards 表，且 schematics={list(db.schematics)[:3]}；"
                f"当前版本无法选择审查板")
        raise SystemExit(
            f".epro 中 project.json 没有 boards/schematics 数据（可能是仅有 PCB 的导出包）：{epro_path}")
    if board_name is None:
        candidates = [n for n in db.boards if "LIA" in n or "锁定" in n]
        board_name = candidates[0] if candidates else list(db.boards)[0]
    main_board = db.boards.get(board_name)
    if not main_board:
        raise SystemExit(f"board not found: {board_name}")
    main_sch_uuid = main_board["schematic"]
    main_sch = db.schematics.get(main_sch_uuid, {})

    findings = []
    modules = []
    flat_components = []
    net_members = defaultdict(list)
    pin_net_map = {}
    pin_local_net = {}
    child_page_registry = []
    bridge_rows = []

    cbb_symbol_titles = {
        u: s.get("title")
        for u, s in db.symbols.items()
        if isinstance(s, dict) and str(s.get("type", "")) == "17"
    }

    # 1) Main pages
    for title, sch_uuid, page_id in _iter_main_pages(db, board_name):
        sheet, comp_pins, pinmap, endp = _collect_pinmap(db, title)
        if sheet is None:
            findings.append(("error", "PAGE_LOAD_FAILED", title, "", f"无法解析页面 {title}"))
            continue
        for c in sheet["components"]:
            des = c.get("designator")
            # CBB module symbols are hierarchy markers, not physical parts.
            if des and not str(des).startswith("#") and c.get("symbol_uuid") not in cbb_symbol_titles:
                item = _fmt_component(db, c)
                item["sheet"] = title
                flat_components.append(item)
        for (des, pin), net in (pinmap or {}).items():
            pin_net_map[(title, str(des), str(pin))] = net
            net_members[net or ""].append({"sheet": title, "ref": str(des), "pin": str(pin)})
        for (des, pin), net in _pin_direct_nets(comp_pins, endp).items():
            pin_local_net[(title, str(des), str(pin))] = net
        bridge_rows.extend(
            lceda_reader.collect_two_pin_bridges(db, sheet, comp_pins, pinmap or {}, endp or {}))

        # Discover CBB instances on this page.
        for c in sheet["components"]:
            sym = c.get("symbol_uuid")
            if sym in cbb_symbol_titles:
                module_name = cbb_symbol_titles[sym]
                board_of_module = board_name_for_symbol(db, sym) or module_name
                sch_uuid2, pages = _cbb_module_pages(db, board_of_module) if board_of_module in db.boards else (None, [])
                if sch_uuid2 is None:
                    findings.append(("error", "CBB_SCHEMA_MISSING", title, str(c.get("designator")),
                                     f"CBB 模块 {module_name} 找不到 schematic"))
                    continue
                overrides = overrides_for_instance(db, main_sch_uuid, c["cid"])
                sp = db.symbol_pins(sym)
                modules.append({
                    "sheet": title, "designator": c.get("designator"), "cid": c["cid"],
                    "module": module_name, "symbol_uuid": sym,
                    "pos": (c.get("x"), c.get("y")),
                    "pins": [p["name"] for p in (sp or {}).get("pins", [])],
                    "port_nets": {
                        p["name"]: pin_net_map.get((title, str(c.get("designator")), str(p["name"])))
                        for p in (sp or {}).get("pins", []) if p.get("name")
                    },
                })
                for page in pages:
                    child_title = f"{title}/CBB:{c.get('designator')}:{page.get('display_title') or page.get('name') or page['id']}"
                    db.register_cbb_page(child_title, sch_uuid2, int(page["id"]), overrides)
                    child_sheet, child_comp_pins, child_pinmap, child_endp = _collect_pinmap(db, child_title)
                    if child_sheet is None:
                        findings.append(("error", "CBB_PAGE_LOAD_FAILED", title, str(c.get("designator")),
                                         f"CBB 子页 {page.get('display_title')} 无法解析"))
                        continue
                    child_page_registry.append({
                        "instance": str(c.get("designator")),
                        "module": module_name,
                        "parent_sheet": title,
                        "child_title": child_title,
                        "page_id": int(page["id"]),
                        "page_name": page.get("display_title") or page.get("name") or str(page.get("id")),
                        "child_sheet": child_sheet,
                        "child_pinmap": child_pinmap or {},
                        "child_endp": child_endp or {},
                    })
                    # Child port components carry Name=VIN/VOUT/... and are
                    # matched to the CBB symbol pin names.
                    port_names = {
                        cc.get("attrs", {}).get("Name"): cc
                        for cc in child_sheet["components"]
                        if cc.get("attrs", {}).get("Name") and not cc.get("designator")
                    }
                    port_net_map = {}
                    for pin_name, port_comp in port_names.items():
                        px, py = port_comp.get("x"), port_comp.get("y")
                        physical_net = None
                        if px is not None and py is not None:
                            physical_net = child_endp.get((px, py))
                            if physical_net is None:
                                # exact-coordinate fallback with small tolerance
                                for (ex, ey), net in child_endp.items():
                                    if abs(ex - px) <= 1e-6 and abs(ey - py) <= 1e-6:
                                        physical_net = net
                                        break
                        port_net_map[pin_name] = physical_net or port_comp.get("net") or pin_name
                    # child_net -> parent net, through the CBB symbol pins.
                    net_bridge = {}
                    for pin_name, child_net in port_net_map.items():
                        parent_net = pin_net_map.get((title, str(c.get("designator")), str(pin_name)))
                        net_bridge[child_net] = parent_net or child_net
                    # Remap child nets into board scope and merge CBB ports.
                    for (des, pin), child_net in (child_pinmap or {}).items():
                        if child_net in net_bridge:
                            flat_net = net_bridge[child_net]
                        elif child_net and POWER_RE.match(str(child_net)):
                            flat_net = child_net
                        elif child_net:
                            flat_net = f"{c.get('designator')}/{child_net}"
                        else:
                            flat_net = ""
                        pin_net_map[(child_title, str(des), str(pin))] = flat_net
                        net_members[flat_net].append({"sheet": child_title, "ref": str(des), "pin": str(pin)})
                    for (des, pin), net in _pin_direct_nets(child_comp_pins, child_endp).items():
                        pin_local_net[(child_title, str(des), str(pin))] = net
                    bridge_rows.extend(
                        lceda_reader.collect_two_pin_bridges(
                            db, child_sheet, child_comp_pins, child_pinmap or {},
                            child_endp or {}))
                    for cc in child_sheet["components"]:
                        if cc.get("designator") and not str(cc.get("designator")).startswith("#"):
                            item = _fmt_component(db, cc)
                            item["sheet"] = child_title
                            item["module_instance"] = str(c.get("designator"))
                            flat_components.append(item)
                    # Verify every module pin found a parent net. 直接网络为
                    # 空时先查两脚中间器件桥：若该引脚与一个 passive 器件
                    # 相连且另一侧有名，则不是“未连接”，而是“经器件连接”。
                    sp = db.symbol_pins(sym)
                    for p in (sp or {}).get("pins", []):
                        pname = p.get("name")
                        if not pname:
                            continue
                        parent_net = pin_net_map.get((title, str(c.get("designator")), str(pname)))
                        if not parent_net:
                            rx, ry = p.get("x"), p.get("y")
                            if c.get("mirror"):
                                rx = -rx
                            rot = (c.get("rot") or 0) % 360
                            for _ in range(int(rot // 90)):
                                rx, ry = -ry, rx
                            ax, ay = (c.get("x") or 0) + rx, (c.get("y") or 0) + ry
                            through = None
                            for b in bridge_rows:
                                pos_a = b.get("pos_a") or [None, None]
                                pos_b = b.get("pos_b") or [None, None]
                                if pos_a[0] is not None and abs(pos_a[0] - ax) <= 1 and abs(pos_a[1] - ay) <= 1 and b.get("net_b"):
                                    through = (b, "b")
                                    break
                                if pos_b[0] is not None and abs(pos_b[0] - ax) <= 1 and abs(pos_b[1] - ay) <= 1 and b.get("net_a"):
                                    through = (b, "a")
                                    break
                            if through:
                                b, side = through
                                other = b.get("net_b") if side == "b" else b.get("net_a")
                                findings.append(("info", "CBB_PIN_THROUGH_PASSIVE", title,
                                                 f"{c.get('designator')}.{pname}",
                                                 f"CBB 引脚 {pname} 直接网络为空，经中间器件 "
                                                 f"{b.get('designator')}({b.get('kind')}) 连接到 {other}"))
                            else:
                                findings.append(("info", "CBB_PIN_INDIRECT_NET", title,
                                                 f"{c.get('designator')}.{pname}",
                                                 f"CBB 模块 {module_name} 引脚 {pname} 直接网络为空；"
                                                 f"可能经导线/无源器件间接连接，请结合 component_bridges 判断"))
                        ptype = (p.get("pin_type") or "").upper()
                        pname_u = str(pname).upper()
                        if ("VOUT" in pname_u or pname_u in ("D+", "D-")) and ptype == "IN":
                            findings.append(("warning", "CBB_PIN_TYPE_SUSPECT", title,
                                             f"{c.get('designator')}.{pname}",
                                             f"CBB 模块 {module_name} 引脚 {pname} 标记为 IN，但按名称应为输出/双向"))
                        if pname_u in ("GND", "VIN", "VBUS") and ptype in ("OUT", "BI"):
                            findings.append(("info", "CBB_PIN_TYPE_SUSPECT", title,
                                             f"{c.get('designator')}.{pname}",
                                             f"CBB 模块 {module_name} 引脚 {pname} 类型为 {ptype}，建议确认"))

    # 1.5) Merge net aliases (SHORT 短接符产生的 "A,B" 域名) across the whole
    # board, then rebuild net membership.
    alias_parent: Dict[str, str] = {}

    def afind(name: str) -> str:
        alias_parent.setdefault(name, name)
        while alias_parent[name] != name:
            alias_parent[name] = alias_parent[alias_parent[name]]
            name = alias_parent[name]
        return name

    def aunion(a: str, b: str) -> None:
        ra, rb = afind(a), afind(b)
        if ra != rb:
            alias_parent[rb] = ra

    def group_of(name: str) -> str:
        """把 'A,B' 别名串归到 alias 组的 root；单名返回自身 root。"""
        if not name:
            return ""
        names = [n for n in str(name).split(",") if n]
        return afind(names[0]) if names else ""

    for key, netstr in list(pin_net_map.items()):
        if not netstr:
            continue
        names = [n for n in str(netstr).split(",") if n]
        if len(names) > 1:
            for n in names[1:]:
                aunion(names[0], n)
    net_members = defaultdict(list)
    net_aliases = defaultdict(set)
    canonical_pin_net_map = {}
    for key, netstr in list(pin_net_map.items()):
        if not netstr:
            canonical_pin_net_map[key] = ""
            continue
        names = [n for n in str(netstr).split(",") if n]
        # pin_net_map 保留“该引脚自己物理端点命中的网络名”，不要被全局
        # alias root 改写。这样 U3.PA9=MCU_UART_TX、SHORTe4381.Pin1#1=
        # MCU_SPI_CS、Pin1#2=IO_L9P...；跨名查找/成员分组使用 alias 组。
        local_name = pin_local_net.get(key)
        if local_name not in names:
            local_name = names[0]
        group = afind(local_name)
        canonical_pin_net_map[key] = local_name
        net_aliases[group].update(names)
        net_members[group].append({"sheet": key[0], "ref": str(key[1]), "pin": str(key[2])})

    comp_lookup = defaultdict(list)
    for comp in flat_components:
        if comp.get("designator"):
            comp_lookup[comp["designator"]].append(comp)

    def member_detail(member):
        ref = member.get("ref", "")
        comps = comp_lookup.get(ref, [])
        comp = next((c for c in comps if c.get("sheet") == member.get("sheet")),
                    comps[0] if comps else {})
        return {
            **member,
            "device": comp.get("device_title") or comp.get("value") or comp.get("title") or "",
            "footprint": comp.get("footprint") or "",
            "module_instance": comp.get("module_instance") or "",
        }

    def trace_net(net):
        target = group_of(net)
        return [member_detail(m) for m in net_members.get(target, [])]

    extra_power_patterns = [re.compile(p) for p in (power_net_patterns or [])]

    def is_power_net_name(name):
        if not name:
            return False
        name = str(name)
        # 层级 1：LCEDA 自己的电源/地正则。
        if POWER_RE.match(name):
            return True
        # 层级 2：用户补充命名模式（非规范命名时使用）。
        for pat in extra_power_patterns:
            if pat.search(name):
                return True
        # 层级 3：SHORT 别名或明显的电源/地标识。
        if name.startswith("SHORT") or name.split(",")[0].strip().upper() in (
            "GND", "AGND", "DGND", "DXN_0", "VCC", "VDD", "VSS", "VBUS", "PWR", "VREF"
        ):
            return True
        return False

    def trace_ref(ref):
        edges = []
        seen = set()
        for key, netstr in list(pin_net_map.items()):
            sheet, ref_key, pin_key = key
            if str(ref_key).lower() != str(ref).lower() or not netstr:
                continue
            canonical = canonical_pin_net_map.get(key, "")
            group = group_of(canonical)
            if trace_skip_power and is_power_net_name(canonical):
                continue
            for member in net_members.get(group, []):
                edge_key = (sheet, str(ref_key), str(pin_key), member["sheet"], member["ref"], member["pin"], canonical)
                if edge_key in seen:
                    continue
                seen.add(edge_key)
                edges.append({
                    "from_sheet": sheet,
                    "from_ref": str(ref_key),
                    "from_pin": str(pin_key),
                    "net": canonical,
                    "to_sheet": member["sheet"],
                    "to_ref": member["ref"],
                    "to_pin": member["pin"],
                    "to_device": member_detail(member)["device"],
                    "to_module_instance": member.get("module_instance", ""),
                })
        return edges

    # CBB 内部展开明细：器件、封装、每个引脚的展平网络。
    module_by_ref = {m["designator"]: m for m in modules}
    cbb_detail = []
    for reg in child_page_registry:
        child_title = reg["child_title"]
        instance = reg["instance"]
        module_meta = module_by_ref.get(instance, {})
        comps = []
        for comp in flat_components:
            if comp.get("sheet") != child_title:
                continue
            pins = []
            for key, net in canonical_pin_net_map.items():
                if key[0] == child_title and str(key[1]) == str(comp.get("designator")):
                    pins.append({"pin": str(key[2]), "net": net})
            comps.append({**comp, "pins": sorted(pins, key=lambda p: (len(p["pin"]), p["pin"]))})
        child_sheet = reg["child_sheet"]
        ports = []
        port_names = {
            cc.get("attrs", {}).get("Name"): cc
            for cc in child_sheet["components"]
            if cc.get("attrs", {}).get("Name") and not cc.get("designator")
        }
        for port_name, port_comp in sorted(port_names.items()):
            child_net = port_comp.get("net") or port_name
            parent_net = module_meta.get("port_nets", {}).get(port_name)
            # 内部器件跟踪必须以“母图网络”为目标：短路桥会把
            # VCC_1V5/VCC_1V35_DDR、D+/USB_D_P 等合并成同一展平网络。
            target = group_of(str(parent_net or child_net))
            members = [
                member_detail(m) for m in net_members.get(target, [])
                if m["sheet"] == child_title and m["ref"]
            ]
            ports.append({
                "name": port_name,
                "child_net": child_net,
                "parent_net": parent_net,
                "flat_net": target,
                "internal_members": members,
            })
        cbb_detail.append({
            "instance": instance,
            "module": reg["module"],
            "parent_sheet": reg["parent_sheet"],
            "page_name": reg["page_name"],
            "components": comps,
            "ports": ports,
        })

    trace_results = {}
    for net in (trace_nets or []):
        trace_results.setdefault("nets", {})[net] = trace_net(net)
    for ref in (trace_refs or []):
        trace_results.setdefault("refs", {})[ref] = trace_ref(ref)

    # 2) Checks over flattened components.
    by_ref = defaultdict(list)
    by_ref_page = defaultdict(list)
    for comp in flat_components:
        if comp.get("designator"):
            by_ref[comp["designator"]].append(comp)
            by_ref_page[(comp["designator"], comp.get("sheet", ""))].append(comp)
    for (ref, page), comps in sorted(by_ref_page.items()):
        if len(comps) > 1:
            uids = {c.get("uid") or "" for c in comps}
            titles = {c.get("title") or "" for c in comps}
            # 脚本自动识别多单元器件：相同 Unique ID + 不同 title 后缀
            # （例如 XC7A35T-2CSG325C.B14 / .B34 / .POWER）。
            same_uid = len(uids) == 1 and bool(next(iter(uids)))
            if same_uid and len(titles) > 1:
                findings.append(("info", "MULTI_UNIT_CONFIRMED", page, ref,
                                 f"位号 {ref} 在同一页出现 {len(comps)} 次，已自动识别为多单元器件"
                                 f"（Unique ID={next(iter(uids))}）"))
            elif same_uid and len(titles) == 1:
                findings.append(("warning", "POSSIBLE_REUSED_INSTANCE", page, ref,
                                 f"位号 {ref} 同页出现 {len(comps)} 次且 Unique ID/title 相同，"
                                 f"可能是分层复用或复制残留，需人工确认"))
            else:
                findings.append(("error", "DUPLICATE_DESIGNATOR", page, ref,
                                 f"位号 {ref} 在同一页/同一 CBB 实例内出现 {len(comps)} 次"))
    for ref, comps in sorted(by_ref.items()):
        pages = {c.get("sheet", "") for c in comps}
        if len(comps) > 1 and len(pages) > 1:
            uids = {c.get("uid") or "" for c in comps}
            titles = {c.get("title") or "" for c in comps}
            same_uid = len(uids) == 1 and bool(next(iter(uids)))
            if same_uid and len(titles) > 1:
                findings.append(("info", "MULTI_UNIT_CONFIRMED", comps[0].get("sheet", ""), ref,
                                 f"位号 {ref} 跨 {len(pages)} 页出现，已自动识别为多单元器件"
                                 f"（Unique ID={next(iter(uids))}）"))
            elif same_uid and len(titles) == 1:
                findings.append(("warning", "POSSIBLE_REUSED_INSTANCE", comps[0].get("sheet", ""), ref,
                                 f"位号 {ref} 跨 {len(pages)} 页出现且 Unique ID/title 相同，"
                                 f"可能是分层复用，需人工确认物理位置"))
            else:
                findings.append(("info", "MULTI_UNIT_UNVERIFIED", comps[0].get("sheet", ""), ref,
                                 f"位号 {ref} 跨 {len(pages)} 页出现但无法自动判定多单元，需人工确认"))
        else:
            comp = comps[0]
            if not comp.get("device_uuid") and not comp.get("symbol_uuid", "").startswith("CBB"):
                pass
            if comp.get("device_uuid") and not comp.get("device_title"):
                findings.append(("warning", "DEVICE_MISSING", comp.get("sheet", ""), ref,
                                 f"Device {comp.get('device_uuid')} 在 devices 表中缺失"))
            if comp.get("device_uuid") and not comp.get("footprint") and not comp.get("reuse") is None:
                pass

    # 3) Nets: single pin nets and CBB port summary.
    for net, members in sorted(net_members.items()):
        if net and len(members) == 1:
            m = members[0]
            findings.append(("info", "SINGLE_PIN_NET", m["sheet"], m["ref"],
                             f"网络 {net} 仅 {m['ref']}.{m['pin']} 一个引脚"))

    # 4) BOM summary.
    bom = defaultdict(lambda: {"qty": 0, "refs": []})
    for comp in flat_components:
        if not comp.get("designator"):
            continue
        key = (comp.get("device_title") or comp.get("value") or comp.get("title") or "?",
               comp.get("footprint") or "")
        bom[key]["qty"] += 1
        bom[key]["refs"].append(comp["designator"])

    report = {
        "epro": str(epro_path),
        "board": board_name,
        "main_schematic": main_sch.get("name"),
        "pages": len(main_sch.get("sheets", [])),
        "cbb_modules": modules,
        "cbb_detail": cbb_detail,
        "flat_components": flat_components,
        "pin_net_map": {
            f"{key[0]}||{key[1]}||{key[2]}": canonical_pin_net_map.get(key, "")
            for key in canonical_pin_net_map
        },
        "net_aliases": {
            group: sorted(names) for group, names in sorted(net_aliases.items())
            if len(names) > 1
        },
        "component_bridges": bridge_rows,
        "trace_results": trace_results,
        "flat_component_count": len(flat_components),
        "bom_line_count": len(bom),
        "net_count": len(net_members),
        "findings": [
            {"severity": s, "code": code, "sheet": sheet, "ref": ref, "message": msg}
            for s, code, sheet, ref, msg in findings
        ],
        "bom": [
            {"device": k[0], "footprint": k[1], "qty": v["qty"],
             "refs": ", ".join(sorted(v["refs"], key=lambda x: (len(x), x)))}
            for k, v in sorted(bom.items(), key=lambda kv: kv[0][0])
        ],
    }

    if out_md:
        out_md = Path(out_md)
        out_json = Path(out_json or out_md.with_suffix(".json"))
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_board = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "_", board_name)
        out_dir = BASE / "reports"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_md = out_dir / f"{safe_board}.lceda-review-{stamp}.md"
        out_json = out_md.with_suffix(".json")
        print(f"[lceda_epro_review] 未指定 --out-md/--out-json，默认输出到 reports/（带时间戳）：{out_md}")
    _write_markdown(report, findings, out_md)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LCEDA review written:\n  md={out_md}\n  json={out_json}")
    print(f"board={board_name} components={len(flat_components)} nets={len(net_members)} findings={len(findings)}")
    return report


def _write_markdown(report, findings, path):
    lines = []
    lines.append(f"# LCEDA `.epro` 审查报告 — {report['board']}")
    lines.append("")
    lines.append(f"> 数据来源：`{report['epro']}`")
    lines.append(f"> 主原理图：{report['main_schematic']}（{report['pages']} 页）")
    lines.append("")
    lines.append("## 1. CBB 模块实例")
    lines.append("")
    lines.append("| 母图页 | 位号 | CBB 模块 | 引脚→母图网络 | 母图位置 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for m in report["cbb_modules"]:
        ports = ", ".join(f"{p}={m['port_nets'].get(p) or '?'}" for p in m["pins"])
        lines.append(f"| {m['sheet']} | {m['designator']} | {m['module']} | {ports} | {m['pos']} |")
    lines.append("")
    lines.append("## 2. CBB 内部展开明细")
    lines.append("")
    for detail in report.get("cbb_detail", []):
        lines.append(f"### {detail['instance']} — {detail['module']}（{detail['page_name']}）")
        lines.append("")
        lines.append("**端口 → 内部网络/器件：**")
        lines.append("")
        lines.append("| 端口 | 子图网络 | 母图网络 | 展平网络 | 内部连接 |")
        lines.append("| --- | --- | --- | --- | --- |")
        for port in detail["ports"]:
            members = ", ".join(
                f"{m['ref']}.{m['pin']}({m['device']})" for m in port["internal_members"][:12]
            )
            lines.append(
                f"| {port['name']} | {port['child_net']} | {port['parent_net'] or '?'} | "
                f"{port['flat_net']} | {members or '—'} |"
            )
        lines.append("")
        lines.append("**内部器件引脚连接：**")
        lines.append("")
        lines.append("| 位号 | 器件/值 | 封装 | 引脚→展平网络 |")
        lines.append("| --- | --- | --- | --- |")
        for comp in detail["components"]:
            pins = ", ".join(f"{p['pin']}={p['net'] or 'NC'}" for p in comp["pins"])
            lines.append(
                f"| {comp['designator']} | {comp.get('device_title') or comp.get('value') or comp.get('title') or '?'} | "
                f"{comp.get('footprint') or '—'} | {pins or '—'} |"
            )
        lines.append("")
    lines.append("## 3. 设计审查发现")
    lines.append("")
    if not findings:
        lines.append("未发现问题。")
    for sev, label in (("error", "错误"), ("warning", "警告"), ("info", "提示")):
        group = [f for f in findings if f[0] == sev]
        if not group:
            continue
        lines.append(f"### {label}（{len(group)}）")
        lines.append("")
        lines.append("| # | 位置 | 代码 | 说明 |")
        lines.append("| --- | --- | --- | --- |")
        for i, (_, code, sheet, ref, msg) in enumerate(group, 1):
            loc = sheet or ""
            if ref:
                loc += f" / {ref}"
            lines.append(f"| {i} | `{loc}` | {code} | {msg} |")
        lines.append("")
    for net, members in (report.get("trace_results", {}).get("nets") or {}).items():
        lines.append(f"### trace net: {net}（{len(members)} 个引脚）")
        lines.append("")
        lines.append("| 图纸/CBB页 | 位号.引脚 | 器件 |")
        lines.append("| --- | --- | --- |")
        for m in members:
            lines.append(f"| {m['sheet']} | {m['ref']}.{m['pin']} | {m['device']} |")
        lines.append("")
    for ref, edges in (report.get("trace_results", {}).get("refs") or {}).items():
        lines.append(f"### trace ref: {ref}（{len(edges)} 条边）")
        lines.append("")
        lines.append("| from | 网络 | to | to 器件 | CBB 实例 |")
        lines.append("| --- | --- | --- | --- | --- |")
        for e in edges:
            lines.append(
                f"| {e['from_ref']}.{e['from_pin']} | {e['net']} | "
                f"{e['to_ref']}.{e['to_pin']} | {e['to_device']} | {e['to_module_instance']} |"
            )
        lines.append("")
    bridges = report.get("component_bridges", [])
    lines.append("## 3.5 两脚中间器件桥接（保留中间 hop）")
    lines.append("")
    if not bridges:
        lines.append("无。")
    else:
        lines.append("| 位号 | 类型 | direct | 引脚 A | 网络 A | 引脚 B | 网络 B | 器件 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for b in bridges:
            lines.append(
                f"| {b['designator']} | {b['kind']} | {b['direct']} | "
                f"{b['pin_a']}({b['number_a'] or ''}) | {b['net_a'] or '?'} | "
                f"{b['pin_b']}({b['number_b'] or ''}) | {b['net_b'] or '?'} | {b['device']} |"
            )
    lines.append("")
    lines.append("> 说明：LCEDA 展平地网络名 `DXN_0` 与 KiCad `GND` 为同一语义；跨工具比对时归一化。")
    lines.append("")
    lines.append("## 4. 展平 BOM（含 CBB 内部器件）")
    lines.append("")
    lines.append(f"共 {report['bom_line_count']} 行 / {report['flat_component_count']} 个位号。")
    lines.append("")
    lines.append("| 器件/值 | 封装 | 数量 | 位号 |")
    lines.append("| --- | --- | --- | --- |")
    for item in report["bom"][:200]:
        lines.append(f"| {item['device']} | {item['footprint']} | {item['qty']} | {item['refs']} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description="LCEDA .epro CBB-aware design review")
    ap.add_argument("epro", help=".epro 文件")
    ap.add_argument("--board", help="审查的板名（默认自动选择含 LIA/锁定 的板）")
    ap.add_argument("--out-md")
    ap.add_argument("--out-json")
    ap.add_argument("--trace-net", action="append", default=[], help="追踪网络并列出 CBB 内部器件")
    ap.add_argument("--trace-ref", action="append", default=[], help="追踪位号并列出 CBB 内部器件")
    ap.add_argument("--trace-skip-power", action="store_true", help="trace-ref 时跳过电源/地网络")
    ap.add_argument("--power-net", action="append", default=[], help="补充电源网络命名正则（非规范命名时使用）")
    args = ap.parse_args(argv)
    review_epro(args.epro, board_name=args.board, out_md=args.out_md, out_json=args.out_json,
                trace_nets=args.trace_net, trace_refs=args.trace_ref,
                trace_skip_power=args.trace_skip_power, power_net_patterns=args.power_net)


if __name__ == "__main__":
    main()
