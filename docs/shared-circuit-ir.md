# 共享 Circuit IR 设计（采纳 ChatGPT 架构评审意见）

## 结论

**采用** `kicad_sch_reader/circuit_ir.py` 作为 KiCad 与 LCEDA 两条数据源的
统一分析层。解析器继续保留格式专属实现（KiCad 为 `parser.py`，LCEDA 为
`scripts/lceda_epro_review.py` + lceda-sch-reader），分析/跨板检查只面向
`BoardIR`。

这是“编译器式分层”的第一步，而不是把所有 EDA 解析器合并成一个文件。

## 分层

```
+---------------------------------------------------------------+
| 分析层: rules / cross-board / trace / LLM skill                |
|   -> 只消费 BoardIR / IRNet / IRComponent / IRCrossLink        |
+---------------------------------------------------------------+
| Circuit IR: kicad_sch_reader/circuit_ir.py                     |
|   -> BoardIR(components, nets), NetKind, Evidence, Finding     |
+-----------------------------+---------------------------------+
| KiCad adapter              | LCEDA adapter                     |
| parser.py + connectivity.py| lceda_epro_review.py + epro DB    |
+-----------------------------+---------------------------------+
| .kicad_sch files           | .epro ZIP + .esch/.esym/.eins     |
+-----------------------------+---------------------------------+
```

## IR 对象

| 对象 | 作用 |
| --- | --- |
| `BoardIR` | 一块板的图：`components`、`nets`，可按位号/网络反查 |
| `IRComponent` | 板级位号；多 unit/CBB 内部位号折叠到一个节点，引脚保留来源 sheet |
| `IRComponentPin` | 引脚号、名称、电气类型、canonical net |
| `IRNet` | 网络节点：`kind`、成员引脚列表、labels、电源 sources |
| `IRNetMember` | 图中的一条连接边（ref.pin 属于 net） |
| `IREvidence` | 证据等级：`direct|calculated|datasheet|declared|inferred|ai` |
| `IRFinding` | 通用审查发现对象；后续规则应逐步迁移到该对象 |
| `IRCrossLink` | 两块板连接器候选对，带 score / confidence / evidence |
| `IRSystem` | 多板工程层：boards + links，对应 ChatGPT 建议的 project 层 |

## Net kind 判定顺序

1. 精确地网络名 → `ground`
2. 结构电源证据（电源符号 / `power_in` / `power_out` 引脚）→ `power`
3. 连接器或 CBB 模块引脚 → `interface`
4. 命名正则或 LCEDA `POWER_NET_RE` / `--power-net` → `power`
5. 默认 → `signal`

命名永远只是兜底，不是第一证据。

## 跨板证据等级

- `candidate`：只有相同 pin 号 + 归一化网络名一致的候选对。
- `detected`：score == 1.0 且至少 2 个 pin（例如 MainBoard J102 ↔
  PowerBoard J103 的 16/16），仍不自动确认。
- `declared`：用户声明或工程 metadata 声明的对插关系。
- `confirmed`：上述声明 + 工具复核一致后才可使用。

`compare_boards()` 只会产生 `candidate|detected`；`confirmed` 必须由
上层显式声明。

## 已接入点

- `scripts/multi_project_cross_check.py`：加载 KiCad/LCEDA 后全部走
  `board_from_kicad` / `board_from_lceda` / `compare_boards`。
- `tests/test_circuit_ir.py`：两个适配器 + 跨板检测的回归测试。

## 下一步（路线图）

- 把 `rules.py` 的 `Issue` 逐步迁移为 `IRFinding`（保留旧输出兼容）。
- `review`/`trace` 命令输出增加 IR 摘要（net kind 统计、interface 列表）。
- 在 `IRSystem` 上实现 declared-links 的显式声明文件（例如
  `board-links.json`），把 `declared` 与 `detected` 分层。
- lceda-sch-reader 保持为 LCEDA parser/adapter，不再向其中塞分析逻辑。
