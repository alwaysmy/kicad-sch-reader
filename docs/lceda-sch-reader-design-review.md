# lceda-sch-reader 设计评审与改进建议

评审对象：`https://github.com/alwaysmy/lceda-sch-reader`
（克隆时间 2026-08-17，main @ shallow clone；评审时已应仓库所有者要求
通过 `gh repo edit --visibility public` 改为公开仓库，GitHub API 已确认
`visibility=public`。）

## 1. 总体评价

这是一个**质量明显高于平均水平的逆向格式工具**。它不只是“把某个工程读出来”，
而是从官方格式规范出发，沉淀出了一套可复用的命令原语（list/components/
pinmap/netlist/trace/netfind/bom/...），并且把开发过程中的错误教训、连接器
语义边界、位号歧义等知识明确写进了 README 和 SKILL。对后续做 KiCad 读取工具
有很高的参考价值。

核心优点：

1. **通用而非专用**：不绑定任何工程路径、位号或网络名；工程路径通过
   `--eprj`/环境变量/目录自动搜索定位。
2. **只读与抗占用**：SQLite 使用 `file:...?mode=ro` URI，编辑器打开时也能读。
3. **连通域精确方案**：不是简单按“同名网络”猜连接，而是
   实例坐标 + PIN 相对坐标 + 旋转/镜像 → 引脚绝对坐标 → 精确匹配 WIRE 端点；
   并正确识别串阻/磁珠/0Ω/短接符等桥接器件。
4. **诚实标注推断**：网络名推断结果带 `net_inferred`，单向传播规则避免
   “上拉电阻把信号名污染到 GND”这类经典误报。
5. **双 uuid 命名空间处理**：Symbol uuid 与 Device uuid 分属 components/
   devices 两表，Device→Symbol 通过 attributes 表桥接；这个坑在文档和代码里
   都处理得清晰。
6. **多工程连接器边界表达**：明确“同名网络 ≠ 物理相连”，`link-check` 只给
   候选，`trace --link` 必须显式声明连接器对；这是 EDA 工具里少见的工程严谨性。
7. **文档即知识库**：README 记录 11 条逆向错误教训、历史修复记录和
   V2.2/V3 后端规划；SKILL.md 把 LLM 的使用方法写成了可执行清单。
8. **零依赖**：仅标准库，Python 3.8+ 可运行。

## 2. 发现的问题与风险

### 2.1 结构性

- **单文件 1648 行**（`lceda_reader.py`）。基础层/解析层/连通域/命令输出/
  argparse 全部混在一个文件里，后续加入 V3 后端会进一步膨胀。
- **没有自动化测试**。仓库中没有 tests/，README 里的“实测 U4/U3/U26/U27/U18/U2
  全部正确”是人工结论，无法防止回归；尤其坐标变换和单向传播规则非常容易
  在重构时悄悄变坏。
- **没有打包元数据**。无 `pyproject.toml`/`setup.py`/entry point，
  只能靠 `python lceda_reader.py ...` 调用；作为库导入不友好。
- **缓存无上限**。`_text_cache` 以 `(docType, title)` 和 `(docType, title, "recs")`
  为键永久缓存整页文本和记录，大工程会持有全部数据；也没有失效机制。
- **解析失败静默**。`sheet_records()`/`symbol_pins()` 对 `json.loads` 失败直接
  `continue`，格式升级或损坏时表现为“数据变少”而不是明确报错，排查成本高。
- **输入发现策略有限**：`find_eprj()` 只 glob `*.eprj2`，不检查文件头/魔数，
  多 `.eprj2` 并存时取 `hits[0]` 的顺序依赖文件系统。

### 2.2 正确性/健壮性

- **几何容差硬编码**。`norm_pt` 先 round(1) 再容差 2（单位 0.01 inch），
  对高密度板或坐标精度不同的工程存在粘连风险；README 没有把容差来源和上限
  写清。
- **性能 O(N×M)**。`resolve_nets_by_domain()` 中每个引脚对全部命名端点
  线性扫描（`for (px, py), nm in endp_net.items()`），大工程会明显变慢；
  应改用空间哈希/字典索引。
- **`parse_value()` 启发式脆弱**。用正则从描述字符串猜阻值/容值/耐压，
  对“格式 1/格式 2”的识别依赖 `;` 和 `:`，立创描述变化后会静默退化。
- **命令层耦合输出**。`out()/outj()` 直接打印，函数内部混用“构建数据”和
  “渲染文本”；没有独立模型层，第三方想拿结构化结果只能解析 stdout。
- **页名作为主键**。`sheet_text(title)` 以 `display_title` 查 documents，
  README 自己承认页名可重名；虽然命令会列出全部同名页，但底层 API 用 title
  取页时无法区分同名的不同页，调用方容易踩坑。
- **错误处理基本靠返回 None/空**。没有退出码语义，脚本难以判断“查询失败”
  和“结果为空”。

### 2.3 工程化

- 无 CI（GitHub Actions 跑单元测试/lint）。
- 无类型注解、无 docstring 规范（部分函数有长注释，但接口签名不清晰）。
- 中英文混排文档对英文贡献者有门槛。
- `archive_探查脚本/` 与正式代码没有隔离，历史脚本中的绝对路径若被误运行
  有误导风险。
- README 很长且信息密度高，适合“知识库”但不适合新用户 30 秒上手；
  可拆 quickstart/reference/development。

## 3. 改进建议（按优先级）

### P0：测试与回归护栏

- 建立 `tests/`，至少覆盖：decompress 链、symbol/device 双命名空间、
  坐标变换（0/90/180/270 + 镜像）、pinmap 已知网络、trace BFS 深度限制、
  link-check 候选。把 README 里 U4/U18 等人工实测固化为断言。
- 加 GitHub Actions：`python -m unittest` + 最小工程夹具。
- 用 schema/快照测试锁定 `--json` 结构，防止下游脚本被无意破坏。

### P1：架构拆分与库化

建议目标结构：

```
lceda_reader/
  backend/eprj2.py     # SQLite 后端
  backend/epro2.py     # V3 后端（现有规划）
  decode.py            # base64/gzip/NDJSON
  model.py             # Sheet/Symbol/Pin/Wire/Net 数据类
  connectivity.py      # 连通域/网络推断（纯函数）
  commands/*.py        # 每个命令一个模块
  cli.py
  report.py            # markdown/json 输出
```

- 把 `LcedaDB` 的数据访问与连通域算法分离，V3 后端即可复用（README 已规划，
  但当前单文件结构会阻碍这个规划）。
- `pyproject.toml` + console_scripts，支持 `pip install -e .` 和作为库导入。
- `--json` 直接输出模型序列化结果，渲染器只负责人类可读文本。

### P1：正确性加固

- 坐标索引：对 wire 端点/命名端点建立量化坐标字典，把 O(N×M) 降到 O(N)。
- 页唯一键：用 `documents.uuid` 作为内部主键，`display_title` 只作为显示名；
  命令输出始终带 uuid。
- 解析失败计数：返回 `(records, warnings)` 或至少把失败行写入 debug 日志；
  `--strict` 模式遇坏行报错。
- 把几何容差参数化，并在 README 记录推导依据。
- 给命令定义退出码（0 成功、2 找不到工程、3 页不存在等）。

### P2：格式与生态

- 实现 README 中规划的 V3 后端抽象；先做 list/components，pinmap 复用。
- 提供“审查规则层”：当前工具是**读取原语**，审查靠 LLM 或一次性脚本
  （如 scripts/gen_audit.py）。建议增加可组合的 rule API：
  `check_single_pin_nets()`、`check_floating_pins()`、`check_power_decoupling()`
  等，把 SKILL.md 中的审查方法变成可回归的代码。
- 输出坐标供图形化审查定位（如 Kiri 式 diff/高亮）。
- 增加导出官方网表（BOM/netlist）的命令，形成“读取 + 审查 + 交付”闭环。

## 4. 对 kicad-sch-reader 的借鉴清单

本项目在实现 KiCad 版读取器时，直接沿用了以下设计：

1. 仅标准库、只读、通用工程发现；
2. 命令原语命名与形态（parse/components/pins/nets/netlist/netfind/find/trace）；
3. 连通域精确方案（量化坐标 + DSU + 几何点匹配）；
4. 电源/地网络识别与 `trace --no-power --depth`；
5. 多图纸/多工程边界必须显式声明（sheet-pin 层级归并）；
6. 全部命令支持 `--json`，供脚本/agent 消费；
7. 文档中记录格式坑与历史教训（见 `DEVELOPMENT.md` 第 3 节）。

同时针对 lceda 版的结构问题做了反向规避：拆包分层、加入 unittest 与
`kicad-cli` 官方网表交叉验证、把解析失败/坐标容差等写成可测试的显式实现。

## 5. 结论

`lceda-sch-reader` 的设计在“逆向格式工具”这一品类中属于优秀水平，
最值得保留的是**精确连通域思想**和**对工具边界的诚实表达**。主要短板在
工程化：无测试、单文件、无打包、输出层耦合。建议作者优先补测试与模块拆分，
再实现 V3 后端；审查规则层可作为后续增量，不阻塞核心价值。
