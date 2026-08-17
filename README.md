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
| `netfind <工程> <网络名>` | 查网络全部引脚 |
| `find <工程> <位号>` | 位号反查 |
| `trace <工程> <位号> [--depth N] [--no-power]` | BFS 链路追踪 |
| `review <工程> [--no-erc] [--out-md ...] [--out-json ...]` | 设计审查报告 |
| `validate <工程>` | 结构冒烟测试 |
| `link-check <工程A> <工程B>` | 跨板连接器对候选核对（逐 pin 网络名比较） |
| `erc / export-netlist / export-bom` | 调用 kicad-cli |

## 测试与验收

- `tests/test_reader.py`：以 `examples/` 两个 KiCad 工程为夹具的单元测试
- `tests/validate_examples.py`：与 `kicad-cli` 官方网表逐引脚交叉验证

```bat
python -m unittest tests.test_reader -v
python tests\validate_examples.py
```

## 已知限制

- 网络命名已按 KiCad 官方约定生成：电源/全局名不带前缀，普通标签为
  `/Label`，分层标签为 `/Sheet Name/Label`；未命名网络为 `N$`。
- `kicad-cli` 不可用时审查仍可运行，仅缺少官方 ERC 结果。
- KiCad 文本变量（如 `${...}`）暂不展开。
- 本工具只读，不会修改任何工程文件。

更多细节见 `DEVELOPMENT.md`、`docs/kicad-tools-survey.md`、
`docs/lceda-sch-reader-design-review.md`。
