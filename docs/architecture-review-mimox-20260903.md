# schematics_review_tool 架构与设计审查报告

**审查人**: mimox  
**审查日期**: 2026-09-03  
**代码基线**: 工作区当前状态（pyproject 0.1.3 / CHANGELOG 至 0.1.5）  
**审查范围**: `kicad_sch_reader/`、`scripts/`、`tests/`、`docs/`、`skill/`  
**验证动作**: 单元测试 28/28 通过；MainBoard 解析+网表 0.008s；关键算法行为探针复现（排序键、动态属性、缺失子图崩溃、电源前缀站点清点）

---

## 1. 审查范围与方法

本报告不是功能验收报告，而是**架构合理性 + 设计问题**审查。方法：

1. 通读 README / DEVELOPMENT / CHANGELOG / docs 设计文档，对齐「声称的目标」；
2. 通读核心实现（sexpr → parser → connectivity → rules → report/cli，以及 circuit_ir、LCEDA 脚本）；
3. 对可疑点用可执行探针验证（排序键、动态属性、复杂度、语义分叉）；
4. 用系统思维评估分层边界、证据模型、扩展路径是否闭环。

不审查内容：UI/图形渲染（明确 out of scope）、器件参数是否正确（需 datasheet）、用户工程本身电气设计。

---

## 2. 项目目标与定位

### 2.1 目标（综合文档自述）

| 维度 | 目标 |
| --- | --- |
| 核心能力 | 纯 Python 只读解析 KiCad 6..10 `.kicad_sch`，几何连通域网表 + 设计审查规则 |
| 扩展能力 | LCEDA `.epro`/CBB 展开；共享 Circuit IR 统一 KiCad/LCEDA 分析面 |
| 工程约束 | 零第三方依赖；`kicad-cli` 仅作 ERC/BOM/网表桥接，缺失时优雅降级 |
| 证据纪律 | 结论必须带 evidence 等级；跨板连接只产 candidate/detected，永不自动 confirmed |
| 使用方式 | CLI + JSON/Markdown 报告 + MCP server + Agent Skill |

### 2.2 定位判断

项目定位清晰：**「文件事实提取器 + 低误报规则引擎」**，而不是全自动设计正确性判定器。  
Skill 文档进一步把「器件参数是否满足」明确划给 LLM/人工 + datasheet，这条边界是对的，也和 `lceda-sch-reader` 的设计哲学一致。

**结论：目标层没有战略摇摆。** 问题主要出现在「IR 统一层尚未真正接管分析面」与「多处平行实现导致语义漂移」。

---

## 3. 架构全景

### 3.1 实际分层（代码真实状态）

```
┌─────────────────────────────────────────────────────────────┐
│ 入口层                                                      │
│   cli.py (876)  ·  mcp_server.py (417)  ·  skill/SKILL.md   │
├─────────────────────────────────────────────────────────────┤
│ 分析/规则层（尚未统一到 IR）                                │
│   rules.py (851)  Issue{official|structural|declared|heur}  │
│   cli.cmd_link_check（独立连接器比较，未走 IR）             │
├─────────────────────────────────────────────────────────────┤
│ 共享 Circuit IR（部分接入）                                 │
│   circuit_ir.py (833)  BoardIR / IRNet / IRFinding          │
│   已接入: multi_project_cross_check, diff, mcp.diff         │
│   未接入: rules 全量, review 报告, link-check CLI           │
├──────────────────────────┬──────────────────────────────────┤
│ KiCad 适配               │ LCEDA 适配                       │
│ parser.py (579)          │ lceda_epro_review.py (1023)      │
│ connectivity.py (520)    │ + repos/lceda-sch-reader         │
│ kicad_cli.py (125)       │   （外部检出，sys.path 注入）    │
├──────────────────────────┴──────────────────────────────────┤
│ 模型/解析基础                                               │
│   model.py (270)  ·  sexpr.py (168)  ·  report.py (179)     │
└─────────────────────────────────────────────────────────────┘
         输入: .kicad_sch / .kicad_pro          .epro ZIP
```

代码量（本仓库，不含 examples/repos）：核心包约 4300 行 + scripts 约 1600 行 + tests 约 690 行 ≈ **6700 行**。

### 3.2 关键数据流

```
.kicad_sch
   → sexpr.tokenize/parse          (原子树)
   → parser.load_project           (Project{SheetData, SymbolInstance...})
   → connectivity.build_local_nets (每页 DSU 连通域)
   → connectivity.build_netlist    (分层 sheet-pin / 全局标签 / 电源名合并)
   → rules.run_all_checks          (Issue 列表)
   → report.write_markdown/json
```

跨板路径：

```
KiCad Project ──board_from_kicad──┐
                                  ├─→ BoardIR ─→ compare_boards ─→ IRCrossLink
LCEDA review dict ─board_from_lceda┘
```

### 3.3 架构优点（先说对的地方）

1. **几何连通域方案正确且经官方网表交叉验证**（missing=0，precision 达标）。这是 EDA 读取工具最容易做错的部分，本项目用「最小旋转实验台 + kicad-cli 比对」锁定了坐标变换语义，纪律很好。
2. **证据分级是产品级设计**：Issue.evidence 与 IR 证据/confidence 双轨，避免把启发式建议伪装成错误。
3. **零依赖 + kicad-cli 可选**：部署边界干净。
4. **规则可配置**（`--config` 启停/改 severity），且 0.1.4 做了降噪分组，说明团队在意「报告信息密度」而不只是堆规则。
5. **跨板语义克制**：candidate/detected/declared/confirmed 四级，工具只自动产生前两级——这是对「同名 ≠ 物理连接」的正确抽象。
6. **回归资产扎实**：单元测试 + 官方网表交叉验证 + 多工程批量脚本，且 CHANGELOG 每次都写验证数字。

---

## 4. 设计问题清单（按严重度）

严重度定义：

- **P0**：正确性/语义一致性风险，可能产出错误结论或不可复现结果  
- **P1**：架构债，当前能工作但会阻碍扩展/造成双源真相  
- **P2**：工程化/可维护性，影响协作与长期演进  

---

### P0-1　`Net` 动态注入属性，模型契约被破坏

**位置**: `connectivity.py:425-426` vs `model.py:229-241`

```python
# connectivity.py 在 materialize 时注入：
group = Net(name="")
group.hier_sources = {}     # 不在 dataclass 字段中
group.label_entries = []    # 不在 dataclass 字段中
```

```python
# model.Net 字段仅有：
name, code, sheet_paths, pins, labels, global_names,
power_names, hierarchical_names, has_conflict, conflict_names, point_count
```

**问题**:

1. `Net` 作为共享数据模型，其契约被解析器单方面扩展；任何序列化、`copy`、`dataclasses.asdict`、类型检查都无法感知这两个字段。
2. `report.write_json` 只导出声明字段——`label_entries`/`hier_sources` 丢失，调试命名问题时 JSON 与内存状态不一致。
3. 静态分析与 IDE 无法提示；后续若有人在 `rules` 里读 `net.label_entries`，在「先 build_netlist 再手工构造 Net」的路径上会 `AttributeError`。

**改法**: 把 `hier_sources: Dict[str, Set[str]]`、`label_entries: List[Tuple[int, str]]` 声明为 dataclass 字段（默认 factory），或在 materialize 阶段构造专用中间类型再投影到 `Net`。

---

### P0-2　未命名网络 `N$` 排序键错误，编号不稳定且语义混乱

**位置**: `connectivity.py:461`

```python
for order, group in enumerate(sorted(
    named_or_pinned_groups,
    key=lambda n: sorted(n.pins[0].ref if n.pins else "")
)):
```

**探针复现**:

| ref | `sorted(ref)` 实际键 | 字典序位置 |
| --- | --- | --- |
| `""`（无引脚） | `[]` | 1（最前） |
| `R101` | `['0','1','1','R']` | 2 |
| `J102` | `['0','1','2','J']` | 3 |
| `C205` | `['0','2','5','C']` | 4 |
| `U3` | `['3','U']` | 5 |

**本意**应是按首位号排序：`['', 'C205', 'J102', 'R101', 'U3']`。  
**实际**是对字符串做 `sorted()`，变成「按字符多重集」排序——`R101` 排在 `J102` 前、`C205` 排在 `J102` 后，与任何工程直觉都不符。

**数学后果**:

- `N$k` 的编号函数 `f(group) = order_in_sorted_list + 1` 依赖于错误的全序；
- 只要工程中多了一个无引脚纯标签域（`[]` 键最小），**所有** `N$` 编号整体平移；
- 两次审查报告的 `N$` 编号不可 diff，跨版本对比（`diff_boards`）会把「编号漂移」误判为网络增删。

**改法**:  
`key=lambda n: (n.pins[0].ref if n.pins else "\xff", n.name or "")`  
或对 unnamed 组用 `(sheet_path, first_ref, pin_count)` 做稳定键。并补一条「N$ 编号稳定性」回归测试。

---

### P0-3　电源符号判定在多处平行实现，语义不一致

**文档已明确**（DEVELOPMENT.md §3.4）：

> 电源符号不一定在 `power:` 库；判定以 lib_symbols 的 `(power)` 标志为准，兜底为 `#PWR*` 单引脚 power_in。**仅看 lib_id 前缀会把 complex_hierarchy 等 demo 的全部电源网打成 N$。**

但代码中 **8 处业务逻辑**仍在用 `lib_id.startswith("power:")` 作为电源/排除依据（`model.is_power_symbol` 属性本身实现正确，但调用方大多没用它）：

| 位置 | 用途 | 风险 |
| --- | --- | --- |
| `model.Net.pin_count` (`model.py:242`) | 统计时排除电源脚 | 工程本地电源库符号被算成负载 |
| `rules._is_capacitor` (`rules.py:74`) | 去耦电容识别 | 误排除/误纳入 |
| `rules.check_single_pin_nets` (`rules.py:205`) | 单脚网 only_power 判断 | 本地电源库的单脚电源网被标 warning 而非 info |
| `rules.check_power_decoupling` (`rules.py:280`) | 排除电源符号 | 同上 |
| `rules._is_power_like` (`rules.py:691`) | N$ 命名统计排除 | 未命名占比虚高 |
| `rules.check_interface_direction` (`rules.py:798`) | 过滤电源成员 | 本地电源符号进入方向分析 |
| `cli.cmd_interfaces` (`cli.py:600`) | 同上 | 同上 |
| `parser.parse_symbol_instance` (`parser.py:272`) | 未知 lib 时 etype 推断 | 次要 |

`SymbolInstance.is_power_symbol` 属性本身是**正确**的（`power` flag + `#PWR` 兜底），但调用方大多没用它。

**系统性影响**:  
同一工程在「连通域层」与「规则层」对「这是不是电源符号」可能给出不同答案 → R302/R402/R501 的误报模式随库组织方式漂移。这是**双源真相**。

**改法**: 全部改为 `sym.is_power_symbol` / 传入的 `PinNet` 上增加 `is_power` 布尔（由连通域层一次判定后写入），规则层禁止再看 lib_id 前缀。

---

### P0-4　`link-check` CLI 与 Circuit IR 跨板比较语义分叉

**位置**: `cli.py:511-596`（`cmd_link_check`） vs `circuit_ir.compare_boards`

| 维度 | CLI `link-check` | IR `compare_boards` |
| --- | --- | --- |
| 连接器识别 | 内联：`conn` in lib_id 或 ref[0] in JPH | `_looks_like_connector`（含 keywords/testpoint 排除） |
| 网络名比较 | `a_net == b_net` **原始字符串** | `normalize_net` 后比较（去层级前缀、DXN_0→GND、大小写） |
| 输出对象 | 自建 dict | `IRCrossLink` + evidence/confidence |
| score/confidence | 无 | 有 |

**后果**:

1. 跨 KiCad/LCEDA 或层级前缀不同的工程时，CLI 会漏报（`/AFE_OUT_P` vs `AFE_OUT_P` 不等）；
2. 文档与 CHANGELOG 声称「统一走 Circuit IR」，但主命令 `link-check` **没有**走 IR——这是架构承诺与实现的偏离；
3. 同一对连接器，`link-check` 与 `multi_project_cross_check` 可能给出不同 exact 计数。

**改法**: `cmd_link_check` 改为 `board_from_kicad` ×2 + `compare_boards`，CLI 只做渲染；方向语义提示（`dir_note`）下沉到 IR 的 diffs 结构。

---

### P1-1　`Issue` 与 `IRFinding` 双轨并行，证据枚举未统一

```
Issue.evidence:     official | structural | declared | heuristic
IREvidence.kind:    direct | calculated | datasheet | declared | inferred | ai
```

文档 `docs/shared-circuit-ir.md` 写明「把 rules.py 的 Issue 逐步迁移为 IRFinding」，但：

- `rules.py` 22 处全部构造 `Issue`，零处 `IRFinding`；
- `report.write_json` 序列化的是 `Issue`，不是 `IRFinding`；
- 两套 evidence 词汇只有 `declared` 交集。

**系统判断**: IR 目前是「跨板专用旁路」，不是「统一分析层」。分层图（docs 中的四层）在文档里成立，在调用图里不成立。

**改法（渐进，不必一次改完）**:

1. 先定义映射表：`structural→direct`，`heuristic→inferred`，`official→direct(official source)`；
2. `Issue` 增加 `to_ir_finding()`，review 输出双写一个版本；
3. 新规则只允许产出 `IRFinding`。

---

### P1-2　`find_net_for` 线性扫描，层级合并复杂度偏高

**位置**: `connectivity.py:353-357`

```python
def find_net_for(path: str, net: _LocalNet) -> Optional[int]:
    for i, n in enumerate(local_by_sheet.get(path, [])):
        if n is net:
            return union.find(index[(path, i)])
    return None
```

**复杂度**:  
设某父页 sheet-pin 数为 \(P\)，子页局部网数为 \(N\)，则层级合并阶段：

\[
T_{\text{hier}} = O(P \cdot N)
\]

对当前 MainBoard（5 页 / 182 网 / 780 线）实测总耗时 8ms，**不是现实瓶颈**。  
但对「多子图复用 + 大连接器」工程（每子图数百网 × 数十 sheet-pin），会进入 \(10^5\)–\(10^6\) 量级无谓比较。

**改法**: 在 `build_local_nets` 返回时附带 `id(net) → flat_index` 映射，`find_net_for` 变 \(O(1)\)。

---

### P1-3　标签吸附容差与坐标量化网格不一致

**位置**: `connectivity.py:28,138`

```python
EPS_MM = 0.001          # qpoint 网格 = 1 μm
...
best_d = 0.01           # 标签贴线容差 = 10 μm
```

**数学含义**:

- 量化网格 \(g = 10^{-3}\,\mathrm{mm}\)；
- 吸附阈值 \(\tau = 10^{-2}\,\mathrm{mm} = 10g\)。

标签距导线 \(d \in (g, \tau)\) 时：不会落到已有 DSU 节点，但会被吸附并 union——行为正确。  
标签距导线 \(d \in (\tau, \infty)\) 时：视为悬空标签（R303）。

风险在于 \(\tau\) 是硬编码魔法数，且与 \(g\) 无文档化关系。若未来有人把 `EPS_MM` 调粗（例如 0.01），吸附会静默失效。

**改法**: `LABEL_SNAP_MM = 10 * EPS_MM`，并在 DEVELOPMENT 中写明容差来源；或对标签也做 qpoint 后在邻域 3×3 搜索（与 LCEDA 侧 `_pin_direct_nets` 的邻域搜索对齐）。

---

### P1-4　LCEDA 侧「上帝模块」+ monkey-patch

**位置**: `scripts/lceda_epro_review.py`（1023 行）

- `EproDB` 同时承担：ZIP 后端、页索引、override 缓存、符号 pin 解析、device map；
- `_monkeypatch_epro_overrides()` 在 import 时给类挂方法（`lceda_epro_review.py:276-299`）；
- 依赖 `repos/lceda-sch-reader` 通过 `sys.path.insert` 注入，**未打包、无版本钉扎**。

这与本项目自己在 `docs/lceda-sch-reader-design-review.md` 里批评上游「单文件混层、无测试、缓存无上限」是同一类问题——只是换了个文件名。

**改法**:

1. 拆成 `epro_db.py` / `cbb_expand.py` / `epro_review.py`；
2. monkey-patch 改为构造时注入或显式子类；
3. `repos/lceda-sch-reader` 做成可选 extra / git submodule + 版本记录（CHANGELOG 已有 commit hash 记录，但运行时无检查）。

---

### P1-5　缺失子图文件导致 `load_project` 崩溃，R601 无法生效

**位置**: `parser.py:550-555`（`load_project`） vs `rules.check_hierarchical_sheet_pins`（R601）

```python
resolved = next((c for c in candidates if c.exists()), candidates[0])
# 文件不存在时仍入队 → parse_sheet_file → file.read_text() → FileNotFoundError
```

**探针复现**（`TEST_SCRIPTS/probe_missing_sheet_20260903.py`）:

```
LOAD FAILED: FileNotFoundError: .../missing_child.kicad_sch
=> R601 cannot fire; load_project crashes on missing child file
```

**问题**:

1. 规则 R601（「分层图纸文件缺失」，severity=error）设计意图是**审查时报告**缺失子图；
2. 但加载阶段就崩溃，审查流程根本跑不到 rules；
3. CLI `main()` 虽捕获 `FileNotFoundError` 返回退出码 2，用户只看到一句 error，得不到结构化报告；
4. 真实工程中「删了子图文件但 sheet 符号还在」是常见脏状态，工具应可继续审查其余页。

**改法**: `load_project` 对不存在的 child file 记入 `project.missing_sheets` 并跳过入队；R601 改读该列表。加载失败仅在**根图**缺失时发生。

---

### P1-6　`resolve_root_file` 用「文件头 200KB 是否含 sheet_instances」猜根图

**位置**: `parser.py:509-516`

```python
nodes = sexpr.parse(f.read_text(...)[:200000])
if ... sexpr.first(nodes[0], "sheet_instances"):
    return f.resolve()
```

**问题**:

1. `sheet_instances` 在 KiCad 文件中通常位于**文件末尾**；截断 200KB 后大概率看不到 → 启发式经常失效，静默落到 `sch_files[0]`；
2. 截断可能切在字符串/列表中间，`sexpr.parse` 抛异常被 `except: continue` 吞掉；
3. 多 `.kicad_sch` 且无 `.kicad_pro` 时，根图选择依赖 `sorted()` 文件名顺序——**不确定**。

**改法**: 优先 `.kicad_pro` → 其次「含 `sheet_instances` 的完整文件」（不截断，或从文件尾部读）→ 再 fallback；失败时警告而不是静默。

---

### P2-1　报告默认输出路径与 CHANGELOG 承诺不符

CHANGELOG 0.1.2：「默认输出到 `reports/` 且文件名带时间戳」。  
实际 `cli.py:464`：

```python
out_md = args.out_md or str(Path.cwd() / f"{name}.review.md")
```

默认写到 **当前工作目录**，且**无时间戳**（会覆盖）。用户全局规则也要求生成文件带时间戳防覆盖——工具自身未遵守。

---

### P2-2　`sexpr.find_all` / `load_project` 使用 `list.pop(0)`

```python
# sexpr.py:125
node = stack.pop(0)          # O(n) per pop → 整体 O(n²)
# parser.py:532
path, file = queue.pop(0)    # 同上，BFS 队列
```

对当前规模无感（探针：深嵌套 ×1000 = 13ms），但是教科书级低效。应改 `collections.deque.popleft()` 或 `stack.pop()`（若无需 BFS 顺序）。

---

### P2-3　测试夹具被 `.gitignore` 整目录排除

```
examples/
repos/
```

`tests/test_reader.py` 与 `validate_examples.py` **强依赖** `examples/`。新 clone 无法跑测试，CI 无法建立。  
「只读用户工程」的意图可以理解，但至少应：

- 提供最小合成夹具（`tests/fixtures/`，项目已有一个 `mini.kicad_sch`）；
- 或 `examples/` 改为 submodule / 文档化获取步骤。

---

### P2-4　`cli.py` / `rules.py` 单文件偏大，命令与实现耦合

- `cli.py` 876 行：20 个子命令的业务逻辑（trace BFS、link-check 比较、bridges 配对）全在 CLI 层；
- `rules.py` 851 行：14 条规则 + 配置加载 + R902 词法分析。

Library 调用方（MCP server）只能重复 import 内部函数，无法 `from kicad_sch_reader import review`。`mcp_server.py` 已经在重新实现 review 组装逻辑（`_tool_review`），这是重复。

**改法**: 抽出 `kicad_sch_reader/services.py`（或 `api.py`）：`run_review(project) -> ReviewResult`，CLI/MCP/Skill 共用。

---

### P2-5　规则阈值硬编码且文档自承「NOT yet configurable」

```python
# rules.py:66-69
# Net-naming rule thresholds (built-in heuristic defaults; NOT yet
# configurable — review --config only supports enabled/severity today).
_UNNAMED_RATIO_WARN = 0.3   # line 68
_UNNAMED_COUNT_WARN = 20    # line 69
```

去耦「同网络存在电容」也是存在性检查而非就近检查（路线图已列）。对审查工具而言，阈值不可配置会迫使用户用 `enabled: false` 粗暴关闭整条规则。

---

## 5. 系统思维：架构是否合理

### 5.1 用「编译器类比」评估分层

项目自己在 `docs/shared-circuit-ir.md` 用了「编译器式分层」类比，这个类比很贴切，据此打分：

| 编译器阶段 | 本项目对应 | 完成度 | 评价 |
| --- | --- | --- | --- |
| 词法/语法 | sexpr | 高 | 干净、够用 |
| AST/IR 前端 | parser / lceda_epro | 中高 | KiCad 侧好；LCEDA 侧过重 |
| 中端 IR | circuit_ir.BoardIR | **中低** | 类型齐了，但 rules/review 未消费 |
| 后端/优化 | rules | 中 | 规则丰富，但双源真相 |
| 代码生成 | report / MCP | 中 | 输出形态全，API 层缺失 |

**核心判断**: 前端（解析+连通域）是项目最强资产；**中端 IR 是半成品**——它正确地服务了跨板场景，却还没成为唯一分析真相源。当前系统是「前端强 + 两条并行分析路径」，不是单管道。

### 5.2 控制复杂度的策略评估

| 策略 | 是否采用 | 效果 |
| --- | --- | --- |
| 零依赖 | 是 | 部署简单，但失去现成 s-expr/图库；自研成本可控 |
| 几何连通域 + 官方网表锚定 | 是 | **极好**，正确性有外部 oracle |
| 证据分级 | 是 | 好，防止 LLM/人把 heuristic 当 error |
| 规则分组降噪（0.1.4） | 是 | 好，报告可用性显著提升 |
| IR 统一分析 | 半 | 跨板好了，规则层未收口 |
| 单文件脚本快速迭代 | 部分 | 短期快，LCEDA 侧已付出上帝模块代价 |

### 5.3 扩展性压力点

若继续按路线图推进（文本变量、总线、就近去耦、PDF 坐标映射、PyPI、统一 schema）：

1. **总线成员解析**需要在 connectivity 增加「成员网」概念——若不先把 `Net` 模型契约修干净（P0-1），会继续动态打补丁；
2. **就近去耦**需要几何距离查询——应复用现有 qpoint 网格建空间索引，而不是再写一套距离逻辑；
3. **统一审查 schema** 必须先消灭 Issue/IRFinding 双轨（P1-1）；
4. **PyPI 发布**要求 `examples/` 夹具策略（P2-3）与 `repos/` 依赖（P1-4）先解决。

### 5.4 总体架构合理性评分

| 维度 | 分数 (1-5) | 说明 |
| --- | --- | --- |
| 目标清晰度 | 5 | 只读、证据、边界说明完整 |
| 分层正确性 | 3.5 | 意图对，IR 未收口 |
| 正确性工程 | 4.5 | 官方网表 oracle + 旋转实验台是亮点 |
| 一致性 | 3 | 电源判定、link-check、报告路径多处分叉 |
| 可测试性 | 4 | 有测试，但夹具不可移植 |
| 可扩展性 | 3.5 | 规则可插；模型/IR 契约需先修 |
| 工程化 | 3 | 无 CI，大文件，sys.path 注入 |

**综合：这是一个「正确性内核优秀、架构收口未完成」的项目。** 不是推倒重来的问题，而是把已写对的 IR 真正接到分析主管道上。

---

## 6. 改进建议（按优先级）

### 立即（1-2 天，低风险高收益）

1. **修 N$ 排序键**（P0-2）+ 稳定性回归测试。  
2. **电源判定收口**（P0-3）：规则层全部改走 `is_power_symbol` / `PinNet.is_power`。  
3. **`Net` 声明动态字段**（P0-1）。  
4. **`cmd_link_check` 改走 IR**（P0-4），消除双实现。  
5. **review 默认输出**改为 `reports/<name>.review-<timestamp>.md`（P2-1）。

### 短期（1 周）

6. `Issue.to_ir_finding()` + evidence 映射表；review JSON 增加 IR 摘要（P1-1 第一步）。  
7. `find_net_for` 建 id→index 映射（P1-2）。  
8. 抽出 `api.run_review()`，MCP/CLI 共用（P2-4）。  
9. `load_project` 对缺失子图降级为 `missing_sheets` 而非崩溃（P1-5）。  
10. `resolve_root_file` 去掉 200KB 截断启发式（P1-6）。

### 中期（与路线图对齐）

11. 拆分 `lceda_epro_review.py`，钉扎 lceda-sch-reader 版本（P1-4）。  
12. 最小合成夹具进仓库，恢复可 CI（P2-3）；加 GitHub Actions：`unittest` + `validate_examples`。  
13. 规则阈值进 `--config`（P2-5）；去耦升级为网格空间索引上的就近检查。  
14. 总线成员 / 文本变量：先冻结 `Net`/`BoardIR` schema 再加字段。

### 不建议做的事

- 不要把 LCEDA 解析「重写进」`kicad_sch_reader` 核心包——分格式前端是对的。  
- 不要在未统一 evidence 词汇前，给 rules 加更多「智能推断」类规则——会加重双轨。  
- 不要为追求零误报把 structural 规则默认降成 info——0.1.4 的分组策略更健康。

---

## 7. 结论

`schematics_review_tool`（kicad-sch-reader）在 **KiCad 几何连通域、官方网表锚定验证、证据分级、跨板候选语义** 上达到了相当高的工程水准，明显不是一次性脚本，而是有知识沉淀的审查内核。

主要架构风险不在「算法错了」，而在：

1. **统一 IR 半接入**——分析面仍有两条真相源；  
2. **电源/连接器等关键谓词多处复制**——文档已警告过的坑，代码仍部分踩着；  
3. **个别正确性细节（N$ 排序键、动态属性）会侵蚀可复现性**。

建议按第 6 节「立即」五项先收口正确性与一致性，再推进路线图功能。收口完成后，本工具具备成为「跨 EDA 统一原理图事实层」的架构基础。

---

*本报告由 mimox 基于源码静态审查 + 可执行探针生成。所有行号引用对应 2026-09-03 工作区状态，并经 `TEST_SCRIPTS/verify_review_citations_20260903.py` 与 `TEST_SCRIPTS/probe_missing_sheet_20260903.py` 校验。*
