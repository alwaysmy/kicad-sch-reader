# kicad-sch-reader 开发文档

## 1. 目标与范围

本工具的目标与 `lceda-sch-reader` 一致：成为一个**通用、只读、可脚本化**
的原理图读取工具，而不是绑定某个工程的一次性脚本。v0.1 范围：

- KiCad 6..10 `.kicad_sch` s-expression 解析（实测 KiCad 10.0.2）
- 平铺/分层工程加载
- 几何连通域网表
- 审查规则与 Markdown/JSON 报告
- `kicad-cli` ERC/netlist/BOM 桥接

不做的部分（记录于 README）：文本变量展开、总线成员解析、图形渲染。

## 2. 目录结构

```
kicad_sch_reader/
  sexpr.py           S-expression 词法/语法
  model.py           数据模型（dataclasses）
  parser.py          .kicad_sch 解析与工程加载
  connectivity.py    几何连通域 + 网表归并
  circuit_ir.py      共享 Circuit IR（KiCad/LCEDA 统一分析层）
  rules.py           审查规则引擎
  kicad_cli.py       kicad-cli 桥接
  report.py          Markdown/JSON 报告
  cli.py             argparse CLI
kicad-sch-reader.py  入口脚本
tests/               单元测试与官方网表交叉验证
docs/                调研/评审文档
examples/            测试夹具（用户工程，只读）
reports/             自动生成的报告
```

## 3. 关键设计决策

### 3.1 只依赖标准库

与 `lceda-sch-reader` 相同，解析和审查零第三方依赖。理由：EDA 工具常运行在
受限环境，少一个依赖就少一类部署问题。`kicad-cli` 仅在需要官方 ERC/网表/
BOM 时按需调用，找不到时优雅降级。

### 3.2 S-expression 解析（sexpr.py）

KiCad 文件是 s-expression。实现要点：

- 引号字符串在词法阶段解码，调用方永远拿到去引号的原子；
- 节点统一为 `[head, *args]`，不引入重量级对象树；
- 提供 `children/first/find_all/xy/pair_xy/prop` 等窄接口。

### 3.3 坐标与引脚变换（重要，经过实验验证）

KiCad 10 的 lib pin 写法是
`(pin passive line (at x y rot) ... (number "N" ...))`；KiCad 6..9 的旧写法是
`(pin "N" (name ...) (type passive) (at ...))`。`_parse_lib_pin()` 同时兼容两种。

两个通过**最小旋转实验台 + kicad-cli 官方网表**确认的关键事实：

1. **lib pin `at` 的 y 坐标取反后才是电气连接点偏移**。
   例如 `Device:C_Small` 中 `number "1"` 的 pin 写在 `(at 0 2.54 270)`，
   但 KiCad 连接性实际把 1 脚放在 `(0, -2.54)`。
2. **实例变换顺序为：先顺时针旋转，后按镜像轴翻转**：
   - 旋转 90：`(x, y) -> (y, -x)`；180：`(-x, -y)`；270：`(-y, x)`；
   - `(mirror x)` 再对 **Y 坐标**取反（关于水平轴镜像）；
   - `(mirror y)` 再对 **X 坐标**取反（关于垂直轴镜像）。

实验记录见 `tests/fixtures/mini.kicad_sch` 与
`tests/test_reader.py::TestRotationLab`。这些事实绝不能凭直觉修改，
修改后必须重新跑 `tests/validate_examples.py` 与官方网表比对。

### 3.4 连通域算法（connectivity.py）

借鉴 `lceda-sch-reader` 的“连通域精确方案”，但按 KiCad 格式重新表达：

1. 坐标量化为 0.001 mm 网格（`qpoint`），消除浮点尾差；
2. DSU 建立导线端点、junction、标签、NC 点的物理域；
3. 每个引脚坐标注册为节点，但只有满足以下条件之一才报告为已连接：
   - 该点存在导线/junction/标签/NC 几何；或
   - 该点上有 ≥2 个引脚（引脚直接接触，如电容脚直接顶在电源符号上）。
4. 同页同名普通标签/分层标签按名称归并（KiCad 局部标签语义）；
5. 父子图纸：父图 sheet-pin 坐标域与子图同名 hierarchical label 域合并；
6. 全局标签与电源符号 Value 跨全部图纸按名合并；
7. 命名优先级：电源名 > 全局标签 > 分层标签 > 普通标签 > `N$编号`；
   多个不同全局名落在同一物理域时打 `has_conflict` 标记。
   命名尽量对齐 `kicad-cli`：`/Label`、`/Sheet Name/Label`、电源/全局名
   不带前缀。

**容易踩的坑**：父图上两个 sheet-pin 之间的纯导线域没有元件引脚，
早期实现把这类“空域”过滤掉，导致 `AFE_OUT_P` 等跨两张子图的网络无法合并。
现在的实现保留全部中间域，仅在最终物化时丢弃从未获得引脚或名字的分组。

### 3.5 多单元器件

KiCad 把同一多单元器件的每个 unit 存为独立 `symbol` 节点（同 Reference，
不同 `unit`）。位号重复检查必须按 `(sheet_path, ref, unit)` 判重，否则会把
合法多单元器件误报为重复位号。

## 4. 审查规则（rules.py）

规则刻意保持“可解释、低误报”：

| 代码 | 级别 | 含义 |
| --- | --- | --- |
| R101/R102 | error/warning | 同页/跨页重复位号 |
| R201/R202 | warning/info | 缺封装 / 值为空 |
| R301 | error/warning/info | 引脚未连接且未标 NC（按 pin type 分级） |
| R302/R303 | warning | 单引脚网络 / 无引脚标签 |
| R401 | error | 同一物理域存在多个全局网络名 |
| R501 | info | 电源输入引脚网络上未发现去耦电容 |
| R601/R602 | error/warning | 图纸文件缺失 / sheet-pin 无对应子图标签 |
| R701 | info | DNP 器件清单 |
| ERC-* | 随官方 | kicad-cli ERC JSON 转写 |

官方 ERC 与本工具规则分开输出（代码前缀不同），便于追溯证据来源。

## 5. 验证方法

1. `python -m unittest tests.test_reader -v`：结构不变量 + 旋转实验台。
2. `python tests/validate_examples.py`：
   - 用 `kicad-cli sch export netlist` 生成官方网表；
   - 逐引脚比对 `(ref, pin) -> net`；
   - 忽略 `#PWR*`（官方网表不含电源符号）与 `unconnected-*` 伪网络；
   - 网络名比较时忽略 `/Sheet/Label` 前缀；
   - 验收阈值：missing pins = 0，名称匹配 precision ≥ 0.95。
3. `review` 命令生成报告后人工抽查关键网络（如 `GND`、`AFE_OUT_P`）。

## 6. 如何新增审查规则

1. 在 `rules.py` 中实现 `check_xxx(project, netlist) -> list[Issue]`；
2. 注册进 `run_all_checks`；
3. 在 `tests/test_reader.py` 增加一个能稳定复现的断言；
4. 对 `examples/` 两个工程重跑 `review`，确认误报在可接受范围。

## 6.5 LCEDA `.epro` CBB 展开与 trace

`scripts/lceda_epro_review.py` 复用 lceda-sch-reader 的解析/连通域函数，
但补上了 CBB 所需的四件事：

1. `.eins` 覆盖应用：CBB 子图内部仍是 U1/L1/C1 等模板位号，必须按
   `INSTANCE/<base64>.eins` 的 OVERRIDE 表映射到母板位号/器件/封装。
2. `symbolType=17` 引脚参与 pinmap（原 lceda_reader 只放行 22）。
3. `.esym` 引脚坐标减去 HEAD origin（TPS563201 CBB 的 origin 不为 0）。
4. 端口桥接以**物理端点**而不是端口 Name 建桥；端口 trace 的目标用
   “母图网络”而不是子图网络，否则 SHORT 短路桥会把 VCC_1V5/
   VCC_1V35_DDR 合并后找不到内部器件。

回归测试：`python -m unittest tests.test_lceda_epro -v`。

## 6.6 共享 Circuit IR（采纳 ChatGPT 架构评审）

`kicad_sch_reader/circuit_ir.py` 是 KiCad 与 LCEDA 的统一分析层，设计要点：

- 解析器保持格式专属；分析/跨板检查只面向 `BoardIR`；
- `BoardIR` 图 = components + nets，多 unit 按位号折叠、引脚保留来源 sheet；
- `IRNet.kind ∈ signal|power|ground|interface`，结构证据优先、命名正则兜底；
- `IRFinding` / `IREvidence` 是所有发现的通用对象，证据等级为
  `direct|calculated|datasheet|declared|inferred|ai`；
- 跨板连接只输出 `candidate|detected`，`declared/confirmed` 必须由用户或
  项目 metadata 显式声明；
- 适配器：`board_from_kicad(project)` / `board_from_lceda(report)`；
- `scripts/multi_project_cross_check.py` 已全部改走 IR。

详细设计见 `docs/shared-circuit-ir.md`，回归测试见
`tests/test_circuit_ir.py`。

## 7. 跨板连接器核对

`link-check` 命令（与 lceda-sch-reader 同语义）对两个工程中的连接器逐 pin
比较网络名：

```bat
python kicad-sch-reader.py link-check ^
  examples\Lock-In-Amplifier_MainBoard_V0.1 ^
  examples\Lock-In-Amplifier_PowerBoard_V0.1
```

实测 MainBoard `J102` ↔ PowerBoard `J103` 16/16 全一致，因此能识别出
两板通过连接器相连；但同名网络仍然只是**候选证据**，物理对插关系与
连接器型号需人工确认（与 lceda-sch-reader 的边界说明一致）。

KiCad 与 LCEDA 混合检查使用共享 IR：

```bat
python scripts\multi_project_cross_check.py ^
  --kicad examples\Lock-In-Amplifier_MainBoard_V0.1 ^
  --kicad examples\Lock-In-Amplifier_PowerBoard_V0.1 ^
  --lceda examples\LIA_DigitalBoard_RevA\ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro
```

## 8. 路线图

- [ ] KiCad 文本变量展开与总线成员解析
- [ ] 去耦检查升级为“距电源引脚就近去耦”（当前为同网络存在性检查）
- [ ] PDF 位置映射：把 Issue 反查回图纸坐标，供图形化审查工具高亮
- [ ] 包发布到 PyPI 与 GitHub Actions CI
- [ ] 与 `lceda-sch-reader` 共用审查报告 schema，形成跨 EDA 统一审查层
