# KiCad 原理图审查报告 — examples.review

> 由 kicad-sch-reader 自动生成，根原理图：`D:\MyProjects\AI\schematics_review_tool\examples\Lock-In-Amplifier_PowerBoard_V0.1`

## 1. 工程概览

| 项目 | 值 |
| --- | --- |
| 图纸页数 | 1 |
| 元件符号数 | 234 |
| 网络数 | 52（命名网络 10） |
| 已解析引脚连接数 | 424 |
| 发现问题总数 | 6 |
| 问题分级 | error=0 / warning=1 / info=5 |

### 图纸清单（页码按 KiCad 导出顺序 = PDF 页序）

| PDF页 | 路径 | 文件 | 标题 | 元件 | 导线 | 标签 | 连接点 | NC | 版本/生成器 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `/` | `Lock-In-Amplifier_PowerBoard_V0.1.kicad_sch` |  | 234 | 316 | 3 | 85 | 3 | 20260306 / eeschema 10.0 |

### 元件清单（位号 / Value / 封装 / 页码）

共 123 个实体元件；其中无源件 96、测试点 8。电源符号 (#PWR) 不列在表内，JSON `components` 中保留全部。

| PDF页 | 位号 | Value/型号 | 库 | 封装 | 图纸 | 类型 | DNP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C101 | 50V 22uF | Device:C_Small | Capacitor_SMD:C_1206_3216Metric | `/` | passive |  |
| 1 | C102 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C103 | 47nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C104 | 47nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C105 | 1uF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C106 | 47nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C107 | 22uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C108 | 470nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C109 | 22uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C110 | 50V 22uF | Device:C_Small | Capacitor_SMD:C_1206_3216Metric | `/` | passive |  |
| 1 | C111 | 50V 47uF | Device:C_Polarized_Small | Capacitor_SMD:CP_Elec_6.3x7.7 | `/` | passive |  |
| 1 | C112 | 50V 47uF | Device:C_Polarized_Small | Capacitor_SMD:CP_Elec_6.3x7.7 | `/` | passive |  |
| 1 | C113 | 47nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive | yes |
| 1 | C114 | 1uF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C115 | 22uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C116 | 50V 47uF | Device:C_Polarized_Small | Capacitor_SMD:CP_Elec_6.3x7.7 | `/` | passive |  |
| 1 | C117 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C118 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C119 | 22uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C120 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C121 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C122 | 50V 22uF | Device:C_Small | Capacitor_SMD:C_1206_3216Metric | `/` | passive |  |
| 1 | C123 | 22uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C124 | 50V 22uF | Device:C_Small | Capacitor_SMD:C_1206_3216Metric | `/` | passive |  |
| 1 | C125 | 22uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C126 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C127 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C128 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C129 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C130 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C131 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C132 | 1nF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/` | passive |  |
| 1 | C133 | 100nF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/` | passive |  |
| 1 | C134 | 6.8pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/` | passive |  |
| 1 | C135 | 10nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C136 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C137 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C138 | 10nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/` | passive |  |
| 1 | C139 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C140 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C141 | 50V 22uF | Device:C_Small | Capacitor_SMD:C_1206_3216Metric | `/` | passive |  |
| 1 | C142 | 50V 22uF | Device:C_Small | Capacitor_SMD:C_1206_3216Metric | `/` | passive |  |
| 1 | C143 | 50V 22uF | Device:C_Small | Capacitor_SMD:C_1206_3216Metric | `/` | passive |  |
| 1 | C144 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C145 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C146 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C147 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C148 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C149 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C150 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | C151 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/` | passive |  |
| 1 | D101 | SMAJ36A | Diode:SMAJ36A | Diode_SMD:D_SMA | `/` | passive |  |
| 1 | D102 | DFLS240L-7 | Device:D_Schottky | Diode_SMD:D_PowerDI-123 | `/` | passive |  |
| 1 | D103 | DFLS240L-7 | Device:D_Schottky | Diode_SMD:D_PowerDI-123 | `/` | passive |  |
| 1 | D104 | SS54 | Device:D_Schottky | Diode_SMD:D_SMA | `/` | passive |  |
| 1 | D105 | GREEN 0603 | Device:LED | LED_SMD:LED_0603_1608Metric | `/` | passive |  |
| 1 | D106 | GREEN 0603 | Device:LED | LED_SMD:LED_0603_1608Metric | `/` | passive |  |
| 1 | F101 | 2920L150/60GR | Device:Fuse | Fuse:Fuse_2920_7451Metric | `/` | active |  |
| 1 | FB101 | BLM21PG121SN1D | Device:FerriteBead_Small | Inductor_SMD:L_0805_2012Metric | `/` | passive |  |
| 1 | FB102 | BLM21PG121SN1D | Device:FerriteBead_Small | Inductor_SMD:L_0805_2012Metric | `/` | passive |  |
| 1 | FB103 | BLM21PG121SN1D | Device:FerriteBead_Small | Inductor_SMD:L_0805_2012Metric | `/` | passive |  |
| 1 | FB104 | BLM21PG121SN1D | Device:FerriteBead_Small | Inductor_SMD:L_0805_2012Metric | `/` | passive |  |
| 1 | FID101 | MKR | Mechanical:Fiducial | Emoe_Mechanical:Mark_D1.0mm | `/` | active |  |
| 1 | FID102 | MKR | Mechanical:Fiducial | Emoe_Mechanical:Mark_D1.0mm | `/` | active |  |
| 1 | FID103 | MKR | Mechanical:Fiducial | Emoe_Mechanical:Mark_D1.0mm | `/` | active |  |
| 1 | H101 | M2 | Mechanical:MountingHole | MountingHole:MountingHole_2.2mm_M2_DIN965 | `/` | active |  |
| 1 | H102 | M2 | Mechanical:MountingHole | MountingHole:MountingHole_2.2mm_M2_DIN965 | `/` | active |  |
| 1 | H103 | M2 | Mechanical:MountingHole | MountingHole:MountingHole_2.2mm_M2_DIN965 | `/` | active |  |
| 1 | H104 | M2_VIA | Mechanical:MountingHole_Pad | MountingHole:MountingHole_2.2mm_M2_Pad_Via | `/` | active |  |
| 1 | J101 | KF2EDGR-4P 2.5mm | Connector_Generic:Conn_01x04 | Emoe_Connector:KF2EDGR-2.5-4P | `/` | connector |  |
| 1 | J102 | DC007B-2.0 | Connector:Barrel_Jack | Emoe_Connector:DC007B-2.5 | `/` | connector |  |
| 1 | J103 | 2.54mm 2x16P Header | Connector_Generic:Conn_01x16 | Connector_PinHeader_2.54mm:PinHeader_1x16_P2.54mm_Vertical | `/` | connector |  |
| 1 | L101 | FXL0630-330-M | Device:L | Inductor_SMD:L_Changjiang_FXL0630 | `/` | passive |  |
| 1 | L102 | FTC252012S3R3MBCA | Device:L_Small | Inductor_SMD:L_Changjiang_FNR252010S | `/` | passive |  |
| 1 | L103 | FTC303020D2R2MBCA | Device:L_Small | Inductor_SMD:L_Cenker_CKCS3015 | `/` | passive |  |
| 1 | L104 | FTC252012S6R8MBCA | Device:L_Small | Inductor_SMD:L_Changjiang_FNR252010S | `/` | passive |  |
| 1 | L105 | FXL0530-220-M | Device:L_Small | Inductor_SMD:L_Changjiang_FXL0530 | `/` | passive |  |
| 1 | L106 | FXL0530-220-M | Device:L_Small | Inductor_SMD:L_Changjiang_FXL0530 | `/` | passive |  |
| 1 | L107 | FXL0630-100-M | Device:L | Inductor_SMD:L_Changjiang_FXL0630 | `/` | passive |  |
| 1 | R101 | 0R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R102 | 102k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive | yes |
| 1 | R103 | 51k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R104 | 7.5k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R105 | 11k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R106 | 10k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R107 | 5.1k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R108 | 11k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R109 | 102k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R110 | 120k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R111 | 2M | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R112 | 102k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R113 | 3.3k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R114 | 2M | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R115 | 18k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R116 | 300k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R117 | 36k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R118 | 51k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R119 | 51k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R120 | 40.2k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R121 | 5.1k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R122 | 102k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R123 | 11k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R124 | 102k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R125 | 10k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R126 | 54.9k 0.1% | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/` | passive |  |
| 1 | R127 | 5.1k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | R128 | 51k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/` | passive |  |
| 1 | TP101 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/` | testpoint | yes |
| 1 | TP102 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/` | testpoint | yes |
| 1 | TP103 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/` | testpoint | yes |
| 1 | TP104 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/` | testpoint | yes |
| 1 | TP105 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/` | testpoint | yes |
| 1 | TP106 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/` | testpoint | yes |
| 1 | TP107 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/` | testpoint | yes |
| 1 | TP108 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/` | testpoint | yes |
| 1 | U101 | ADP5071ACPZ | Emoe_DCDC:ADP5071ACPZ | Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm | `/` | active |  |
| 1 | U102 | TPS62913 | Regulator_Switching:TPS62913 | Package_DFN_QFN:Texas_RPU0010A_VQFN-HR-10_2x2mm_P0.5mm | `/` | active |  |
| 1 | U103 | TPS54360DDA | Regulator_Switching:TPS54360DDA | Package_SO:TI_SO-PowerPAD-8_ThermalVias | `/` | active |  |
| 1 | U104 | TPS7A4701RGWR | Emoe_LDOs:TPS7A4701 | Package_DFN_QFN:QFN-20-1EP_5x5mm_P0.65mm_EP3.35x3.35mm | `/` | active |  |
| 1 | U105 | TPS7A3301RGWR | Emoe_LDOs:TPS7A3301 | Package_DFN_QFN:QFN-20-1EP_5x5mm_P0.65mm_EP3.35x3.35mm | `/` | active |  |
| 1 | U106 | GM1200ACPZ | Emoe_LDOs:GM1200ACPZ | Package_DFN_QFN:DFN-10-1EP_3x3mm_P0.5mm_EP1.65x2.38mm | `/` | active |  |
| 1 | U107 | L79L05_SOT89 | Regulator_Linear:L79L05_SOT89 | Package_TO_SOT_SMD:SOT-89-3 | `/` | active |  |
| 1 | U108 | L78L33_SOT89 | Regulator_Linear:L78L33_SOT89 | Package_TO_SOT_SMD:SOT-89-3 | `/` | active |  |

## 2. 网络清单（按名称）

> 说明：同一网络的层次/全局端口别名并入同一行（例如 ADC_VREFIN 可能并入 /5V_VREF）；JSON `nets[].hierarchical_names/aliases` 保留全部别名。

| 网络 | 类型 | 别名/层次端口 | PDF页 | 引脚数 | 所在图纸 | 引脚示例 |
| --- | --- | --- | --- | --- | --- | --- |
| +12VA | power |  | 1 | 16 | / | #PWR0184.1, J103.1, R120.1, C139.1, #PWR0168.1, C136.1, … |
| +3.3V | power |  | 1 | 6 | / | #PWR0192.1, J103.9, #PWR0203.1, FB104.1, R109.2, #PWR0126.1 |
| +5VA | power |  | 1 | 8 | / | U106.9, U106.10, C149.2, #PWR0200.1, C151.2, TP105.1, … |
| +5VP | power |  | 1 | 14 | / | TP106.1, #PWR0146.1, C123.2, C125.2, R115.1, FB102.2, … |
| -12VA | power |  | 1 | 15 | / | C137.1, R122.1, U105.1, U105.20, C138.2, C140.1, … |
| -5VA | power |  | 1 | 5 | / | #PWR0198.1, C147.1, U107.3, J103.7, #PWR0190.1 |
| /BUCK_COMP | local | BUCK_COMP | 1 | 3 | / | C134.1, R119.2, U103.6 |
| /VREG1B | local | VREG1B | 1 | 3 | / | U101.4, U101.14, C105.1 |
| GND | power |  | 1 | 195 | / | #PWR0194.1, J103.11, J103.12, J103.13, #PWR0129.1, L104.1, … |
| N$11 | unnamed |  | 1 | 3 | / | U101.5, R110.2, R111.1 |
| N$12 | unnamed |  | 1 | 3 | / | U101.11, R114.1, R112.1 |
| N$13 | unnamed |  | 1 | 2 | / | U101.1, L102.1 |
| N$14 | unnamed |  | 1 | 3 | / | U101.18, D103.1, L104.2 |
| N$15 | unnamed |  | 1 | 2 | / | U101.6, R107.2 |
| N$16 | unnamed |  | 1 | 3 | / | U101.12, C114.1, R112.2 |
| N$18 | unnamed |  | 1 | 2 | / | U101.10, R108.2 |
| N$19 | unnamed |  | 1 | 4 | / | R120.2, R121.1, U104.3, C135.1 |
| N$20 | unnamed |  | 1 | 5 | / | R102.2, U101.7, U101.9, R103.1, R101.1 |
| N$21 | unnamed |  | 1 | 2 | / | U102.10, R104.1 |
| N$22 | unnamed |  | 1 | 2 | / | U102.8, C108.2 |
| N$23 | unnamed |  | 1 | 6 | / | D103.2, L106.1, R114.2, TP102.1, C121.2, C118.2 |
| N$24 | unnamed |  | 1 | 2 | / | L103.1, U102.2 |
| N$25 | unnamed |  | 1 | 4 | / | D104.1, L107.1, C133.2, U103.8 |
| N$26 | unnamed |  | 1 | 2 | / | U104.14, C130.2 |
| N$27 | unnamed |  | 1 | 2 | / | U105.14, C131.2 |
| N$28 | unnamed |  | 1 | 2 | / | C106.2, R108.1 |
| N$29 | unnamed |  | 1 | 6 | / | L106.2, C129.2, U105.13, U105.15, U105.16, C127.2 |
| N$31 | unnamed |  | 1 | 6 | / | R106.2, C109.2, U102.6, C107.2, C103.2, FB101.2 |
| N$32 | unnamed |  | 1 | 2 | / | R106.1, U102.1 |
| N$33 | unnamed |  | 1 | 3 | / | U106.7, R126.1, C145.2 |
| N$35 | unnamed |  | 1 | 2 | / | R107.1, C104.2 |
| N$36 | unnamed |  | 1 | 3 | / | U108.3, FB103.2, C148.2 |
| N$37 | unnamed |  | 1 | 3 | / | U108.1, C150.2, FB104.2 |
| N$38 | unnamed |  | 1 | 4 | / | C113.1, R109.1, R101.2, U102.5 |
| N$39 | unnamed |  | 1 | 3 | / | R113.2, U102.9, R115.2 |
| N$40 | unnamed |  | 1 | 5 | / | C115.2, L103.2, U102.3, C119.2, FB102.1 |
| N$41 | unnamed |  | 1 | 3 | / | R116.2, R117.1, U103.3 |
| N$42 | unnamed |  | 1 | 6 | / | C117.2, C120.2, D102.1, L105.1, R111.2, TP101.1 |
| N$43 | unnamed |  | 1 | 2 | / | R118.1, U103.4 |
| N$44 | unnamed |  | 1 | 4 | / | R122.2, R123.1, U105.3, C138.1 |
| N$45 | unnamed |  | 1 | 2 | / | C132.2, R119.1 |
| N$46 | unnamed |  | 1 | 3 | / | R124.2, R125.1, U103.5 |
| N$47 | unnamed |  | 1 | 2 | / | R127.2, D105.2 |
| N$48 | unnamed |  | 1 | 6 | / | C128.2, U104.13, U104.15, U104.16, L105.2, C126.2 |
| N$49 | unnamed |  | 1 | 2 | / | R128.2, D106.1 |
| N$5 | unnamed |  | 1 | 4 | / | F101.1, J101.1, J101.2, J102.1 |
| N$50 | unnamed |  | 1 | 2 | / | C133.1, U103.1 |
| N$6 | unnamed |  | 1 | 7 | / | L101.2, C124.1, C112.1, R116.1, C122.1, C116.1, … |
| N$7 | unnamed |  | 1 | 5 | / | L101.1, C110.1, F101.2, C111.1, D101.1 |
| N$8 | unnamed |  | 1 | 2 | / | U101.2, R105.2 |
| N$9 | unnamed |  | 1 | 3 | / | U101.20, D102.2, L102.2 |
| VBUS | power |  | 1 | 20 | / | U101.15, U101.16, U101.17, #PWR0109.1, C143.1, L107.2, … |

### 网络连接明细（全量，供逐条核对）

| 网络 | PDF页 | 类型 | 连接点（ref.pin） |
| --- | --- | --- | --- |
| +12VA | 1 | power | #PWR0184.1, J103.1, R120.1, C139.1, #PWR0168.1, C136.1, U104.1, U104.20, TP104.1, C135.2, U106.1, U106.2, U106.3, U106.6, #PWR0174.1, C144.2 |
| +3.3V | 1 | power | #PWR0192.1, J103.9, #PWR0203.1, FB104.1, R109.2, #PWR0126.1 |
| +5VA | 1 | power | U106.9, U106.10, C149.2, #PWR0200.1, C151.2, TP105.1, #PWR0188.1, J103.5 |
| +5VP | 1 | power | TP106.1, #PWR0146.1, C123.2, C125.2, R115.1, FB102.2, J103.14, J103.15, J103.16, #PWR0195.1, R127.1, #PWR0207.1, #PWR0116.1, R105.1 |
| -12VA | 1 | power | C137.1, R122.1, U105.1, U105.20, C138.2, C140.1, #PWR0167.1, TP103.1, #PWR0186.1, J103.3, C146.1, #PWR0178.1, U107.2, R128.1, #PWR0209.1 |
| -5VA | 1 | power | #PWR0198.1, C147.1, U107.3, J103.7, #PWR0190.1 |
| /BUCK_COMP | 1 | local | C134.1, R119.2, U103.6 |
| /VREG1B | 1 | local | U101.4, U101.14, C105.1 |
| GND | 1 | power | #PWR0194.1, J103.11, J103.12, J103.13, #PWR0129.1, L104.1, #PWR0154.1, U105.21, C131.1, #PWR0152.1, #PWR0185.1, J103.2, U101.13, U101.19, U101.21, #PWR0123.1, #PWR0153.1, U104.21, #PWR0104.1, J102.2, J101.3, J101.4, #PWR0103.1, U102.7, #PWR0121.1, J103.10, #PWR0193.1, R118.2, #PWR0150.1, #PWR0155.1, U103.7, U103.9, R110.1, #PWR0127.1, U105.2, U105.4, U105.5, U105.6, U105.7, U105.8, U105.9, U105.10, U105.11, U105.12, U105.17, U105.18, U105.19, #PWR0159.1, J103.6, #PWR0189.1, #PWR0158.1, U104.2, U104.7, U104.17, U104.18, U104.19, #PWR0191.1, J103.8, J103.4, #PWR0187.1, #PWR0151.1, C130.1, #PWR0118.1, C107.1, C143.2, #PWR0171.1, C132.1, #PWR0156.1, R113.1, #PWR0130.1, C124.2, #PWR0142.1, C146.2, #PWR0180.1, C110.2, #PWR0122.1, #PWR0120.1, C109.1, #PWR0204.1, H104.1, C113.2, #PWR0132.1, C112.2, #PWR0128.1, C106.1, #PWR0115.1, C115.1, #PWR0131.1, C128.1, #PWR0148.1, R121.2, #PWR0163.1, #PWR0211.1, TP108.1, D104.2, #PWR0166.1, C137.2, #PWR0161.1, C117.1, #PWR0135.1, #PWR0134.1, C116.2, D106.2, #PWR0208.1, U106.5, #PWR0179.1, U106.8, U106.11, #PWR0181.1, R103.2, #PWR0110.1, #PWR0147.1, R117.2, C134.2, #PWR0157.1, C141.2, #PWR0169.1, #PWR0119.1, D101.2, #PWR0162.1, C139.2, #PWR0145.1, C127.1, C114.2, #PWR0133.1, C120.1, #PWR0138.1, #PWR0165.1, R123.2, #PWR0160.1, C136.2, C122.2, #PWR0140.1, C123.1, #PWR0141.1, #PWR0111.1, R104.2, #PWR0202.1, C150.1, #PWR0206.1, D105.1, #PWR0210.1, TP107.1, C129.1, #PWR0149.1, U108.2, #PWR0201.1, #PWR0113.1, C104.1, R125.2, #PWR0172.1, #PWR0176.1, R126.2, #PWR0196.1, C147.2, #PWR0102.1, C101.1, #PWR0112.1, C103.1, C142.2, #PWR0170.1, #PWR0205.1, C151.1, C149.1, #PWR0199.1, C140.2, #PWR0164.1, U102.4, #PWR0124.1, #PWR0144.1, C126.1, C119.1, #PWR0137.1, #PWR0197.1, C148.1, #PWR0136.1, C118.1, #PWR0125.1, C111.2, C125.1, #PWR0143.1, #PWR0175.1, C144.1, U107.1, #PWR0182.1, C145.1, #PWR0177.1, C121.1, #PWR0139.1, #PWR0117.1, C108.1, #PWR0114.1, C105.2, C102.1, #PWR0108.1 |
| N$11 | 1 | unnamed | U101.5, R110.2, R111.1 |
| N$12 | 1 | unnamed | U101.11, R114.1, R112.1 |
| N$13 | 1 | unnamed | U101.1, L102.1 |
| N$14 | 1 | unnamed | U101.18, D103.1, L104.2 |
| N$15 | 1 | unnamed | U101.6, R107.2 |
| N$16 | 1 | unnamed | U101.12, C114.1, R112.2 |
| N$18 | 1 | unnamed | U101.10, R108.2 |
| N$19 | 1 | unnamed | R120.2, R121.1, U104.3, C135.1 |
| N$20 | 1 | unnamed | R102.2, U101.7, U101.9, R103.1, R101.1 |
| N$21 | 1 | unnamed | U102.10, R104.1 |
| N$22 | 1 | unnamed | U102.8, C108.2 |
| N$23 | 1 | unnamed | D103.2, L106.1, R114.2, TP102.1, C121.2, C118.2 |
| N$24 | 1 | unnamed | L103.1, U102.2 |
| N$25 | 1 | unnamed | D104.1, L107.1, C133.2, U103.8 |
| N$26 | 1 | unnamed | U104.14, C130.2 |
| N$27 | 1 | unnamed | U105.14, C131.2 |
| N$28 | 1 | unnamed | C106.2, R108.1 |
| N$29 | 1 | unnamed | L106.2, C129.2, U105.13, U105.15, U105.16, C127.2 |
| N$31 | 1 | unnamed | R106.2, C109.2, U102.6, C107.2, C103.2, FB101.2 |
| N$32 | 1 | unnamed | R106.1, U102.1 |
| N$33 | 1 | unnamed | U106.7, R126.1, C145.2 |
| N$35 | 1 | unnamed | R107.1, C104.2 |
| N$36 | 1 | unnamed | U108.3, FB103.2, C148.2 |
| N$37 | 1 | unnamed | U108.1, C150.2, FB104.2 |
| N$38 | 1 | unnamed | C113.1, R109.1, R101.2, U102.5 |
| N$39 | 1 | unnamed | R113.2, U102.9, R115.2 |
| N$40 | 1 | unnamed | C115.2, L103.2, U102.3, C119.2, FB102.1 |
| N$41 | 1 | unnamed | R116.2, R117.1, U103.3 |
| N$42 | 1 | unnamed | C117.2, C120.2, D102.1, L105.1, R111.2, TP101.1 |
| N$43 | 1 | unnamed | R118.1, U103.4 |
| N$44 | 1 | unnamed | R122.2, R123.1, U105.3, C138.1 |
| N$45 | 1 | unnamed | C132.2, R119.1 |
| N$46 | 1 | unnamed | R124.2, R125.1, U103.5 |
| N$47 | 1 | unnamed | R127.2, D105.2 |
| N$48 | 1 | unnamed | C128.2, U104.13, U104.15, U104.16, L105.2, C126.2 |
| N$49 | 1 | unnamed | R128.2, D106.1 |
| N$5 | 1 | unnamed | F101.1, J101.1, J101.2, J102.1 |
| N$50 | 1 | unnamed | C133.1, U103.1 |
| N$6 | 1 | unnamed | L101.2, C124.1, C112.1, R116.1, C122.1, C116.1, U103.2 |
| N$7 | 1 | unnamed | L101.1, C110.1, F101.2, C111.1, D101.1 |
| N$8 | 1 | unnamed | U101.2, R105.2 |
| N$9 | 1 | unnamed | U101.20, D102.2, L102.2 |
| VBUS | 1 | power | U101.15, U101.16, U101.17, #PWR0109.1, C143.1, L107.2, C141.1, R124.1, C142.1, #PWR0173.1, #PWR0105.1, FB101.1, R102.1, #PWR0106.1, FB103.1, #PWR0183.1, #PWR0107.1, C102.2, C101.2, #PWR0101.1 |

### 电源网络去耦统计（按 power_in 引脚所在网络）

| 电源网络 | PDF页 | power_in 引脚 | 电容数 | 电容位号 | 判定 |
| --- | --- | --- | --- | --- | --- |
| +12VA | 1 | U106.1 | 4 | C135, C136, C139, C144 | OK |
| -12VA | 1 | U107.2 | 4 | C137, C138, C140, C146 | OK |
| GND | 1 | U101.13, U101.19, U101.21, U103.7, U103.9, U106.8, U108.2, U102.4, U107.1 | 48 | C101, C102, C103, C104, C105, C106, C107, C108, C109, C110, C111, C112, C113, C114, C115, C116, C117, C118, C119, C120 | OK |
| N$31 | 1 | U102.6 | 3 | C103, C107, C109 | OK |
| N$36 | 1 | U108.3 | 1 | C148 | OK |
| N$6 | 1 | U103.2 | 4 | C112, C116, C122, C124 | OK |
| VBUS | 1 | U101.15, U101.16, U101.17 | 5 | C101, C102, C141, C142, C143 | OK |

## 3. 设计审查发现

### 警告（1）

| # | PDF页 | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | `/` | RU603 | 图纸 / 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |

### 提示（5）

| # | PDF页 | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | `/` | RU402 | 项目有 42 个未命名网络（N$，占网络总数 81%）；关键信号建议命名以便跨页追踪与复查。最大的几个: N$6(7 脚); N$23(6 脚); N$29(6 脚); N$31(6 脚); N$42(6 脚) | N$6, N$23, N$29 | heuristic |
| 2 | 1 | `/ / D101` | RU801 | D101（SMAJ36A）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(A1)->N$7; 2(A2)->GND |  | structural |
| 3 | 1 | `/ / U101` | RU304 | U101（ADP5071ACPZ）有 2 个引脚被标记为 no-connect: 3, 8（类型 input, passive）；请对照手册确认这些脚确实可悬空 |  | structural |
| 4 | 1 | `/ / U104` | RU304 | U104（TPS7A4701RGWR）有 8 个引脚被标记为 no-connect: 4, 5, 6, 8, 9, 10, 11, 12（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 5 | 1 | `/ / U106` | RU304 | U106（GM1200ACPZ）有 1 个引脚被标记为 no-connect: 4（类型 open_collector）；请对照手册确认这些脚确实可悬空 |  | structural |

## 4. 工具与方法说明

- 网络表由纯 Python 几何连通域构建（导线端点 + 连接点 + 标签 + 电源符号），并完成分层图纸与全局标签合并。
- 悬空/单引脚等判定基于本工具解析结果；KiCad ERC 结果（如已运行）以 ERC-* 代码单独列出。
- 报告中的 info 级发现需要人工结合设计意图判断，不代表设计错误。
- 发现条目带"依据"级别：official=官方 ERC 转写；structural=原理图结构事实；declared=字段约定检查；heuristic=启发式建议（可结合设计意图忽略）。
