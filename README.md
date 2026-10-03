# kicad-sch-reader

纯 Python 的 KiCad 原理图（`.kicad_sch`）读取与设计审查工具。它参考了
[lceda-sch-reader](https://github.com/alwaysmy/lceda-sch-reader) 的设计优点
（只读、标准库、几何连通域、跨页网络归并、链路追踪、JSON 输出），并面向
KiCad 10 的 s-expression 格式重新实现，同时补充了审查规则与官方
`kicad-cli` ERC 集成。

## 功能

- 解析 KiCad 6..10 `.kicad_sch`（兼容新旧 lib pin 写法，实测 KiCad 10.0.2）
- 分层工程加载：根图 + 图纸符号递归展开，按 sheet path 组织
- 几何连通域网表：导线、连接点（junction）、标签、全局标签、分层标签、
  电源符号、引脚直接接触，全部基于精确坐标归并
- 同页同名标签、跨页全局标签/电源符号、父子图纸 sheet-pin 自动归并
- 查询命令：`parse`、`sheets`、`components`、`pins`、`nets`、`netfind`、
  `find`、`trace`
- 设计审查规则：重复位号、缺封装/缺值、悬空引脚、单引脚网络、网络名冲突、
  去耦电容检查、分层引脚完整性、DNP 清单
- 集成官方 `kicad-cli sch erc`，生成 Markdown/JSON 审查报告
- 共享 Circuit IR：KiCad/LCEDA 都归一为 `BoardIR`（components/nets/evidence），
  跨板检查只面向统一图结构（`kicad_sch_reader/circuit_ir.py`）
- 无第三方依赖（仅 Python 标准库）；KiCad CLI 仅用于 ERC/BOM/网表导出

## 快速开始

```bat
cd D:\MyProjects\AI\schematics_review_tool
set PYTHONIOENCODING=utf-8

rem 解析工程
python kicad-sch-reader.py parse examples\Lock-In-Amplifier_MainBoard_V0.1

rem 生成审查报告
python kicad-sch-reader.py review examples\Lock-In-Amplifier_MainBoard_V0.1 ^
  --out-md reports\Lock-In-Amplifier_MainBoard_V0.1.review.md ^
  --out-json reports\Lock-In-Amplifier_MainBoard_V0.1.review.json

rem 结构化数据
python kicad-sch-reader.py --json components examples\Lock-In-Amplifier_PowerBoard_V0.1
python kicad-sch-reader.py --json netfind examples\Lock-In-Amplifier_PowerBoard_V0.1 +15V
```

## 常用命令

| 命令 | 说明 |
| --- | --- |
| `parse <工程>` | 图纸/元件/网络统计 |
| `sheets <工程>` | 图纸树与 sheet-pin |
| `components <工程> [过滤]` | 元件、型号、封装 |
| `pins <工程> [位号]` | 引脚级网络表（含悬空/NC） |
| `nets <工程> [网络名]` | 项目网络清单 |
| `netfind <工程> <网络名> [--exact]` | 查网络全部引脚（N$ 网络建议 --exact） |
| `bridges <工程>` | 两脚中间器件桥接对（排阻 Rk.1↔Rk.2、0Ω 等） |
| `find <工程> <位号>` | 位号反查 |
| `trace <工程> <位号> [--depth N] [--no-power]` | BFS 链路追踪 |
| `review <工程> [--no-erc] [--out-md ...] [--out-json ...]` | 设计审查报告 |
| `validate <工程>` | 结构冒烟测试 |
| `link-check <工程A> <工程B>` | 跨板连接器对候选核对（逐 pin 网络名比较） |
| `erc / export-netlist / export-bom` | 调用 kicad-cli |

## 测试与验收

公共测试不依赖用户工程文件。可选的私有夹具可放在仓库外，通过
`KICAD_READER_EXAMPLES` 指向其父目录；不存在的夹具会明确跳过。

```sh
python -m unittest discover -v
# 可选原生回归，要求 KiCad 10；也可用 KICAD_CLI 指定可执行文件
KICAD_CLI=/path/to/kicad-cli python -m unittest tests.test_official_cli -v
# 任意真实工程的严格验收：检查全部物理引脚，以及网络分区的漏连/误短接
python tests/validate_examples.py /path/to/root.kicad_sch --work-dir /tmp/kicad-validation
```

验收不再使用网络名相似度或 95% 阈值：覆盖缺失、多余引脚、拆网或误并网
任一非零都会失败。未命名网络和层级同名网络也比较实际成员集合；NC/悬空
引脚作为独立分区参与完整引脚库存核对。网络命名差异不会掩盖拓扑错误。

## LCEDA `.epro` / CBB 审查（附带工具）

```bat
python scripts\lceda_epro_review.py ^
  examples\LIA_DigitalBoard_RevA\ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro ^
  --trace-net VCC_1V5 --trace-ref U6
```

会展开 CBB 复用模块：应用 `.eins` 位号覆盖、连接模块端口与子图网络，
输出 CBB 内部器件逐 pin 连接，并让 `--trace-net/--trace-ref` 直接穿透到
CBB 内部器件。普通电阻/电感等中间器件保留为 `component_bridges` hop，
只有 SHORT/0Ω 跳线做脚本化直连合并。

`lceda_reader.py` CLI 现在也直接接受 `.epro`（自动解包并打印日志）：

```bat
python repos\lceda-sch-reader\lceda_reader.py --eprj xxx.epro boards
```

KiCad + LCEDA 多工程跨板候选核对（统一走 Circuit IR）：

```bat
python scripts\multi_project_cross_check.py ^
  --kicad examples\Lock-In-Amplifier_MainBoard_V0.1 ^
  --kicad examples\Lock-In-Amplifier_PowerBoard_V0.1 ^
  --lceda examples\LIA_DigitalBoard_RevA\ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro
```

## 已知限制

- 网络命名已按 KiCad 官方约定生成：电源/全局名不带前缀，普通标签为
  `/Label`，分层标签为 `/Sheet Name/Label`；未命名网络为 `N$`。
- `kicad-cli` 不可用或执行失败时，可生成纯 Python 审查；JSON 的 `erc_status` 明确标记 `failed`，不会把缺失/陈旧报告当作零违规。`--no-erc` 标记为 `skipped`。
- KiCad 文本变量（如 `${...}`）暂不展开。
- 本工具只读，不会修改任何工程文件；ERC 默认报告写入临时目录。
- 缺少嵌入符号库、无效坐标、损坏语法、循环层级会报错；不会把未知引脚放到元件原点。
- 内部节点连线按 KiCad 10 原生实测：导线内部需要显式 junction 或标签锚点；没有 junction 的 T 端点/引脚不会自动短接到导线。KiCad 9 对未分段 junction 的导出行为不同，不能承诺所有旧版本导出完全等价。
- 总线/总线别名、继承库、文本变量、重复引脚 jumper 等高级格式语义仍需后续覆盖；本轮不是全部 KiCad 语义验收。跨页多单元器件若页码缺失或重复，严格验证会明确失败，避免猜测物理实例身份。

更多细节见 `DEVELOPMENT.md`、`docs/shared-circuit-ir.md`、
`docs/kicad-tools-survey.md`、`docs/lceda-sch-reader-design-review.md`。
