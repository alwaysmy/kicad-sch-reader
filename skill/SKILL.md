---
name: kicad-sch-reader
description: |
  Use when the user asks to parse, review, trace, or cross-check KiCad schematic
  projects and LCEDA .epro projects (including CBB reuse modules). Provides
  deterministic extraction first, then guides LLM datasheet/manual verification.
---

# kicad-sch-reader 使用规范

工具只做“文件事实提取”和“确定性规则检查”。设计是否合理、器件参数是否满足，
需要 LLM 继续阅读数据手册后判断；所有结论必须带证据来源。

## 1. 基础命令

```bat
cd D:\MyProjects\AI\schematics_review_tool
set PYTHONIOENCODING=utf-8

python kicad-sch-reader.py parse <kicad工程目录>
python kicad-sch-reader.py review <kicad工程目录> --out-md reports\xxx.review.md --out-json reports\xxx.review.json
python kicad-sch-reader.py trace <工程> <位号> --no-power --depth 3
python kicad-sch-reader.py link-check <工程A> <工程B>
python scripts\lceda_epro_review.py <xxx.epro> --trace-net VCC_1V5 --trace-ref U6 --trace-skip-power
```

## 2. trace 的 power 判断（不要只靠名字正则）

“电源网络”命名不一定规范，按以下证据层级判断：

1. 结构证据（最强）：网络内有 `power:GND`/`power:+5V` 等电源符号，
   或引脚类型为 `power_in` / `power_out`。
2. 命名正则（中）：`GND|AGND|DGND|VCC|VDD|VSS|VBUS|VREF|±?数字V...`。
3. 用户补充（弱）：`--power-net <regex>` 传入非规范命名。
4. 无法判定时：不要跳过，列出候选并标注“疑似电源网络”。

KiCad CLI 已按此实现；LCEDA 脚本使用 `POWER_RE + --power-net + SHORT/别名`。

## 3. 器件参数必须查手册，禁止猜

示例：报告发现 `CBB1 EN=VCC_1V8`，不能直接说“TPS563201 EN 阈值是否满足”。
必须：

1. 从报告拿到器件位号、MPN、连接网络：
   `CBB1 -> U6 TPS563201DDCR -> EN pin -> VCC_1V8`。
2. 先查本地手册：
   - Everything 搜索 `TPS563201*`、`slvs*`、`*datasheet*.pdf`、`TPS563201DDCR`；
   - 找到 PDF 后用 Okular 打开，或文本提取工具搜 `EN threshold` / `Enable`；
   - 记录文件路径与页码/段落。
3. 本地没有再上网：
   - TI 官网搜索 MPN，找 `TPS563201 3-A Synchronous Buck Converter datasheet (SLVSDG5)`；
   - 或用 Kimi WebBridge / Edge 打开搜索结果页，`evaluate` 提取正文。
4. 拿手册参数与原理图事实比较：
   - EN 高电平阈值典型值/最大值 vs 实际 `VCC_1V8`；
   - EN 绝对最大额定值 vs 实际电压；
   - 输入电压范围 vs `VCC_5V`；
   - 输出电流能力 vs 后端负载（需要 BOM/负载表或后续功耗分析）。
5. 输出 Finding 时写证据：
   `source=datasheet, sheet=..., ref=U6, pin=EN, evidence=..., confidence=...`。
   区分 `direct`（文件事实）、`calculated`（计算）、`datasheet`（手册）、`ai`（推断）。

## 4. 跨板检查的证据等级

- `link-check` 逐 pin 同名匹配只是 `candidate`，不是物理连接。
- 只有用户声明或项目 metadata 声明连接器对插，才是 `declared`。
- 输出建议保留 `confidence: candidate|detected|inferred|declared`。
- MainBoard J102 ↔ PowerBoard J103 实测 16/16，可写 `detected(score=1.0)`，
  但仍需说明“实际对插关系需用户确认”。

## 5. CBB 展开后的汇报要求

- CBB 内部器件必须用 `.eins` 覆盖后的母板位号（U6/L5/C37...）。
- 提到器件时写 `板 / 页 / CBB实例 / 位号`。
- CBB 端口 trace 要用母图网络 canonical，避免 SHORT 短路桥造成
  `VCC_1V5` / `VCC_1V35_DDR` 名实分离。

## 6. 多工程跨板检查

```bat
python scripts\multi_project_cross_check.py --kicad <工程A> --kicad <工程B> --lceda <xxx.epro>
```

输出候选连接器对、score、evidence，不自动确认。脚本内部先把 KiCad/LCEDA
统一为 `kicad_sch_reader.circuit_ir.BoardIR`，分析/汇报时优先引用 IR 中的
canonical net 与 `net.kind`，不要直接读两种格式的原始字典。
