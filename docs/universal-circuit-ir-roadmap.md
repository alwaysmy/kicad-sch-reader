# Universal Circuit IR 路线图

> 依据：ChatGPT 架构评审意见（docs/chatgpt-architecture-opinions.md）
> 整理：2026-09-19
> 原则：Parser 只负责格式；统一 IR 表达电路概念；Analysis 与 Rules 分离；AI 只看 IR。

## 1. 目标定位

把 EDA project 编译成可查询、可分析的电路模型，而不是把文件格式模型当内部模型。

目标问题示例：

- 有哪些电源域？
- 3V3 谁产生、谁消耗？
- CAN 总线在哪里、有几个节点？
- 两块板通过什么连接器相连？
- ADC 输入经过哪些器件？
- 这个 GPIO 最终控制了什么？

这些问题优先由确定性 Analysis/Graph 回答；LLM 负责判断设计是否合理。

## 2. 目标分层

    KiCad ----\
    LCEDA ----+--> Format Adapter -> Universal Circuit IR -> Circuit Graph
    Altium ---/                                                |
                                                               +--> Analysis -> Rules -> Finding
                                                               |
                                                               +--> AI Reasoner

关键边界：

- Parser / Adapter：只负责读懂源格式，不做审查。
- Universal IR：Project / Board / Sheet / Component / Pin / Net / Connection /
  Connector / Interface / PowerDomain / BoardConnection。
- Graph：NetGraph / SignalGraph / PowerGraph / InterfaceGraph。
- Analysis：电路是什么（拓扑、电源域、信号链、接口）。
- Rules：这样设计是否合理（确定性规则）。
- Knowledge：datasheet / MPN / 封装 / 接口约束结构化事实。
- AI：读取 IR 摘要与 Finding，不直接读原始 .kicad_sch。
- Finding：统一对象，带证据来源和 confidence。

## 3. 当前仓库映射

已有基础：

- `kicad_sch_reader/circuit_ir.py`：BoardIR / IRComponent / IRPin / IRNet /
  IRCrossLink / IRSystem / 证据等级。
- `kicad_sch_reader/parser.py`：KiCad parser。
- `scripts/lceda_epro_review.py`：LCEDA .epro parser + CBB 展开适配。
- `kicad_sch_reader/rules.py`：确定性规则 R101...R902。
- `scripts/multi_project_cross_check.py`：多工程跨板候选检查。
- `skill/SKILL.md`：LLM 手册查询、power 判断、证据要求。

差距：

- IR 已有骨架，但还没有 Project / Sheet / Interface / PowerDomain 的完整对象。
- Graph 层只有隐式 BFS trace，没有独立的 Net/Signal/Power/Interface Graph。
- Analysis 与 Rules 仍混在部分规则实现里。
- Datasheet 知识层尚未对象化。
- BoardConnection 还没有声明式映射文件与状态机（当前有 --pin-map 雏形）。
- AI context 仍直接给报告 JSON，未形成稳定的上下文协议。

## 4. 分阶段路线

### P0 已完成

- KiCad / LCEDA 两个 Adapter 能产出 BoardIR。
- 精确连通域、网络归并、trace、CBB 展开。
- 多工程跨板 candidate/detected + 证据等级。
- power-aware trace（结构证据优先）。

### P1 IR 对象模型补全

- Project / Board / Sheet 层级对象。
- ComponentRole（MCU / Buck / ADC / Transceiver / Connector）。
- ElectricalSemantics：Pin 的 electrical_type / direction / power_role / function。
- PowerDomain / Interface / Signal 作为一等对象。
- Evidence 从 finding 扩展到所有推导结果。

验收：同一个 BoardIR 能同时导出 NetGraph、PowerGraph、InterfaceGraph。

### P2 Graph 层独立

- NetGraph：只表达物理网络。
- SignalGraph：跨电阻/电容/电感/连接器的信号路径。
- PowerGraph：电源域与来源/负载。
- InterfaceGraph：SPI / I2C / UART / CAN / USB / JTAG 等接口实例。
- TraversalPolicy：include_power 作为策略，而不是名字黑名单。

验收：trace 走 signal graph 时不跨非 0 欧器件；走 net graph 时只做物理连通。

### P3 Analysis / Rules 分离

- Analysis 输出事实：电源域、负载、轨道、信号路径、接口节点。
- Rules 只消费 Analysis 事实做判定。
- 规则结果统一为 Finding。

验收：新增规则不需要修改 parser 或 graph。

### P4 Datasheet / Knowledge 层

- 结构化 datasheet 事实：MPN、引脚、电压范围、电流能力、时序、接口约束。
- 本地手册检索：Everything -> PDF 文本 -> 结构化 JSON。
- 找不到本地手册时用 Kimi WebBridge / 官方页面补充。
- LLM 只能通过 Finding evidence 引用 datasheet 事实。

验收：例如 TPS563201 EN 阈值判断输出
`source=datasheet, ref=U6, pin=EN, confidence=calculated`。

### P5 多板项目与 BoardConnection

- Project 层：多个 BoardIR + 连接关系。
- BoardConnection 字段：from/to、connector、mapping、confidence、evidence。
- confidence：declared / detected / inferred / assumed / unknown。
- link-check / multi_project_cross_check 只产生 candidate 或 detected；declared 必须来自用户或项目 metadata。
- --pin-map 作为 declared mapping 输入。

验收：MainBoard J102 对 PowerBoard J103 输出 detected；DigitalBoard CN7 对 MainBoard J101 输出信号重合为 0 的候选并说明原因。

### P6 AI Context 协议

- 给 LLM 的上下文 = IR 摘要 + Finding + Analysis 事实 + datasheet 事实。
- 不直接给原始 .kicad_sch / .epro。
- 每条 Finding 可追溯到 direct / calculated / datasheet / inferred / ai。

## 5. 证据与 confidence 约定

| 来源 | 含义 | 例子 |
| --- | --- | --- |
| direct | 文件直接事实 | 引脚名称、网络名 |
| calculated | 由 IR/Graph 推导 | 网络连通、电源域、跨板同名匹配 |
| datasheet | 手册事实 | EN 阈值、输出电流 |
| inferred | 规则或 AI 推断 | 电源过载风险 |
| ai | LLM 判断 | 设计意图不一致 |

confidence：confirmed / detected / candidate / inferred / declared / unknown。
物理连接绝不能因为同名网络自动升级为 confirmed。

## 6. 决策与反模式

必须避免：

- KiCad Parser 直接调用 Rules。
- LCEDA Parser 直接产 Review 结论。
- 用网名正则代替 power 结构判断。
- 把 Net 当 Signal，忽略电阻/电容/连接器造成的逻辑边界。
- 让 AI 直接读原始文件并自由猜测。
- 把未知的跨板连接自动写成 confirmed。

## 7. 下一步清单

- [ ] 补完 IR 对象模型（Project/Sheet/Interface/PowerDomain）。
- [ ] 把 trace 迁移到独立 Graph + TraversalPolicy。
- [ ] Analysis 与 Rules 目录/接口分离。
- [ ] Datasheet 事实 JSON schema + 本地手册检索脚本。
- [ ] BoardConnection 声明文件格式与 --pin-map 完整校验。
- [ ] AI context 导出协议（JSON schema）。
- [ ] 为上述每层补回归测试。
