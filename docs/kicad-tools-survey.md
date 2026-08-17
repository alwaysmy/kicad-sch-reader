# KiCad 原理图审查工具调研

调研时间：2026-08-17。来源：GitHub Repository Search、PyPI、DuckDuckGo
网页搜索。目标是找出可复用的设计思想，而非简单复制某个工具。

## 1. 结论摘要

| 能力 | 现有工具 | 本工具选择 |
| --- | --- | --- |
| 官方 ERC | KiCad 内置 / `kicad-cli sch erc --format json` | 桥接官方 CLI，JSON 转写 |
| 官方网表 | `kicad-cli sch export netlist` | 桥接官方 CLI + 自研几何网表交叉验证 |
| 文件解析 | `kinparse`（网表）、`kicad-skip`（s-expr）、`pykicad` | 自研标准库 s-expr 解析（零依赖） |
| Git 可视化评审 | Kiri（700★） | 未纳入 v0.1，列为后续方向 |
| AI/MCP 集成 | kicad-mcp-pro、Konnect、eda-agent、akcli | 提供 `--json` 原语，便于 agent 调用 |
| CI 自动检查 | kicad-actions、kicad-action、title-block-check | 后续补 GitHub Actions |
| BOM/供应链 | KiBot、KiCAD-BS-Checker、pcb_checker | BOM 导出已桥接 kicad-cli |

## 2. 重点工具清单

### 官方/准官方

- **KiCad ERC/DRC + `kicad-cli`**：KiCad 10 自带，
  `sch erc --format json --severity-all` 可输出结构化违规；本项目直接复用。
- **KiBot**（PyPI `kibot`，1.9.1）：KiCad 文档/制造文件自动生成，
  擅长把 ERC/DRC 纳入可重复 CI 流程。
- **kicad-actions**（24★）：GitHub Action 自动生成并检查原理图/PCB。
- **sparkengineering/kicad-action**（11★）：PR 级 ERC/DRC 检查。

### 解析与网表

- **kinparse**（27★，PyPI 1.2.4）：解析 Eeschema 网表文件，适合后处理，
  但依赖网表导出步骤，不直接读 `.kicad_sch`。
- **kicad-skip**（PyPI 0.2.5）：操作 KiCad 7+ s-expression 原理图/网表/PCB，
  证明 s-expr 层可以做通用操作。
- **pykicad**（0.1.1）：KiCad 文件格式库，长期维护一般。
- **skidl**（2.3.0）：文本化电路描述与 ERC（电源、NC 检查），其
  “先建模后查规则”的思路与本工具一致。

### 审查/自动化/AI

- **Kiri**（700★）：面向 Git 版本化 KiCad 工程的原理图/布局可视化评审。
  值得借鉴：评审结果必须能回到图纸位置；本工具后续要输出坐标映射。
- **Konnect**（279★）：KiCad 10 原生插件，171 个设计评审/制造工具，
  说明 LLM 原语化是当前趋势。
- **kicad-mcp-pro**（50★）：MCP server，自动化原理图/PCB/ERC/DFM/BOM 评审。
- **eda-agent**（144★）：MCP 驱动 Altium/KiCad/EasyEDA Pro 设计评审。
- **akcli**（5★）：纯标准库 Python CLI，对 `.kicad_sch` 做 op-list 编辑与
  ERC/设计/意图/BOM 检查——与本项目的“零依赖”路线最接近。
- **circuit-unittests**：对原理图/PCB 写单元测试，思路可借鉴为规则引擎。
- **kicad-title-block-check-action**：标题块合规检查，属于规则子集。

### BOM/制造

- **KiCAD-BS-Checker**：DigiKey/Octopart 供应链检查。
- **pcb_checker**：Gerber/钻孔/BOM/CPL 出厂前检查。
- **KiCad `sch export bom`**：本项目直接桥接。

## 3. 对本项目的启发

1. **解析与审查分离**：所有成熟工具都把“读文件”和“查规则”分层；
   本项目因此拆为 `parser / connectivity / rules / report`。
2. **以官方工具为真值源**：自研几何网表必须与 `kicad-cli` 官方网表
   逐引脚交叉验证，而不是自证正确。`tests/validate_examples.py` 即源于此。
3. **零依赖仍是差异化优势**：akcli、lceda-sch-reader 都选择纯标准库；
   本项目延续这一路线，`kicad-cli` 只是可选桥接。
4. **面向 agent 的结构化输出**：`--json` 全部命令可脚本消费，
   为后续 MCP/skill 包装保留接口。
5. **可视化/Git 评审是下一步**：Kiri 表明“报告 → 图形位置”很关键；
   路线图已列入 PDF/图纸坐标映射。

## 4. 与 lceda-sch-reader 的对比

| 维度 | lceda-sch-reader | kicad-sch-reader（本项目） |
| --- | --- | --- |
| 输入格式 | 立创EDA Pro `.eprj2`（SQLite） | KiCad `.kicad_sch`（s-expr） |
| 解析层 | SQLite + base64/gzip/NDJSON | s-expr tokenizer/parser |
| 连通性 | 精确坐标域 + 单向网络名传播 | DSU 几何连通域 + 层级/全局归并 |
| 官方校验 | 无内置 ERC 等价物 | 桥接 kicad-cli ERC |
| 规则引擎 | 未内置（靠脚本/LLM） | 内置 8 组规则 + ERC 转写 |
| 输出 | 文本/JSON 命令原语 | 同样命令原语 + MD/JSON 报告 |
| 依赖 | 仅标准库 | 仅标准库（CLI 可选） |
