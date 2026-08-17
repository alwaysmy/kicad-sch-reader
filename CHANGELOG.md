# 变更记录（CHANGELOG）

本项目采用语义化版本。所有重要变更按时间倒序记录。

## [0.1.2] - 2026-08-18

### 新增/修复（NIM 审查问题与经验 v2 实测驱动）

- LCEDA 多 Part 符号支持完整 PART 名（B0/B14/GTP/POWER 等字母名）
- 同器件重名引脚以 `name#number` 为键，修复 SHORT `Pin1/Pin1`、ESD
  `IN/IN`、`NC/NC` 导致的网络错误合并
- `pin_net_map` 保留每个引脚自己物理端点命中的网络名，alias 组仅用于
  跨名查询/成员分组
- 连通性策略修订：仅 SHORT(symbolType=22)/0Ω 跳线脚本化直连；普通电阻/
  电感/LED/磁珠两侧网络不再自动合并，器件作为中间 hop 输出
- `component_bridges`：LCEDA 报告新增两脚中间器件桥接表
- `.epro` CLI 自动解包支持：`lceda_reader.py --eprj xxx.epro ...`，
  打印解包日志
- `netfind --exact`：KiCad 未命名网络精确查询
- `bridges` 命令：KiCad 两脚器件/排阻 `Rk.1 ↔ Rk.2` 通道桥接对导出
- 跨工具比对 `DXN_0 -> GND` 归一化
- 默认输出到 `reports/` 且文件名带时间戳
- 修订文档：`原理图审查工具问题与经验v2.MD`（NIM DesignDocs）

### 验证

- 单元测试 29/29 通过
- KiCad 官方网表交叉验证保持 735/735 与 313/313
- 数字板实测：260 位号 / 272 网络 / 59 findings；U1 pin_net_map 322 条；
  U3 关键引脚与坐标法一致；CBB3.VOUT4=VCC_3V3；R26 1kΩ 上拉不再并入电源轨

## [0.1.1] - 2026-08-18

### 新增

- 共享 Circuit IR：`kicad_sch_reader/circuit_ir.py`
  - `BoardIR`（components/nets/pins/connections）统一 KiCad 与 LCEDA 数据源
  - net kind：`signal|power|ground|interface`，结构证据优先、命名正则兜底
  - `IREvidence` / `IRFinding` / `IRCrossLink` / `IRSystem` 多板工程层
  - 跨板证据等级：`candidate|detected|declared|confirmed`，工具只自动产生
    前两级
  - 适配器 `board_from_kicad()` / `board_from_lceda()`
  - 设计文档：`docs/shared-circuit-ir.md`
- `scripts/multi_project_cross_check.py`：KiCad + LCEDA 混合多板检查，内部
  全部改走共享 IR；报告每行增加 evidence 列
- LCEDA 多单元器件自动判定：
  - 同页/跨页同 `Unique ID` + 不同 title → `MULTI_UNIT_CONFIRMED`
  - 同 `Unique ID` + 同 title → `POSSIBLE_REUSED_INSTANCE`
  - 其余跨页重复 → `MULTI_UNIT_UNVERIFIED`
- `--trace-skip-power` / `--power-net`：trace 的电源网络跳过与用户命名补充
- `skill/SKILL.md`：手册查阅协议、电源判断层级、跨板证据等级
- 测试：`tests/test_circuit_ir.py`（7 项共享 IR 回归）

### 验证

- 单元测试 24/24 通过（含 CBB 展开、共享 IR、旋转实验台）
- KiCad 官方网表交叉验证：
  - MainBoard common=735/735、missing=0、name_mismatch=0、precision=1.0
  - PowerBoard common=313/313、missing=0、name_mismatch=0、precision=1.0
- 混合多板检查：3 板 / 72 候选连接对，MainBoard J102 ↔ PowerBoard J103
  保持 `detected(score=1.0, 16/16)`

## [0.1.0] - 2026-08-17

### 新增

- `kicad_sch_reader` 包：纯 Python 标准库实现
  - S-expression 解析器（`sexpr.py`），兼容引号字符串转义
  - KiCad 6..10 `.kicad_sch` 解析器（`parser.py`），兼容新旧 lib pin 写法
  - 分层工程递归加载，sheet-path 组织图纸
  - 几何连通域网表（`connectivity.py`）
    - 导线/junction/标签/电源符号/引脚直接接触的统一 DSU 归并
    - 同页同名标签、跨页全局标签、父子 sheet-pin 层级归并
    - 电源网络优先命名与多全局名冲突检测
  - 审查规则引擎（`rules.py`）：8 组自有规则 + KiCad ERC 转写
  - `kicad-cli` 桥接（`kicad_cli.py`）：ERC JSON、网表、BOM 导出
  - Markdown/JSON 审查报告（`report.py`）
  - CLI（`cli.py`）：parse/sheets/components/pins/nets/netfind/find/trace/
    review/validate/erc/export-netlist/export-bom/link-check
  - `link-check`：跨板连接器逐 pin 网络名核对（MainBoard J102 ↔ PowerBoard
    J103 实测 16/16 一致）
  - 网络命名对齐 kicad-cli：`/Label`、`/Sheet Name/Label`、电源/全局名无前缀
- 入口脚本 `kicad-sch-reader.py` 与 `pyproject.toml`
- 文档：`README.md`、`DEVELOPMENT.md`、`CHANGELOG.md`、
  `docs/kicad-tools-survey.md`、`docs/lceda-sch-reader-design-review.md`
- 测试：
  - `tests/test_reader.py`（以 `examples/` 两工程为夹具，含旋转实验台）
  - `tests/validate_examples.py`（与 kicad-cli 官方网表逐引脚交叉验证）

### 验证

- MainBoard：5 页 / 484 符号 / 182 网络 / 964 引脚连接（含电源符号）；
  官方 ERC 20 warnings；审查报告合计 48 条发现
- PowerBoard：1 页 / 234 符号 / 52 网络 / 424 引脚连接（含电源符号）；
  官方 ERC 11 errors；审查报告合计 21 条发现
- 官方网表交叉验证（排除 #PWR 与 unconnected 伪网络）：
  - MainBoard common=735/735、missing=0、name_mismatch=0、precision=1.0
  - PowerBoard common=313/313、missing=0、name_mismatch=0、precision=1.0

### LCEDA .epro / CBB 审查

- 新增 `scripts/lceda_epro_review.py`：
  - 读取 `.epro`（ZIP：project.json + SHEET/SYMBOL/INSTANCE）
  - 兼容 lceda-sch-reader 的 parse_sheet/连通域函数
  - CBB 展开：识别 symbolType=17 复用模块、应用 `.eins` 位号/器件覆盖、
    以端口名连接母图与 CBB 子图网络
  - CBB 内部展开明细：端口→内部网络→内部器件逐 pin 连接
  - `--trace-net` / `--trace-ref`：trace 可穿透 CBB 端口显示内部器件
  - 修复 `lceda_reader._collect_pinmap_data` 对 symbolType=17 的漏读
  - LIA_DigitalBoard_RevA 审查报告：
    `reports/LIA_DigitalBoard_RevA.lceda-review.md` / `.json`
- 新增 `tests/test_lceda_epro.py`：7 项 CBB 展开/trace 回归测试

### 调研与设计输入

- 拉取并评审 `alwaysmy/lceda-sch-reader`（私有仓库已应要求改为 public）
- 调研 KiCad 原理图审查工具 20+ 项，详见 `docs/kicad-tools-survey.md`
- 从 lceda-sch-reader 借鉴：只读标准库、连通域精确方案、trace/netfind、
  JSON 输出、工程通用性；针对 KiCad 新增：官方 ERC 桥接与审查规则

### 已知限制

- 分层网络命名与官方 `/Sheet/Label` 前缀未完全对齐（语义一致）
- 不解析总线成员与文本变量
- 去耦检查为“同网络存在电容”，非就近去耦
