# schematic-review 项目进度与交接文档

> 生成时间：2026-08-18
> 项目根目录：D:\MyProjects\AI\schematics_review_tool
> 远程：
> - github.com/alwaysmy/kicad-sch-reader（main=8d82e97，之后有未提交改动）
> - github.com/alwaysmy/lceda-sch-reader（public；分支 cbb-symboltype17-fix；PR #1）

---

## 1. 项目目标

做一个"多 EDA 格式的原理图审查工具"，当前同时覆盖：

1. KiCad `.kicad_sch` 工程：解析、审查、trace、跨板 link-check，优先兼容 `kicad-cli`。
2. LCEDA `.epro` 工程：CBB 复用模块展开、内部器件连接、穿透 trace。
3. 多工程跨板检查：KiCad 对 KiCad、KiCad 对 LCEDA。
4. 给 LLM 使用的 skill：指导手册（datasheet）查询和结果判定，避免猜测。

---

## 2. 已完成能力

### 2.1 KiCad 工具链

- 纯 Python `.kicad_sch` 解析（KiCad 6..10）
- 分层工程加载、几何连通域、电源/全局/分层标签归并
- 命令：`parse` / `sheets` / `components` / `pins` / `nets` / `netfind` / `find` / `trace` / `review` / `link-check` / `erc` / `export-netlist` / `export-bom`
- 与官方 `kicad-cli` 交叉验证：
  - MainBoard：`common=735/735, missing=0, mismatch=0, precision=1.0`
  - PowerBoard：`common=313/313, missing=0, mismatch=0, precision=1.0`
- KiCad 网络命名与 kicad-cli 对齐：电源/全局名不带前缀，普通标签 `/Label`，分层标签 `/Sheet Name/Label`，未命名 `N$n`

### 2.2 LCEDA `.epro` / CBB

关键文件：
- `scripts/lceda_epro_review.py`
- `reports/LIA_DigitalBoard_RevA.lceda-review.md`
- `reports/LIA_DigitalBoard_RevA.lceda-review.json`

已实现：
- `.epro`（ZIP）后端 `EproDB`
- `.eins` OVERRIDE 应用：CBB 内部模板位号 U1/L1/C1 变为母板位号 U6/L5/C37 等
- `symbolType=17` CBB 引脚参与 pinmap（lceda-sch-reader 中已修复，见 PR #1）
- CBB symbol 引脚坐标 `pin - HEAD.origin`
- CBB 端口按物理端点建桥；trace 使用母图网络 canonical
- CBB 内部展开明细：端口 -> 内部网络/器件；内部器件 -> 引脚 -> 展平网络
- `--trace-net` / `--trace-ref` 可穿透 CBB
- `--trace-skip-power` / `--power-net <regex>`
- report JSON 增加 `pin_net_map`，供多工程跨板脚本复用

LIA_DigitalBoard_RevA 当前结果：
- 4 个 CBB：CBB1 TPS563201、CBB3 EA3059、CBB2/CBB4 Type-C
- 典型内部连接：
  - CBB1 VOUT = VCC_1V5 -> U6.SW/VFB、L5、C37/C40/C41/C42、R33/R34
  - CBB3 VOUT1 = VCC_1V0 -> U7.LX1/FB1、L1、R17/R18 等
  - CBB4 D+ = USBC_D_PE -> USB1.D+
- 最后生成的 findings = 130：
  - 5 条 `CBB_PIN_TYPE_SUSPECT` 警告（VOUT、D+/D- 标成 IN 等）
  - 122 条单引脚网络 info（多数为测试点/连接器/调试口，需人工确认）
  - 2~3 条 `MULTI_UNIT_CONFIRMED` info
  - 0 error

### 2.3 多单元器件自动识别（回答"脚本还是 LLM"）

已把逻辑改为脚本自动识别，不依赖 LLM：

| 条件 | 输出 |
| --- | --- |
| 同页/跨页多次出现 + 相同 Unique ID + 不同 title 后缀 | `MULTI_UNIT_CONFIRMED` info |
| 相同 Unique ID + 相同 title | `POSSIBLE_REUSED_INSTANCE` warning |
| 无法判定 | `MULTI_UNIT_UNVERIFIED` info |
| 同页重复且不满足多单元 | `DUPLICATE_DESIGNATOR` error |

例：
- U1（XC7A35T 多 BANK 单元）-> 自动确认多单元
- U24（双片 DDR `.1/.2`）-> 自动确认多单元

原逻辑其实已经是脚本侧判断（Unique ID + title），只是输出笼统的"多单元或复用，需人工确认"；现在改为确定性分类。

### 2.4 多工程跨板检查

新增：
- `scripts/multi_project_cross_check.py`
- `reports/multi_project_cross_check.md`
- `reports/multi_project_cross_check.json`

能力：
- 输入多个 KiCad 工程 + LCEDA `.epro`
- 统一成 `BoardView { connectors: ref -> { pins: {pin: net} } }`
- 两种格式的连接器逐 pin 网络比较
- 输出 `confidence: detected | candidate`

当前结果：
- MainBoard `J102` 对 PowerBoard `J103`：exact=16/16，score=1.0，`detected`
- 其余大量低分候选，符合"同名网络只是候选证据"的原则

### 2.5 LLM skill 文档

新增：`skill/SKILL.md`。内容：
- 工具命令示例
- power 判断的证据层级：
  1. 结构证据（电源符号、`power_in/out` 引脚、`#PWR`）最强
  2. 命名正则（GND/VCC/VBUS/正负数字 V 等）
  3. 用户补充 `--power-net <regex>`
  4. 无法判定时不要跳过，列为候选
- 手册检查协议：Everything 搜本地手册 -> 读 PDF 拿 EN 阈值/输入范围/输出能力 -> 本地没有再上网（Kimi WebBridge / Edge）-> Finding 带 datasheet 证据和 confidence
- 跨板检查必须标注 `candidate / declared`
- CBB 展开汇报要求

### 2.6 trace 的 power 判断增强（回答"不一定规范"）

已修改 `kicad_sch_reader/cli.py`：

```python
def _is_power_net(net, extra_patterns=None):
    # 1) net.power_names（电源符号）
    # 2) 引脚类型 power_in / power_out
    # 3) ref 以 #PWR 开头
    # 4) 名字正则 GND|VCC|VBUS|正负数字 V...
    # 5) 用户 --power-net <regex>
```

`trace` 命令已加 `--power-net`。结论：不能只靠名字正则；必须结构证据优先，无法判定时不做静默跳过。

---

## 3. ChatGPT 架构意见摘要

来源：`https://chatgpt.com/c/6a8317b5-4034-83ea-af07-c7c6c620a05d`
原始抓取临时文件：`x4_webbridge.txt`（建议尽快转正式文档，勿清理）

核心意见：
1. 命名建议：`schematic-review` / `schematic-review-tool`
2. 按编译器架构分层：Parser -> Universal Circuit IR -> Graph -> Analysis -> Rules -> AI -> Finding
3. 必须有统一 IR，不能把 KiCad/LCEDA 文件格式模型当内部模型
4. Parser 不做审查；Analysis 与 Rules 分开
5. AI 只看 IR/JSON，不看原始 `.kicad_sch`
6. Finding 统一对象；证据来源区分 `direct / calculated / datasheet / inferred / ai`
7. Datasheet 知识层不要直接塞进 AI，先形成结构化事实
8. 多板项目单独 project 层，解决多文件/多板
9. 跨板连接区分 `declared / detected / inferred / unknown`
10. 当前 lceda-sch-reader 定位：LCEDA Parser/Adapter 很强，但缺 IR、电气语义、power/signal/interface graph

---

## 4. 当前主要问题（接手重点）

### 问题 1：MainBoard 对 DigitalBoard 没有匹配上

`multi_project_cross_check` 当前按相同 pin number 比较：
- MainBoard `J101`（`Conn_02x40_Odd_Even`，80 pin）
- DigitalBoard `CN7`（`X0802FVS-80AS-LPV01`，80 pin BTB）
- 共同 pin=60，exact=0，score=0.0

原因很可能是 pin 编号规则不同：
- KiCad `Conn_02x40_Odd_Even`：奇数/偶数编号
- BTB 连接器：顺序编号 1..80

下一步：
1. 增加 net-set overlap 指标（不看 pin number，比较网络名集合）
2. 增加 `--pin-map mapping.json`，支持用户声明映射
3. 自动尝试 odd/even 转 sequential 重排，但只能输出 `candidate`，不能自动 confirmed
4. 输出 BoardConnection 证据：`declared/detected/candidate/inferred/unknown`

### 问题 2：测试需要重跑

之前 17 个测试通过（KiCad 10 + CBB 7）。之后又改了 multi-unit、power、cross-check，需要重跑：

```bat
python -m unittest discover -s tests -v
python tests\validate_examples.py
```

另：本线程最后一次尝试给 `tests/test_lceda_epro.py` 增加"多单元自动识别"断言时失败，因为当前线程没有文件编辑工具 `str_replace_editor`。该测试补充还没写入，接手线程需要补：

```python
def test_multi_unit_parts_are_detected_automatically(self):
    confirmed = {
        f["ref"] for f in self.report["findings"]
        if f["code"] == "MULTI_UNIT_CONFIRMED"
    }
    self.assertIn("U1", confirmed)
    self.assertIn("U24", confirmed)
    self.assertNotIn(
        "MULTI_UNIT_UNVERIFIED",
        {f["code"] for f in self.report["findings"]},
    )
```

### 问题 3：ChatGPT 意见还没落成正式文档

建议接手后转成：
- `docs/chatgpt-architecture-opinions.md`
- `docs/universal-circuit-ir-roadmap.md`

### 问题 4：未提交变更

远程 main 当前是 `8d82e97`。之后本地新增/修改了：
- `scripts/lceda_epro_review.py`（multi-unit、pin_net_map、power）
- `scripts/multi_project_cross_check.py`（新增）
- `kicad_sch_reader/cli.py`（power 判断）
- `skill/SKILL.md`（新增）
- `reports/LIA_DigitalBoard_RevA.lceda-review.md/.json`
- `reports/multi_project_cross_check.md/.json`
- `.gitignore` / `scripts/cleanup_dev_temp.py`（可能）

接手先执行：

```powershell
cd D:\MyProjects\AI\schematics_review_tool
git status --short
git add -A
git commit -m "Add multi-project cross-check, power classification, datasheet skill"
git push origin main
```

注意：临时文件 `x4_webbridge.txt`、`_x*.py`、`_v*.py` 等不要提交；先把 ChatGPT 内容转正式文档，再清理。

---

## 5. 关键文件清单

| 文件 | 说明 |
| --- | --- |
| `scripts/lceda_epro_review.py` | LCEDA .epro / CBB 审查、展开明细、trace |
| `scripts/multi_project_cross_check.py` | 多工程 KiCad+LCEDA 跨板候选检查 |
| `kicad_sch_reader/cli.py` | KiCad 命令；power 判断增强 |
| `tests/test_lceda_epro.py` | CBB 回归测试（7 项，待补多单元断言） |
| `skill/SKILL.md` | LLM 使用规范、手册检查、power 判断 |
| `reports/LIA_DigitalBoard_RevA.lceda-review.md/.json` | LIA 数字板 CBB 审查报告 |
| `reports/multi_project_cross_check.md/.json` | 多工程跨板候选报告 |
| `docs/cross-board-link-check.md` | 现有跨板 link-check 说明 |
| `x4_webbridge.txt` | ChatGPT 架构意见原始抓取（临时，需转正式文档） |

关键命令：

```bat
python scripts\lceda_epro_review.py examples\LIA_DigitalBoard_RevA\ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro ^
  --out-md reports\LIA_DigitalBoard_RevA.lceda-review.md ^
  --out-json reports\LIA_DigitalBoard_RevA.lceda-review.json ^
  --trace-net VCC_1V5 --trace-ref U6 --trace-skip-power

python scripts\multi_project_cross_check.py ^
  --kicad examples\Lock-In-Amplifier_MainBoard_V0.1 ^
  --kicad examples\Lock-In-Amplifier_PowerBoard_V0.1 ^
  --lceda examples\LIA_DigitalBoard_RevA\ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro
```

---

## 6. 建议接手顺序

1. `git status` 盘点未提交变更。
2. 重跑 `unittest discover` 和 `validate_examples`。
3. 补 `test_multi_unit_parts_are_detected_automatically`。
4. 给 `multi_project_cross_check.py` 增加 net-set overlap、`--pin-map`、confidence 输出，重跑 MainBoard 对 DigitalBoard。
5. 把 `x4_webbridge.txt` 转成 `docs/chatgpt-architecture-opinions.md` 和 IR roadmap。
6. 更新 `README.md`、`DEVELOPMENT.md`、`CHANGELOG.md`、`docs/example-review-summary.md`。
7. 提交并推送 `main`。
8. 可选：把 datasheet/power 规范同步到 `lceda-sch-reader/skill/`，推到 PR #1。

---

## 7. 回答用户四个问题（结论）

1. U1/U24 是否脚本自动识别？
   原逻辑是脚本侧判断（Unique ID + title 后缀），但只输出"需人工确认"的模糊 info；现在改为脚本确定性分类 `MULTI_UNIT_CONFIRMED`，U1/U24 自动确认为多单元，不需要 LLM。

2. ChatGPT 意见与多工程跨板检查
   核心是统一 IR、Parser/Review 分层、Finding 统一、证据等级、多板 project、BoardConnection 不能自动确认。多工程跨板脚本已有第一版，MainBoard 对 PowerBoard 已 detected，MainBoard 对 DigitalBoard 因 pin 编号规则差异需要继续加 net-overlap / pin-map。

3. 手册检查应写进 skill
   已写入 `skill/SKILL.md`：指导 LLM 用 Everything 查本地手册、Kimi WebBridge 上网、读 datasheet 参数后自主判断，并要求 Finding 带 datasheet 证据和 confidence。

4. trace power 如何判断
   已改为"结构证据优先 + 命名正则 + 用户补充正则"的多级判断；不规范的电源网络用 `--power-net` 补充；无法判定时不做静默跳过，列为候选。

---

## 8. 工具环境说明

- Windows 环境，无 bash；日常通过 `.bat` + `kimi-cu launch_app` 执行 Python。
- 当前交接线程可用 `pwsh` 直接执行 PowerShell 命令；文件编辑可用 PowerShell（`Set-Content` / `Add-Content`）。
- 注意：PowerShell here-string 中不要使用弯引号（中文弯引号会导致命令解析失败），统一用直引号。
- Kimi WebBridge：
  - 本地 daemon：`http://127.0.0.1:10086`
  - 会话名示例：`schematic-review-research`
  - 用法：`navigate` -> `evaluate`（用 `[data-message-author-role]` 提取 ChatGPT 对话）
- kicad-cli：`C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`

---

## 9. 2026-09-19 复核更新（重要）

### 9.1 仓库状态已前进

- 当前 HEAD：`fc2ce2f`（不是本文档最初记录的 `8d82e97`）
- 之前那批改动并没有丢失，已经被后续提交整合：
  - `b9bc30c` Add multi-project cross-check, auto multi-unit classification, power-aware traces
    包含：`scripts/multi_project_cross_check.py`、自动多单元分类、power-aware trace、
    `skill/SKILL.md`、`reports/multi_project_cross_check.*`、CBB 报告更新
  - `639e902` Add shared Circuit IR and migrate multi-board cross-check
    包含：`kicad_sch_reader/circuit_ir.py`、`docs/shared-circuit-ir.md`，
    并把跨板检查迁移到共享 Circuit IR
- 因此"之前的改动"当前版本里都能找到。

### 9.2 当前未提交改动是叠加，不是覆盖

当前 `git status` 中与本项目相关的修改只有：
- `CHANGELOG.md`（新增 0.1.4 / 0.1.5 条目）
- `DEVELOPMENT.md`（规则表 R801/IFC901、R103/R304/R701 描述更新）
- `scripts/lceda_epro_review.py`（新增 IFC901 接口方向语义核对，+18 行，纯插入）

以上都是**新增内容**，没有删除或回退之前的 CBB、trace、多单元、power、多工程改动。
`git diff` 确认 `scripts/lceda_epro_review.py` 仅在 `comp_lookup` 构造后插入 IFC901
分析块，原有函数与数据结构保持不变。

### 9.3 复核验证结果

- `python -m unittest discover -s tests -v`：41 tests OK（含 CBB 展开、trace、
  KiCad 规则、IFC901 新测试等）
- `scripts/multi_project_cross_check.py` 重跑：
  - MainBoard `J102` 对 PowerBoard `J103`：`detected`，score=1.0，exact=16/16
  - 迁移到 Circuit IR 后，candidate / detected / evidence 语义仍保留
- 当前代码中仍能找到之前的标记：
  - `MULTI_UNIT_CONFIRMED`、`POSSIBLE_REUSED_INSTANCE`、`pin_net_map`、
    `trace_skip_power`、`power_net_patterns`（`scripts/lceda_epro_review.py`）
  - `_is_power_net(net, extra_patterns)`、`--power-net`（`kicad_sch_reader/cli.py`）
  - `skill/SKILL.md` 中 TPS563201 手册查询、power 证据层级、跨板 candidate 原则
- 仍未完成（与本文档第 4 节一致）：
  1. `tests/test_lceda_epro.py` 仍缺 `test_multi_unit_parts_are_detected_automatically`
     （功能已在脚本中，但没有这个专项断言；当前 41 个测试不覆盖该断言名）
  2. MainBoard J101 对 DigitalBoard CN7 的 net-overlap / `--pin-map` 仍未实现
  3. ChatGPT 架构意见仍未转成 `docs/chatgpt-architecture-opinions.md`
  4. `reports/LIA_DigitalBoard_RevA.lceda-review.*` 可能落后于当前代码
     （live review 测试通过，但仓库内报告文件是老一代产物，需要时重新生成）

### 9.4 提交注意事项（已修正）

不要直接 `git add -A`：当前工作区有大量其他线程/实验产生的 untracked 文件
（`_*.py`、`TEST_SCRIPTS/`、`dsh-*`、`EVERYTHING_IPC_RESEARCH.md`、
`reports/_*.json` 等）。提交本项目改动请按路径精确 add，例如：

```powershell
git add CHANGELOG.md DEVELOPMENT.md scripts/lceda_epro_review.py docs/HANDOFF.md
git commit -m "Add IFC901 interface direction semantics and LCEDA review integration"
```

如果需要把之前已整合的改动一并确认，可查看：

```powershell
git show --stat b9bc30c
git show --stat 639e902
git show --stat fc2ce2f
```
