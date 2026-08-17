# examples 工程审查与工具验收记录

日期：2026-08-17。测试用例：

| 工程 | 格式 | 工具 |
| --- | --- | --- |
| `LIA_DigitalBoard_RevA` | 立创EDA（.epro） | 不在 kicad-sch-reader 范围内，见 lceda-sch-reader 仓库 |
| `Lock-In-Amplifier_MainBoard_V0.1` | KiCad 10 分层工程 | kicad-sch-reader |
| `Lock-In-Amplifier_PowerBoard_V0.1` | KiCad 10 单页工程 | kicad-sch-reader |

## 1. 工具正确性验收（与 kicad-cli 官方网表交叉验证）

`python tests/validate_examples.py` 结果：

| 工程 | 官方网表引脚 | 共同引脚 | 漏掉 | 多出 | 名称不一致 | precision |
| --- | --- | --- | --- | --- | --- | --- |
| MainBoard | 735 | 735 | 0 | 0 | 0 | 1.0 |
| PowerBoard | 313 | 313 | 0 | 0 | 0 | 1.0 |

说明：官方网表不含 `#PWR*` 电源符号，`unconnected-*` 为 NC 伪网络，
两者按规则剔除后逐 `(ref, pin)` 比对。结论：几何网表与官方结果**完全一致**。

`python -m unittest tests.test_reader -v`：10 项测试全部通过。

## 2. MainBoard 审查摘要

- 结构：根图 + 4 张子图；484 个符号实例；182 个网络；
  964 个引脚连接（含电源符号）。
- KiCad 官方 ERC：20 条 warning，主要是：
  - `power_pin_not_driven`：多处电源输入脚未被 Output Power 驱动
    （如 U201.4、U206.1、U303.2 等）
  - `lib_symbol_mismatch`：DRV8837、REF5050AD 符号与来源库不一致
- 本工具自有规则：
  - 27 条 DNP 提示（测试点/选焊器件），需人工确认 BOM 策略
  - 1 条去耦提示：U303.3 的电源网络 N$152 上未发现电容
- 结论：分层网络 ADC_CS、AFE_OUT_P 等已正确跨页归并，未发现漏网。

## 3. PowerBoard 审查摘要

- 结构：单页；234 个符号实例；52 个网络；424 个引脚连接（含电源符号）。
- KiCad 官方 ERC：11 条 error：
  - `power_pin_not_driven`：+#PWR0116、#PWR0126、U101.15、U102.6、
    U103.2、U104.1、U106.1、U107.2、U108.3 等电源输入无 Output Power 驱动
  - `pin_to_pin`：U104.1 与 U105.1 的 Output-Output 互连
- 本工具自有规则：10 条 DNP 提示（TP101-TP108 等测试点与选焊件）。
- 结论：`GND`（195 pin）、`VBUS`（20 pin）等电源网络归并正常；
  与官方 ERC 的错误集合一致，工具判定可信。

## 4. 测试用例对工具设计的反馈

1. **多单元器件**：MainBoard 的 MUX509/OPA690 暴露了“非本单元引脚”
   与“0_* 公共电源引脚”两种边界，已修正并固化为单元测试。
2. **纯导线层间连接**：`AFE_OUT_P` 等跨两张子图的信号通过父图 sheet-pin
   导线直连，没有元件引脚。早期过滤空域导致断链，已修复。
3. **同名局部标签**：根图连接器信号 `ADC_CS` 等由两段相同局部标签连接，
   验证了“同页同名标签必须归并”。
4. **引脚坐标变换**：合成最小旋转实验台（tests/fixtures/mini.kicad_sch）
   证明 KiCad 10 需要 y 取反 + 顺时针旋转 + 旋转后镜像，已被文档记录。

## 5. CBB 展开与 trace 验收

- `scripts/lceda_epro_review.py --trace-net VCC_1V5 --trace-ref U6` 可穿透
  CBB 端口：
  - `trace VCC_1V5` 显示 CBB1 内部 `U6.SW/VFB`、`L5`、`C37/C40/C41/C42`、
    `R33/R34`；
  - `trace VCC_1V0` 显示 CBB3 内部 `U7.LX1/FB1`、`L1`、`R17/R18`、`C18/C21`。
- `tests/test_lceda_epro.py` 固化 7 项 CBB 回归断言（模块数量、`.eins`
  位号覆盖、端口桥、内部器件 trace、无重复位号/无 CBB 悬空、pin type 告警）。

## 6. 审查报告位置

- `reports/Lock-In-Amplifier_MainBoard_V0.1.review.md` / `.json`
- `reports/Lock-In-Amplifier_PowerBoard_V0.1.review.md` / `.json`
- `reports/validation/validation.json`
- 官方 ERC JSON：`reports/erc_*.json`
- 官方网表：`reports/validation/*.net`
