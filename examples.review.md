# KiCad 原理图审查报告 — examples.review

> 由 kicad-sch-reader 自动生成，根原理图：`D:\MyProjects\AI\schematics_review_tool\examples\Lock-In-Amplifier_MainBoard_V0.1`

## 1. 工程概览

| 项目 | 值 |
| --- | --- |
| 图纸页数 | 5 |
| 元件符号数 | 484 |
| 网络数 | 182（命名网络 53） |
| 已解析引脚连接数 | 964 |
| 发现问题总数 | 35 |
| 问题分级 | error=0 / warning=20 / info=15 |
| KiCad ERC | warnings=20 |

### 图纸清单（页码按 KiCad 导出顺序 = PDF 页序）

| PDF页 | 路径 | 文件 | 标题 | 元件 | 导线 | 标签 | 连接点 | NC | 版本/生成器 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `/` | `Lock-In-Amplifier_MainBoard_V0.1.kicad_sch` | Digital Lock-In Amplifier | 43 | 139 | 72 | 10 | 20 | 20260306 / eeschema 10.0 |
| 2 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | `lia_analog_front_end.kicad_sch` | Digital Lock-In Amplifier | 146 | 187 | 16 | 36 | 0 | 20260306 / eeschema 10.0 |
| 7 | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | `lia_internal_ref_source.kicad_sch` | Digital Lock-In Amplifier | 110 | 195 | 25 | 29 | 0 | 20260306 / eeschema 10.0 |
| 3 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | `lia_adc_block.kicad_sch` | Digital Lock-In Amplifier | 105 | 153 | 11 | 33 | 3 | 20260306 / eeschema 10.0 |
| 4 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | `lia_ref_input.kicad_sch` | Digital Lock-In Amplifier | 80 | 106 | 7 | 19 | 0 | 20260306 / eeschema 10.0 |

### 元件清单（位号 / Value / 封装 / 页码）

共 255 个实体元件；其中无源件 172、测试点 20。电源符号 (#PWR) 不列在表内，JSON `components` 中保留全部。

| PDF页 | 位号 | Value/型号 | 库 | 封装 | 图纸 | 类型 | DNP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | C201 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C202 | 2.2uF | Device:C_Small | Capacitor_THT:C_Disc_D7.5mm_W5.0mm_P5.00mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C204 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C205 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C206 | 2.2uF | Device:C_Small | Capacitor_THT:C_Disc_D7.5mm_W5.0mm_P5.00mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C207 | 100pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C208 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C209 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C211 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C212 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C213 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C214 | 100pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C215 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C216 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C217 | 390pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C218 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C219 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C220 | 100pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C223 | 270pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C224 | 100pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C226 | 1.2nF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C227 | 100pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | C232 | 100pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 3 | C301 | 220pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C302 | 220pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C303 | 220pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C304 | 2.2nF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C305 | 220pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C306 | 4.7uF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C307 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C308 | 1uF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C309 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C310 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C311 | 1uF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C312 | 22uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C313 | 1uF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C314 | 1uF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C315 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C316 | 22uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C317 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C318 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C319 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C320 | 10uF | Device:C_Small | Capacitor_SMD:C_0805_2012Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C321 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C322 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C323 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | C324 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 4 | C401 | 2.2uF | Device:C_Small | Capacitor_THT:C_Disc_D7.5mm_W5.0mm_P5.00mm | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | C402 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | C403 | 100pF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive | yes |
| 4 | C404 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | C405 | 4.7uF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | C406 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | C407 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | C408 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | C409 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | C410 | DNP | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive | yes |
| 7 | C701 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C702 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C704 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C705 | 270pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C706 | 33pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C707 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C708 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C709 | 330pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C710 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C712 | 100pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C713 | 300pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C714 | 150pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C715 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C716 | 180pF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C717 | 4.7uF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C718 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C719 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C720 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C721 | 4.7uF | Device:C_Small | Capacitor_SMD:C_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | C722 | 100nF | Device:C_Small | Capacitor_SMD:C_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 2 | D201 | BAV199 | Diode:BAV99 | Package_TO_SOT_SMD:SOT-23 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | D202 | BAV199 | Diode:BAV99 | Package_TO_SOT_SMD:SOT-23 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | D203 | BSD5C121V-ES | Diode:SD12C-01F | Diode_SMD:D_SOD-323F | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | D204 | BSD5C121V-ES | Diode:SD12C-01F | Diode_SMD:D_SOD-323F | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 4 | D401 | BAV199 | Diode:BAV99 | Package_TO_SOT_SMD:SOT-23 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | D402 | BAV199 | Diode:BAV99 | Package_TO_SOT_SMD:SOT-23 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | D403 | 0603 YELLOW | Device:LED | LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | D404 | 0603 GREEN | Device:LED | LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | D405 | BSD5C121V-ES | Diode:SD12C-01F | Diode_SMD:D_SOD-323F | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 7 | D701 | BSD5C121V-ES | Diode:SD12C-01F | Diode_SMD:D_SOD-323F | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 3 | FB301 | GZ2012D601TF | Device:FerriteBead_Small | Inductor_SMD:L_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | FB302 | GZ2012D601TF | Device:FerriteBead_Small | Inductor_SMD:L_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | FB303 | GZ2012D601TF | Device:FerriteBead_Small | Inductor_SMD:L_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 4 | FB401 | GZ2012D601TF | Device:FerriteBead_Small | Inductor_SMD:L_0603_1608Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 1 | FID101 | MARKER | Mechanical:Fiducial | Emoe_Mechanical:Mark_D1.0mm | `/` | active |  |
| 1 | FID102 | MARKER | Mechanical:Fiducial | Emoe_Mechanical:Mark_D1.0mm | `/` | active |  |
| 1 | H101 | M2 | Mechanical:MountingHole | MountingHole:MountingHole_2.2mm_M2_DIN965 | `/` | active |  |
| 1 | H102 | M2 | Mechanical:MountingHole | MountingHole:MountingHole_2.2mm_M2_DIN965 | `/` | active |  |
| 1 | H103 | M2 | Mechanical:MountingHole | MountingHole:MountingHole_2.2mm_M2_DIN965 | `/` | active |  |
| 1 | H104 | M2 | Mechanical:MountingHole_Pad | MountingHole:MountingHole_2.2mm_M2_Pad_Via | `/` | active |  |
| 1 | J101 | Conn_02x40_Odd_Even | Connector_Generic:Conn_02x40_Odd_Even | Emoe_Connector_BTB:SGD-08_2x40P_0.8mm_Male | `/` | connector |  |
| 1 | J102 | Conn_01x16 | Connector_Generic:Conn_01x16 | Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Vertical | `/` | connector |  |
| 2 | J201 | MMCX | Connector:Conn_Coaxial | Connector_Coaxial:MMCX_Molex_73415-0961_Horizontal_1.6mm-PCB | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | connector |  |
| 2 | J202 | MMCX | Connector:Conn_Coaxial | Connector_Coaxial:MMCX_Molex_73415-0961_Horizontal_1.6mm-PCB | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | connector |  |
| 4 | J401 | MMCX | Connector:Conn_Coaxial | Connector_Coaxial:MMCX_Molex_73415-0961_Horizontal_1.6mm-PCB | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | connector |  |
| 7 | J701 | MMCX | Connector:Conn_Coaxial | Connector_Coaxial:MMCX_Molex_73415-0961_Horizontal_1.6mm-PCB | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | connector |  |
| 2 | K201 | G6KU-2F-Y-TR DC5 | Relay:G6K-2 | Relay_SMD:Relay_DPDT_Omron_G6K-2F-Y | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 4 | K401 | G6KU-2F-Y-TR DC5 | Relay:G6K-2 | Relay_SMD:Relay_DPDT_Omron_G6K-2F-Y | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active |  |
| 7 | L701 | LQW18CNR47J00D | Device:L_Small | Inductor_SMD:L_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | L702 | LQW18CNR39J00D | Device:L_Small | Inductor_SMD:L_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | L703 | LQW18CNR27J00D | Device:L_Small | Inductor_SMD:L_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 1 | R101 | 0R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/` | passive |  |
| 2 | R201 | 10Meg | Device:R_Small_US | Resistor_SMD:R_0805_2012Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R202 | 100R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R203 | 10Meg | Device:R_Small_US | Resistor_SMD:R_0805_2012Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R204 | 100R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R205 | RT0603BRD079K09L | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R206 | RT0603BRD079K09L | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R207 | RT0603BRD07200RL | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R208 | PTFR0603B909RN9 | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R209 | 4.7k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R210 | 2.2k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R211 | 2.2k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R212 | 2.2k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R213 | 2.7k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R214 | 2.7k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R215 | 3k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R216 | 1k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R217 | 1k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R218 | 1.3k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R220 | PTFR0603B909RN9 | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 2 | R221 | 0R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive | yes |
| 3 | R301 | 10k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R302 | 4.7R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R303 | 4.7R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R304 | 22R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R305 | 22R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R306 | 10k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R307 | 10k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R308 | 3R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R309 | 200mR | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R310 | 1k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R311 | 22R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R312 | 1k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | R313 | 22R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 4 | R401 | 10Meg | Device:R_Small_US | Resistor_SMD:R_0805_2012Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R402 | 1k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R403 | 2k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R404 | 100R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R405 | 2k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive | yes |
| 4 | R406 | 2k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R407 | 100R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R408 | 100R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R409 | 10k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R410 | 100k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive | yes |
| 4 | R411 | 910k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive | yes |
| 4 | R412 | 2k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R413 | 10k | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R414 | 100R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 4 | R415 | 100R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | passive |  |
| 7 | R701 | 49.9R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R702 | 200R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R703 | 49.9R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R704 | 7.5k | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R705 | 1.5k | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R706 | 1k | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R707 | 4.7R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R708 | 49.9R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R709 | 49.9R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R710 | 49.9R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R711 | 49.9R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R712 | 49.9R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R713 | 4.7R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R714 | RT0603BRD072KL | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R715 | 49.9R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R716 | 4.7R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R717 | 4.7R | Device:R_Small_US | Resistor_SMD:R_0402_1005Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R718 | 750R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R719 | 750R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R720 | 200R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | R721 | 200R | Device:R_Small_US | Resistor_SMD:R_0603_1608Metric | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 2 | RN201 | 4D03WGJ0330T5E | Device:R_Pack04 | Resistor_SMD:R_Array_Convex_4x0603 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | passive |  |
| 3 | RN301 | 4D03WGJ0330T5E | Device:R_Pack04 | Resistor_SMD:R_Array_Convex_4x0603 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 3 | RN302 | 4D03WGJ0330T5E | Device:R_Pack04 | Resistor_SMD:R_Array_Convex_4x0603 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | passive |  |
| 7 | RN701 | 4D03WGJ0330T5E | Device:R_Pack04 | Resistor_SMD:R_Array_Convex_4x0603 | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | RN702 | 4D03WGJ0330T5E | Device:R_Pack04 | Resistor_SMD:R_Array_Convex_4x0603 | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | RN703 | 4D03WGJ0330T5E | Device:R_Pack04 | Resistor_SMD:R_Array_Convex_4x0603 | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | RN704 | 4D03WGJ0330T5E | Device:R_Pack04 | Resistor_SMD:R_Array_Convex_4x0603 | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 7 | RN705 | 4D03WGJ0330T5E | Device:R_Pack04 | Resistor_SMD:R_Array_Convex_4x0603 | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | passive |  |
| 2 | TP201 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | testpoint | yes |
| 2 | TP202 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | testpoint | yes |
| 2 | TP203 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | testpoint | yes |
| 2 | TP204 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | testpoint | yes |
| 2 | TP205 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | testpoint | yes |
| 2 | TP206 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | testpoint | yes |
| 2 | TP207 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | testpoint | yes |
| 3 | TP301 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | testpoint | yes |
| 3 | TP302 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | testpoint | yes |
| 3 | TP303 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | testpoint | yes |
| 3 | TP304 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | testpoint | yes |
| 3 | TP305 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | testpoint | yes |
| 3 | TP306 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | testpoint | yes |
| 3 | TP307 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | testpoint | yes |
| 4 | TP401 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | testpoint | yes |
| 4 | TP402 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | testpoint | yes |
| 4 | TP403 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | testpoint | yes |
| 7 | TP701 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | testpoint | yes |
| 7 | TP702 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | testpoint | yes |
| 7 | TP703 | TP | Connector:TestPoint_Alt | TestPoint:TestPoint_Pad_1.0x1.0mm | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | testpoint | yes |
| 2 | U201 | OPA828IDR | Emoe_OpAmps:OPA828 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U201 | OPA828IDR | Emoe_OpAmps:OPA828 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U202 | MUX509IPWR | Emoe_AnalogSwitch:MUX509 | Package_SO:TSSOP-16_4.4x5mm_P0.65mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U202 | MUX509IPWR | Emoe_AnalogSwitch:MUX509 | Package_SO:TSSOP-16_4.4x5mm_P0.65mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U202 | MUX509IPWR | Emoe_AnalogSwitch:MUX509 | Package_SO:TSSOP-16_4.4x5mm_P0.65mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U203 | LHE5400-1 | Emoe_Analog_Devices:LT5400-1 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U203 | LHE5400-1 | Emoe_Analog_Devices:LT5400-1 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U203 | LHE5400-1 | Emoe_Analog_Devices:LT5400-1 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U203 | LHE5400-1 | Emoe_Analog_Devices:LT5400-1 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U203 | LHE5400-1 | Emoe_Analog_Devices:LT5400-1 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U204 | OPA828IDR | Emoe_OpAmps:OPA828 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U204 | OPA828IDR | Emoe_OpAmps:OPA828 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U205 | OPA828IDR | Emoe_OpAmps:OPA828 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U205 | OPA828IDR | Emoe_OpAmps:OPA828 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U206 | DRV8837CDSGR | Driver_Motor:DRV8837 | Package_SON:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U207 | OPA1678 | Amplifier_Operational:OPA1678 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U207 | OPA1678 | Amplifier_Operational:OPA1678 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U207 | OPA1678 | Amplifier_Operational:OPA1678 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U208 | OPA1656IDR | Amplifier_Operational:OPA1656ID | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U208 | OPA1656IDR | Amplifier_Operational:OPA1656ID | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 2 | U208 | OPA1656IDR | Amplifier_Operational:OPA1656ID | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | active |  |
| 3 | U301 | THS4551IRGTR | Amplifier_Difference:THS4551xRGT | Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U301 | THS4551IRGTR | Amplifier_Difference:THS4551xRGT | Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U302 | LHE5400-4 | Emoe_Analog_Devices:LT5400-4 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U302 | LHE5400-4 | Emoe_Analog_Devices:LT5400-4 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U302 | LHE5400-4 | Emoe_Analog_Devices:LT5400-4 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U302 | LHE5400-4 | Emoe_Analog_Devices:LT5400-4 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U302 | LHE5400-4 | Emoe_Analog_Devices:LT5400-4 | Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U303 | ADS127L11 | Emoe_ADDA:ADS127L11 | Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U303 | ADS127L11 | Emoe_ADDA:ADS127L11 | Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U304 | OPA171DBV | Emoe_OpAmps:OPA171 | Package_TO_SOT_SMD:SOT-23-5 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U304 | OPA171DBV | Emoe_OpAmps:OPA171 | Package_TO_SOT_SMD:SOT-23-5 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U305 | TPA5581 | Emoe_OpAmps:TPA5581 | Package_TO_SOT_SMD:SOT-23-6 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 3 | U306 | TPR7050 | Reference_Voltage:REF5050AD | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |
| 4 | U401 | DRV8837CDSGR | Driver_Motor:DRV8837 | Package_SON:WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active |  |
| 4 | U402 | OPA1678 | Amplifier_Operational:OPA1678 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active |  |
| 4 | U402 | OPA1678 | Amplifier_Operational:OPA1678 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active |  |
| 4 | U402 | OPA1678 | Amplifier_Operational:OPA1678 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active |  |
| 4 | U403 | TS5A3159DCK | Analog_Switch:TS5A3159DCK | Package_TO_SOT_SMD:SOT-363_SC-70-6 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active |  |
| 4 | U403 | TS5A3159DCK | Analog_Switch:TS5A3159DCK | Package_TO_SOT_SMD:SOT-363_SC-70-6 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active |  |
| 4 | U404 | TP1961 | Emoe_OpAmps:TP1961 | Package_TO_SOT_SMD:SOT-23-5 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active |  |
| 4 | U405 | 74LVC1G08 | 74xGxx:74LVC1G08 | Package_TO_SOT_SMD:SOT-23-5 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | active | yes |
| 7 | U701 | OPA1656IDR | Amplifier_Operational:OPA1656ID | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | active |  |
| 7 | U701 | OPA1656IDR | Amplifier_Operational:OPA1656ID | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | active |  |
| 7 | U701 | OPA1656IDR | Amplifier_Operational:OPA1656ID | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | active |  |
| 7 | U702 | TMUX4051PWR | Emoe_AnalogSwitch:TMUX4051 | Package_SO:TSSOP-16_4.4x5mm_P0.65mm | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | active |  |
| 7 | U703 | DAC904 | Emoe_ADDA:DAC904 | Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | active |  |
| 7 | U704 | OPA690IDBVR | Amplifier_Operational:OPA690xDBV | Package_TO_SOT_SMD:SOT-23-6 | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | active |  |
| 3 | Y301 | SX3M25.600M20F30TNN | Oscillator:ASE-xxxMHz | Oscillator:Oscillator_SMD_Abracon_ASE-4Pin_3.2x2.5mm | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | active |  |

## 2. 网络清单（按名称）

> 说明：同一网络的层次/全局端口别名并入同一行（例如 ADC_VREFIN 可能并入 /5V_VREF）；JSON `nets[].hierarchical_names/aliases` 保留全部别名。

| 网络 | 类型 | 别名/层次端口 | PDF页 | 引脚数 | 所在图纸 | 引脚示例 |
| --- | --- | --- | --- | --- | --- | --- |
| +12VA | power |  | 1, 2, 3, 4, 7 | 42 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /69c97752-28d7-4ad3-888a-2beb501d4b85, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | #PWR0104.1, J102.1, D202.2, #PWR0235.1, U208.8, #PWR0228.1, … |
| +3.3V | power |  | 1, 2, 3, 4, 7 | 37 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /69c97752-28d7-4ad3-888a-2beb501d4b85, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | #PWR0112.1, J102.9, #PWR0220.1, U206.7, #PWR0227.1, U202.2, … |
| +5VA | power |  | 1, 3, 7 | 27 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | #PWR0108.1, J102.5, C718.2, #PWR0716.1, C717.2, U703.24, … |
| +5VP | power |  | 1, 2, 4 | 15 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | #PWR0114.1, J102.14, J102.15, J102.16, J101.1, J101.3, … |
| -12VA | power |  | 1, 2, 4, 7 | 42 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /69c97752-28d7-4ad3-888a-2beb501d4b85, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | #PWR0105.1, J102.3, D202.1, #PWR0234.1, C209.1, #PWR0251.1, … |
| -5VA | power |  | 1, 7 | 4 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J102.7, #PWR0109.1, #PWR0744.1, R717.2 |
| /ADC_CS | hierarchical_port | ADC_CS | 1, 3 | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.51, RN301.2 |
| /ADC_DRDY | hierarchical_port | ADC_DRDY | 1, 3 | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.46, RN302.2 |
| /ADC_MISO | hierarchical_port | ADC_MISO | 1, 3 | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.44, RN302.1 |
| /ADC_MOSI | hierarchical_port | ADC_MOSI | 1, 3 | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.49, RN301.3 |
| /ADC_RESET | hierarchical_port | ADC_RESET | 1, 3 | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.53, RN301.1 |
| /ADC_SCLK | hierarchical_port | ADC_SCLK | 1, 3 | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.48, RN301.4 |
| /ADC_START | hierarchical_port | ADC_START | 1, 3 | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.42, RN302.3 |
| /Analog Front End/AFE_OUT_P | hierarchical_port | AFE_OUT_P | 2, 3 | 5 | /2cbef686-8f02-4c5f-bcf6-217497882ee3, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C232.1, TP205.1, U208.7, R217.2, U302.2 |
| /Analog Front End/CAL_IN+ | hierarchical_port | CAL_IN+ | 1, 2, 4 | 3 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R101.1, K201.4, K401.5 |
| /Analog Front End/GAIN_A0 | local | GAIN_A0 | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | RN201.1, U202.1 |
| /Analog Front End/GAIN_A1 | local | GAIN_A1 | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | RN201.2, U202.16 |
| /Analog Front End/IN_SW_CTL1 | local | IN_SW_CTL1 | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | RN201.3, U206.6 |
| /Analog Front End/IN_SW_CTL2 | local | IN_SW_CTL2 | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | RN201.4, U206.5 |
| /DAC_CLK | hierarchical_port | DAC_CLK | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.12, RN705.5 |
| /DAC_D0 | hierarchical_port | DAC_D0 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.25, RN702.8 |
| /DAC_D1 | hierarchical_port | DAC_D1 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.29, RN702.7 |
| /DAC_D10 | hierarchical_port | DAC_D10 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.22, RN704.6 |
| /DAC_D11 | hierarchical_port | DAC_D11 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.18, RN704.5 |
| /DAC_D12 | hierarchical_port | DAC_D12 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.16, RN705.8 |
| /DAC_D13 | hierarchical_port | DAC_D13 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.14, RN705.7 |
| /DAC_D2 | hierarchical_port | DAC_D2 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.31, RN702.6 |
| /DAC_D3 | hierarchical_port | DAC_D3 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.33, RN702.5 |
| /DAC_D4 | hierarchical_port | DAC_D4 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.28, RN703.8 |
| /DAC_D5 | hierarchical_port | DAC_D5 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.32, RN703.7 |
| /DAC_D6 | hierarchical_port | DAC_D6 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.34, RN703.6 |
| /DAC_D7 | hierarchical_port | DAC_D7 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.36, RN703.5 |
| /DAC_D8 | hierarchical_port | DAC_D8 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.26, RN704.8 |
| /DAC_D9 | hierarchical_port | DAC_D9 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.24, RN704.7 |
| /DAC_PD | hierarchical_port | DAC_PD | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.19, U703.15 |
| /GAIN_SW_A0 | hierarchical_port | GAIN_SW_A0 | 1, 2 | 2 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3 | J101.75, RN201.8 |
| /GAIN_SW_A1 | hierarchical_port | GAIN_SW_A1 | 1, 2 | 2 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3 | J101.77, RN201.7 |
| /IN_SW_C1 | hierarchical_port | IN_SW_C1 | 1, 2 | 2 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3 | J101.76, RN201.6 |
| /IN_SW_C2 | hierarchical_port | IN_SW_C2 | 1, 2 | 2 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3 | J101.78, RN201.5 |
| /Internal Reference Source/IOUT | local | IOUT | 7 | 4 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R711.2, U703.22, R709.1, R721.1 |
| /Internal Reference Source/SRC_OUT | hierarchical_port | SRC_OUT | 1, 7 | 4 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | R101.2, R701.1, J701.1, D701.2 |
| /Internal Reference Source/~{IOUT} | local | ~{IOUT} | 7 | 4 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R712.1, R710.2, U703.21, R720.2 |
| /LOCK_IND | hierarchical_port | LOCK_IND | 1, 4 | 2 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.35, R413.2 |
| /REFIN_CMP | hierarchical_port | REFIN_CMP | 1, 4 | 3 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.39, U403.4, R412.2 |
| /REF_CAL_1 | hierarchical_port | REF_CAL_1 | 1, 4 | 2 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.43, R414.1 |
| /REF_CAL_2 | hierarchical_port | REF_CAL_2 | 1, 4 | 2 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.45, R415.1 |
| /REF_SW | hierarchical_port | REF_SW | 1, 4 | 2 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.41, R404.2 |
| /SRC_ATT_A0 | hierarchical_port | SRC_ATT_A0 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.52, RN701.6 |
| /SRC_ATT_A1 | hierarchical_port | SRC_ATT_A1 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.54, RN701.7 |
| /SRC_ATT_A2 | hierarchical_port | SRC_ATT_A2 | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.56, RN701.8 |
| /SRC_ATT_EN | hierarchical_port | SRC_ATT_EN | 1, 7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.58, RN701.5 |
| GND | power | AFE_OUT_N, CAL_IN- | 1, 2, 3, 4, 7 | 314 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /69c97752-28d7-4ad3-888a-2beb501d4b85, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | #PWR0130.1, J101.40, #PWR0115.1, J102.11, J102.12, J102.13, … |
| N$100 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R207.1, R208.2, U202.6 |
| N$101 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R720.1, U704.3, R718.2 |
| N$102 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R702.2, U701.6 |
| N$103 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U207.3, R209.2, C214.2 |
| N$104 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U702.3, U701.5 |
| N$105 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R303.2, U301.11 |
| N$106 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.11, RN301.6 |
| N$107 | unnamed |  | 3 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.4, TP301.1, C303.2, R304.2, C304.1 |
| N$108 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.12, RN301.5 |
| N$109 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.19, RN302.6 |
| N$110 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.15, RN302.5 |
| N$111 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.14, RN302.7 |
| N$112 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.1, C311.1 |
| N$113 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.18, C308.1 |
| N$114 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.13, RN302.8 |
| N$115 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.10, RN301.7 |
| N$116 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.9, RN301.8 |
| N$117 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.3, R308.1 |
| N$118 | unnamed |  | 4 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | C403.1, K401.6, R410.1, C401.1 |
| N$119 | unnamed |  | 4 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | C403.2, R411.2, R410.2, U405.1 |
| N$120 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | D403.2, R412.1 |
| N$121 | unnamed |  | 3 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | TP304.1, C316.1, U305.3, R312.1 |
| N$122 | unnamed |  | 4 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U403.1, TP403.1, U405.4 |
| N$123 | unnamed |  | 4 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U403.3, TP402.1, R407.2, C410.2 |
| N$124 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U403.6, R404.1 |
| N$126 | unnamed |  | 3 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C306.1, FB301.2, C307.1, U303.16 |
| N$127 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R703.2, U704.5 |
| N$128 | unnamed |  | 3 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R307.1, U304.3, R306.1, C321.2 |
| N$129 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.6, RN704.1 |
| N$130 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.18, R714.2 |
| N$131 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.3, RN704.4 |
| N$132 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.10, RN703.1 |
| N$133 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.8, RN703.3 |
| N$134 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.9, RN703.2 |
| N$135 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.4, RN704.3 |
| N$136 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.5, RN704.2 |
| N$137 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.7, RN703.4 |
| N$138 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.23, C707.2 |
| N$139 | unnamed |  | 4 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | C404.1, U404.5, FB401.2, C405.1 |
| N$140 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | D404.2, R413.1 |
| N$141 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R405.1, U405.2 |
| N$142 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C704.2, R707.2, U701.8 |
| N$143 | unnamed |  | 4 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R409.1, U404.3, R408.2 |
| N$144 | unnamed |  | 4 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R409.2, U404.1, R407.1 |
| N$145 | unnamed |  | 7 | 5 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C705.2, U701.3, R708.2, C706.2, L701.1 |
| N$146 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN705.1, U703.2 |
| N$147 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN705.2, U703.1 |
| N$148 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN705.4, U703.28 |
| N$149 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R705.1, R704.2, U702.14 |
| N$150 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R706.1, R705.2, U702.15 |
| N$151 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C708.2, R713.1, U701.4 |
| N$152 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R211.2, U208.1, R216.1, C220.1 |
| N$153 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R311.2, Y301.3 |
| N$154 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R311.1, RN302.4 |
| N$156 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R212.2, U208.2, C220.2 |
| N$157 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R221.2, K201.7, J202.1 |
| N$158 | unnamed |  | 3 | 7 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C312.1, U303.7, R307.2, TP303.1, R309.1, C309.1, … |
| N$159 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R213.1, U207.1, U207.2 |
| N$160 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R213.2, R215.1, C223.1, R214.1 |
| N$161 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R215.2, C227.2, U207.6 |
| N$162 | unnamed |  | 7 | 5 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C712.2, L702.1, C709.2, C706.1, L701.2 |
| N$164 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R721.2, R719.1, U704.4 |
| N$165 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R218.1, C226.1, R216.2, R217.1 |
| N$166 | unnamed |  | 3 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C314.1, U305.4, R310.2 |
| N$167 | unnamed |  | 3 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C314.2, U305.1, R309.2 |
| N$168 | unnamed |  | 3 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C315.1, Y301.1, Y301.4, FB303.2 |
| N$169 | unnamed |  | 3 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C317.2, U306.6, R312.2 |
| N$170 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C318.1, U306.5 |
| N$171 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R414.2, U401.6 |
| N$172 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R415.2, U401.5 |
| N$173 | unnamed |  | 7 | 5 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C714.2, C712.1, L703.1, L702.2, C713.2 |
| N$174 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C715.1, U703.17 |
| N$175 | unnamed |  | 7 | 4 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R715.1, C714.1, L703.2, C716.2 |
| N$176 | unnamed |  | 7 | 4 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R715.2, R719.2, TP701.1, U704.1 |
| N$177 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R716.2, U704.6, C720.2 |
| N$178 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C719.2, U704.2, R717.1 |
| N$180 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C232.2, R218.2, U208.6 |
| N$181 | unnamed |  | 2 | 5 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C224.1, R209.1, TP204.1, U204.6, U203.1 |
| N$182 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C224.2, U203.7, U204.2, U203.8 |
| N$46 | unnamed |  | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | K201.2, J201.1 |
| N$47 | unnamed |  | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | K201.8, U206.2 |
| N$48 | unnamed |  | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | K201.1, U206.3 |
| N$53 | unnamed |  | 2 | 5 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | TP201.1, U203.3, R205.1, U201.6, U202.4 |
| N$54 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R210.1, C227.1, U207.7, R214.2 |
| N$55 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R210.2, R212.1, R211.1, C217.1 |
| N$56 | unnamed |  | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U201.2, U202.8 |
| N$57 | unnamed |  | 3 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C310.2, U303.2, C313.2, R308.2, FB302.1 |
| N$58 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C301.2, U301.4 |
| N$59 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R301.2, U301.12 |
| N$60 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U301.1, C302.1 |
| N$61 | unnamed |  | 4 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | K401.2, D405.2, J401.2 |
| N$62 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | K401.1, U401.2 |
| N$63 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | K401.8, U401.3 |
| N$64 | unnamed |  | 4 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | K401.7, J401.1 |
| N$65 | unnamed |  | 4 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R401.1, C401.2, R402.1 |
| N$66 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C710.1, U703.19 |
| N$67 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN701.3, U702.11 |
| N$68 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN701.1, U702.9 |
| N$69 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN701.4, U702.6 |
| N$70 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN701.2, U702.10 |
| N$71 | unnamed |  | 7 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R701.2, R702.1, U701.7 |
| N$72 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C202.2, D203.2, K201.3 |
| N$73 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C202.1, R201.2, R202.1 |
| N$74 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | D202.3, U205.3, TP207.1, R204.2 |
| N$75 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R220.2, R206.1, U202.12 |
| N$76 | unnamed |  | 3 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C320.2, U306.2, R313.2 |
| N$77 | unnamed |  | 3 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | TP302.1, U303.5, R305.1, C304.2, C305.1 |
| N$78 | unnamed |  | 3 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R302.1, U301.10 |
| N$79 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U203.6, C207.1, U204.3, U203.5 |
| N$80 | unnamed |  | 3 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U302.5, U301.3, C302.2, TP307.1, U302.6 |
| N$81 | unnamed |  | 3 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U302.7, U302.8, C301.1, U301.2, TP306.1 |
| N$82 | unnamed |  | 3 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U302.1, R302.2, R304.1 |
| N$83 | unnamed |  | 3 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U302.4, R303.1, R305.2 |
| N$84 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | D204.2, C206.2, K201.6 |
| N$85 | unnamed |  | 4 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | D402.3, R408.1, R406.2, R403.2 |
| N$86 | unnamed |  | 4 | 5 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U402.3, U402.5, TP401.1, D401.3, R402.2 |
| N$87 | unnamed |  | 4 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U402.6, U402.7, R403.1 |
| N$88 | unnamed |  | 4 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U402.1, U402.2, R406.1 |
| N$89 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R205.2, R208.1, U202.5 |
| N$90 | unnamed |  | 2 | 5 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U205.6, TP202.1, R206.2, U203.2, U202.13 |
| N$91 | unnamed |  | 2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U205.2, U202.9 |
| N$92 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C206.1, R204.1, R203.2 |
| N$93 | unnamed |  | 2 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | TP206.1, D201.3, U201.3, R202.2 |
| N$94 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN702.1, U703.14 |
| N$95 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN702.2, U703.13 |
| N$96 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN702.4, U703.11 |
| N$97 | unnamed |  | 7 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN702.3, U703.12 |
| N$98 | unnamed |  | 7 | 5 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | TP702.1, U701.1, U701.2, R704.1, U702.13 |
| N$99 | unnamed |  | 2 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R207.2, R220.1, U202.11 |
| VCM_2V5 | global_port |  | 3 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | TP305.1, U304.1, U304.4, U301.9 |

### 网络连接明细（全量，供逐条核对）

| 网络 | PDF页 | 类型 | 连接点（ref.pin） |
| --- | --- | --- | --- |
| +12VA | 1, 2, 3, 4, 7 | power | #PWR0104.1, J102.1, D202.2, #PWR0235.1, U208.8, #PWR0228.1, C205.1, #PWR0247.1, C211.1, #PWR0255.1, #PWR0206.1, U204.7, #PWR0245.1, C204.1, #PWR0210.1, U205.7, #PWR0231.1, D201.2, #PWR0207.1, U201.7, U202.14, #PWR0219.1, #PWR0262.1, C215.1, C216.1, #PWR0264.1, U207.8, #PWR0225.1, #PWR0715.1, R707.1, C701.2, #PWR0710.1, U702.16, #PWR0703.1, R313.1, #PWR0340.1, #PWR0410.1, D401.2, #PWR0416.1, U402.8, C406.1, #PWR0425.1 |
| +3.3V | 1, 2, 3, 4, 7 | power | #PWR0112.1, J102.9, #PWR0220.1, U206.7, #PWR0227.1, U202.2, #PWR0221.1, U206.8, #PWR0728.1, C722.2, C721.2, U703.27, #PWR0748.1, R703.1, C319.1, #PWR0339.1, FB303.1, FB301.1, #PWR0320.1, #PWR0414.1, FB401.1, #PWR0403.1, U401.7, R405.2, #PWR0421.1, D402.2, #PWR0413.1, #PWR0432.1, C409.1, U403.5, #PWR0411.1, #PWR0402.1, U401.8, #PWR0431.1, C408.1, #PWR0420.1, U405.5 |
| +5VA | 1, 3, 7 | power | #PWR0108.1, J102.5, C718.2, #PWR0716.1, C717.2, U703.24, R716.1, #PWR0743.1, FB302.2, #PWR0328.1, #PWR0311.1, R301.1, C324.2, #PWR0306.1, #PWR0336.1, U304.5, U305.6, #PWR0329.1, C322.2, #PWR0302.1, U301.5, U301.6, U301.7, U301.8, #PWR0309.1, #PWR0304.1, C323.2 |
| +5VP | 1, 2, 4 | power | #PWR0114.1, J102.14, J102.15, J102.16, J101.1, J101.3, #PWR0116.1, #PWR0222.1, U206.1, #PWR0212.1, C201.1, #PWR0401.1, U401.1, #PWR0407.1, C402.1 |
| -12VA | 1, 2, 4, 7 | power | #PWR0105.1, J102.3, D202.1, #PWR0234.1, C209.1, #PWR0251.1, U208.4, #PWR0229.1, #PWR0226.1, U207.4, #PWR0267.1, C218.1, C213.1, #PWR0259.1, #PWR0214.1, U204.4, #PWR0223.1, U202.3, D201.1, #PWR0232.1, C212.1, #PWR0257.1, C219.1, #PWR0269.1, #PWR0211.1, U205.4, #PWR0249.1, C208.1, U201.4, #PWR0208.1, R713.2, #PWR0731.1, C702.2, #PWR0712.1, U702.7, #PWR0702.1, #PWR0409.1, D401.1, C407.1, #PWR0426.1, U402.4, #PWR0417.1 |
| -5VA | 1, 7 | power | J102.7, #PWR0109.1, #PWR0744.1, R717.2 |
| /ADC_CS | 1, 3 | hierarchical_port | J101.51, RN301.2 |
| /ADC_DRDY | 1, 3 | hierarchical_port | J101.46, RN302.2 |
| /ADC_MISO | 1, 3 | hierarchical_port | J101.44, RN302.1 |
| /ADC_MOSI | 1, 3 | hierarchical_port | J101.49, RN301.3 |
| /ADC_RESET | 1, 3 | hierarchical_port | J101.53, RN301.1 |
| /ADC_SCLK | 1, 3 | hierarchical_port | J101.48, RN301.4 |
| /ADC_START | 1, 3 | hierarchical_port | J101.42, RN302.3 |
| /Analog Front End/AFE_OUT_P | 2, 3 | hierarchical_port | C232.1, TP205.1, U208.7, R217.2, U302.2 |
| /Analog Front End/CAL_IN+ | 1, 2, 4 | hierarchical_port | R101.1, K201.4, K401.5 |
| /Analog Front End/GAIN_A0 | 2 | local | RN201.1, U202.1 |
| /Analog Front End/GAIN_A1 | 2 | local | RN201.2, U202.16 |
| /Analog Front End/IN_SW_CTL1 | 2 | local | RN201.3, U206.6 |
| /Analog Front End/IN_SW_CTL2 | 2 | local | RN201.4, U206.5 |
| /DAC_CLK | 1, 7 | hierarchical_port | J101.12, RN705.5 |
| /DAC_D0 | 1, 7 | hierarchical_port | J101.25, RN702.8 |
| /DAC_D1 | 1, 7 | hierarchical_port | J101.29, RN702.7 |
| /DAC_D10 | 1, 7 | hierarchical_port | J101.22, RN704.6 |
| /DAC_D11 | 1, 7 | hierarchical_port | J101.18, RN704.5 |
| /DAC_D12 | 1, 7 | hierarchical_port | J101.16, RN705.8 |
| /DAC_D13 | 1, 7 | hierarchical_port | J101.14, RN705.7 |
| /DAC_D2 | 1, 7 | hierarchical_port | J101.31, RN702.6 |
| /DAC_D3 | 1, 7 | hierarchical_port | J101.33, RN702.5 |
| /DAC_D4 | 1, 7 | hierarchical_port | J101.28, RN703.8 |
| /DAC_D5 | 1, 7 | hierarchical_port | J101.32, RN703.7 |
| /DAC_D6 | 1, 7 | hierarchical_port | J101.34, RN703.6 |
| /DAC_D7 | 1, 7 | hierarchical_port | J101.36, RN703.5 |
| /DAC_D8 | 1, 7 | hierarchical_port | J101.26, RN704.8 |
| /DAC_D9 | 1, 7 | hierarchical_port | J101.24, RN704.7 |
| /DAC_PD | 1, 7 | hierarchical_port | J101.19, U703.15 |
| /GAIN_SW_A0 | 1, 2 | hierarchical_port | J101.75, RN201.8 |
| /GAIN_SW_A1 | 1, 2 | hierarchical_port | J101.77, RN201.7 |
| /IN_SW_C1 | 1, 2 | hierarchical_port | J101.76, RN201.6 |
| /IN_SW_C2 | 1, 2 | hierarchical_port | J101.78, RN201.5 |
| /Internal Reference Source/IOUT | 7 | local | R711.2, U703.22, R709.1, R721.1 |
| /Internal Reference Source/SRC_OUT | 1, 7 | hierarchical_port | R101.2, R701.1, J701.1, D701.2 |
| /Internal Reference Source/~{IOUT} | 7 | local | R712.1, R710.2, U703.21, R720.2 |
| /LOCK_IND | 1, 4 | hierarchical_port | J101.35, R413.2 |
| /REFIN_CMP | 1, 4 | hierarchical_port | J101.39, U403.4, R412.2 |
| /REF_CAL_1 | 1, 4 | hierarchical_port | J101.43, R414.1 |
| /REF_CAL_2 | 1, 4 | hierarchical_port | J101.45, R415.1 |
| /REF_SW | 1, 4 | hierarchical_port | J101.41, R404.2 |
| /SRC_ATT_A0 | 1, 7 | hierarchical_port | J101.52, RN701.6 |
| /SRC_ATT_A1 | 1, 7 | hierarchical_port | J101.54, RN701.7 |
| /SRC_ATT_A2 | 1, 7 | hierarchical_port | J101.56, RN701.8 |
| /SRC_ATT_EN | 1, 7 | hierarchical_port | J101.58, RN701.5 |
| GND | 1, 2, 3, 4, 7 | power | #PWR0130.1, J101.40, #PWR0115.1, J102.11, J102.12, J102.13, #PWR0106.1, J102.2, #PWR0123.1, J101.47, J101.70, #PWR0127.1, #PWR0129.1, J101.50, J101.2, J101.4, #PWR0117.1, #PWR0134.1, J101.5, #PWR0118.1, J101.11, J101.13, J101.15, #PWR0120.1, #PWR0125.1, J101.67, #PWR0131.1, J101.30, #PWR0103.1, J101.79, #PWR0101.1, J101.80, #PWR0128.1, J101.60, #PWR0124.1, J101.57, #PWR0111.1, J102.8, J102.10, #PWR0113.1, J101.20, #PWR0132.1, #PWR0119.1, J101.10, #PWR0110.1, J102.6, #PWR0107.1, J102.4, #PWR0122.1, J101.27, J101.73, #PWR0126.1, J101.17, #PWR0121.1, J101.37, #PWR0133.1, #PWR0102.1, H104.1, #PWR0218.1, K201.5, #PWR0258.1, C212.2, C209.2, #PWR0252.1, D204.1, #PWR0238.1, D203.1, #PWR0237.1, C205.2, #PWR0248.1, U208.3, #PWR0271.1, C211.2, #PWR0256.1, #PWR0215.1, U203.4, C213.2, #PWR0260.1, R221.1, #PWR0233.1, #PWR0282.1, C226.2, #PWR0205.1, U202.7, #PWR0266.1, C217.2, U202.15, #PWR0224.1, C219.2, #PWR0270.1, U208.5, #PWR0287.1, #PWR0216.1, C207.2, C215.2, #PWR0263.1, #PWR0265.1, C216.2, C204.2, #PWR0246.1, C218.2, #PWR0268.1, #PWR0213.1, C201.2, #PWR0281.1, U207.5, C208.2, #PWR0250.1, U203.9, #PWR0217.1, #PWR0236.1, TP203.1, J202.2, #PWR0203.1, #PWR0230.1, R201.1, #PWR0202.1, J201.2, U206.4, U206.9, #PWR0209.1, C223.2, #PWR0276.1, #PWR0204.1, U202.10, R203.1, #PWR0201.1, #PWR0261.1, C214.1, U702.8, #PWR0704.1, #PWR0734.1, U703.16, #PWR0750.1, D701.1, #PWR0738.1, U703.26, #PWR0739.1, U703.20, #PWR0735.1, C717.1, #PWR0730.1, R714.1, #PWR0721.1, R710.1, #PWR0746.1, RN705.3, C718.1, #PWR0736.1, #PWR0709.1, U702.4, #PWR0719.1, C705.1, #PWR0720.1, R709.2, C702.1, #PWR0713.1, #PWR0726.1, C709.1, R706.2, #PWR0714.1, #PWR0737.1, C719.1, #PWR0722.1, R711.1, C722.1, #PWR0742.1, C708.1, #PWR0725.1, R712.2, #PWR0723.1, #PWR0741.1, C721.1, C715.2, #PWR0732.1, #PWR0727.1, C710.2, #PWR0705.1, U702.12, RN705.6, #PWR0747.1, #PWR0745.1, R718.1, C704.1, #PWR0717.1, #PWR0701.1, J701.2, #PWR0724.1, C707.1, C713.1, #PWR0729.1, C701.1, #PWR0711.1, R708.1, #PWR0718.1, #PWR0749.1, TP703.1, #PWR0740.1, C720.1, U702.1, #PWR0706.1, U702.2, #PWR0708.1, U702.5, #PWR0707.1, #PWR0733.1, C716.1, U303.20, #PWR0318.1, U303.17, #PWR0319.1, U302.3, #PWR0322.1, U303.8, #PWR0308.1, U301.13, U301.14, U301.15, U301.16, #PWR0327.1, C313.1, #PWR0330.1, U305.2, #PWR0314.1, C305.2, #PWR0335.1, C318.2, C310.1, #PWR0324.1, #PWR0332.1, C316.2, C306.2, #PWR0315.1, C324.1, #PWR0307.1, #PWR0301.1, C321.1, #PWR0303.1, C322.1, #PWR0321.1, R306.2, #PWR0312.1, U302.9, C320.1, #PWR0337.1, C312.2, #PWR0326.1, C317.1, #PWR0334.1, #PWR0317.1, C308.2, #PWR0341.1, U306.4, C307.2, #PWR0316.1, C303.1, #PWR0313.1, C319.2, #PWR0338.1, #PWR0342.1, U304.2, #PWR0331.1, C315.2, #PWR0305.1, C323.1, U301.17, #PWR0310.1, C311.2, #PWR0325.1, Y301.2, #PWR0333.1, C309.2, #PWR0323.1, #PWR0406.1, R401.2, K401.3, #PWR0436.1, D405.1, K401.4, #PWR0415.1, U404.4, #PWR0433.1, C410.1, D402.1, #PWR0412.1, #PWR0418.1, U403.2, #PWR0419.1, U405.3, D404.1, #PWR0435.1, #PWR0430.1, C407.2, C402.2, #PWR0408.1, #PWR0422.1, U404.2, C404.2, #PWR0423.1, D403.1, #PWR0404.1, #PWR0434.1, C409.2, #PWR0428.1, C408.2, #PWR0405.1, U401.4, U401.9, C405.2, #PWR0424.1, #PWR0429.1, C406.2, R411.1, #PWR0427.1 |
| N$100 | 2 | unnamed | R207.1, R208.2, U202.6 |
| N$101 | 7 | unnamed | R720.1, U704.3, R718.2 |
| N$102 | 7 | unnamed | R702.2, U701.6 |
| N$103 | 2 | unnamed | U207.3, R209.2, C214.2 |
| N$104 | 7 | unnamed | U702.3, U701.5 |
| N$105 | 3 | unnamed | R303.2, U301.11 |
| N$106 | 3 | unnamed | U303.11, RN301.6 |
| N$107 | 3 | unnamed | U303.4, TP301.1, C303.2, R304.2, C304.1 |
| N$108 | 3 | unnamed | U303.12, RN301.5 |
| N$109 | 3 | unnamed | U303.19, RN302.6 |
| N$110 | 3 | unnamed | U303.15, RN302.5 |
| N$111 | 3 | unnamed | U303.14, RN302.7 |
| N$112 | 3 | unnamed | U303.1, C311.1 |
| N$113 | 3 | unnamed | U303.18, C308.1 |
| N$114 | 3 | unnamed | U303.13, RN302.8 |
| N$115 | 3 | unnamed | U303.10, RN301.7 |
| N$116 | 3 | unnamed | U303.9, RN301.8 |
| N$117 | 3 | unnamed | U303.3, R308.1 |
| N$118 | 4 | unnamed | C403.1, K401.6, R410.1, C401.1 |
| N$119 | 4 | unnamed | C403.2, R411.2, R410.2, U405.1 |
| N$120 | 4 | unnamed | D403.2, R412.1 |
| N$121 | 3 | unnamed | TP304.1, C316.1, U305.3, R312.1 |
| N$122 | 4 | unnamed | U403.1, TP403.1, U405.4 |
| N$123 | 4 | unnamed | U403.3, TP402.1, R407.2, C410.2 |
| N$124 | 4 | unnamed | U403.6, R404.1 |
| N$126 | 3 | unnamed | C306.1, FB301.2, C307.1, U303.16 |
| N$127 | 7 | unnamed | R703.2, U704.5 |
| N$128 | 3 | unnamed | R307.1, U304.3, R306.1, C321.2 |
| N$129 | 7 | unnamed | U703.6, RN704.1 |
| N$130 | 7 | unnamed | U703.18, R714.2 |
| N$131 | 7 | unnamed | U703.3, RN704.4 |
| N$132 | 7 | unnamed | U703.10, RN703.1 |
| N$133 | 7 | unnamed | U703.8, RN703.3 |
| N$134 | 7 | unnamed | U703.9, RN703.2 |
| N$135 | 7 | unnamed | U703.4, RN704.3 |
| N$136 | 7 | unnamed | U703.5, RN704.2 |
| N$137 | 7 | unnamed | U703.7, RN703.4 |
| N$138 | 7 | unnamed | U703.23, C707.2 |
| N$139 | 4 | unnamed | C404.1, U404.5, FB401.2, C405.1 |
| N$140 | 4 | unnamed | D404.2, R413.1 |
| N$141 | 4 | unnamed | R405.1, U405.2 |
| N$142 | 7 | unnamed | C704.2, R707.2, U701.8 |
| N$143 | 4 | unnamed | R409.1, U404.3, R408.2 |
| N$144 | 4 | unnamed | R409.2, U404.1, R407.1 |
| N$145 | 7 | unnamed | C705.2, U701.3, R708.2, C706.2, L701.1 |
| N$146 | 7 | unnamed | RN705.1, U703.2 |
| N$147 | 7 | unnamed | RN705.2, U703.1 |
| N$148 | 7 | unnamed | RN705.4, U703.28 |
| N$149 | 7 | unnamed | R705.1, R704.2, U702.14 |
| N$150 | 7 | unnamed | R706.1, R705.2, U702.15 |
| N$151 | 7 | unnamed | C708.2, R713.1, U701.4 |
| N$152 | 2 | unnamed | R211.2, U208.1, R216.1, C220.1 |
| N$153 | 3 | unnamed | R311.2, Y301.3 |
| N$154 | 3 | unnamed | R311.1, RN302.4 |
| N$156 | 2 | unnamed | R212.2, U208.2, C220.2 |
| N$157 | 2 | unnamed | R221.2, K201.7, J202.1 |
| N$158 | 3 | unnamed | C312.1, U303.7, R307.2, TP303.1, R309.1, C309.1, R310.1 |
| N$159 | 2 | unnamed | R213.1, U207.1, U207.2 |
| N$160 | 2 | unnamed | R213.2, R215.1, C223.1, R214.1 |
| N$161 | 2 | unnamed | R215.2, C227.2, U207.6 |
| N$162 | 7 | unnamed | C712.2, L702.1, C709.2, C706.1, L701.2 |
| N$164 | 7 | unnamed | R721.2, R719.1, U704.4 |
| N$165 | 2 | unnamed | R218.1, C226.1, R216.2, R217.1 |
| N$166 | 3 | unnamed | C314.1, U305.4, R310.2 |
| N$167 | 3 | unnamed | C314.2, U305.1, R309.2 |
| N$168 | 3 | unnamed | C315.1, Y301.1, Y301.4, FB303.2 |
| N$169 | 3 | unnamed | C317.2, U306.6, R312.2 |
| N$170 | 3 | unnamed | C318.1, U306.5 |
| N$171 | 4 | unnamed | R414.2, U401.6 |
| N$172 | 4 | unnamed | R415.2, U401.5 |
| N$173 | 7 | unnamed | C714.2, C712.1, L703.1, L702.2, C713.2 |
| N$174 | 7 | unnamed | C715.1, U703.17 |
| N$175 | 7 | unnamed | R715.1, C714.1, L703.2, C716.2 |
| N$176 | 7 | unnamed | R715.2, R719.2, TP701.1, U704.1 |
| N$177 | 7 | unnamed | R716.2, U704.6, C720.2 |
| N$178 | 7 | unnamed | C719.2, U704.2, R717.1 |
| N$180 | 2 | unnamed | C232.2, R218.2, U208.6 |
| N$181 | 2 | unnamed | C224.1, R209.1, TP204.1, U204.6, U203.1 |
| N$182 | 2 | unnamed | C224.2, U203.7, U204.2, U203.8 |
| N$46 | 2 | unnamed | K201.2, J201.1 |
| N$47 | 2 | unnamed | K201.8, U206.2 |
| N$48 | 2 | unnamed | K201.1, U206.3 |
| N$53 | 2 | unnamed | TP201.1, U203.3, R205.1, U201.6, U202.4 |
| N$54 | 2 | unnamed | R210.1, C227.1, U207.7, R214.2 |
| N$55 | 2 | unnamed | R210.2, R212.1, R211.1, C217.1 |
| N$56 | 2 | unnamed | U201.2, U202.8 |
| N$57 | 3 | unnamed | C310.2, U303.2, C313.2, R308.2, FB302.1 |
| N$58 | 3 | unnamed | C301.2, U301.4 |
| N$59 | 3 | unnamed | R301.2, U301.12 |
| N$60 | 3 | unnamed | U301.1, C302.1 |
| N$61 | 4 | unnamed | K401.2, D405.2, J401.2 |
| N$62 | 4 | unnamed | K401.1, U401.2 |
| N$63 | 4 | unnamed | K401.8, U401.3 |
| N$64 | 4 | unnamed | K401.7, J401.1 |
| N$65 | 4 | unnamed | R401.1, C401.2, R402.1 |
| N$66 | 7 | unnamed | C710.1, U703.19 |
| N$67 | 7 | unnamed | RN701.3, U702.11 |
| N$68 | 7 | unnamed | RN701.1, U702.9 |
| N$69 | 7 | unnamed | RN701.4, U702.6 |
| N$70 | 7 | unnamed | RN701.2, U702.10 |
| N$71 | 7 | unnamed | R701.2, R702.1, U701.7 |
| N$72 | 2 | unnamed | C202.2, D203.2, K201.3 |
| N$73 | 2 | unnamed | C202.1, R201.2, R202.1 |
| N$74 | 2 | unnamed | D202.3, U205.3, TP207.1, R204.2 |
| N$75 | 2 | unnamed | R220.2, R206.1, U202.12 |
| N$76 | 3 | unnamed | C320.2, U306.2, R313.2 |
| N$77 | 3 | unnamed | TP302.1, U303.5, R305.1, C304.2, C305.1 |
| N$78 | 3 | unnamed | R302.1, U301.10 |
| N$79 | 2 | unnamed | U203.6, C207.1, U204.3, U203.5 |
| N$80 | 3 | unnamed | U302.5, U301.3, C302.2, TP307.1, U302.6 |
| N$81 | 3 | unnamed | U302.7, U302.8, C301.1, U301.2, TP306.1 |
| N$82 | 3 | unnamed | U302.1, R302.2, R304.1 |
| N$83 | 3 | unnamed | U302.4, R303.1, R305.2 |
| N$84 | 2 | unnamed | D204.2, C206.2, K201.6 |
| N$85 | 4 | unnamed | D402.3, R408.1, R406.2, R403.2 |
| N$86 | 4 | unnamed | U402.3, U402.5, TP401.1, D401.3, R402.2 |
| N$87 | 4 | unnamed | U402.6, U402.7, R403.1 |
| N$88 | 4 | unnamed | U402.1, U402.2, R406.1 |
| N$89 | 2 | unnamed | R205.2, R208.1, U202.5 |
| N$90 | 2 | unnamed | U205.6, TP202.1, R206.2, U203.2, U202.13 |
| N$91 | 2 | unnamed | U205.2, U202.9 |
| N$92 | 2 | unnamed | C206.1, R204.1, R203.2 |
| N$93 | 2 | unnamed | TP206.1, D201.3, U201.3, R202.2 |
| N$94 | 7 | unnamed | RN702.1, U703.14 |
| N$95 | 7 | unnamed | RN702.2, U703.13 |
| N$96 | 7 | unnamed | RN702.4, U703.11 |
| N$97 | 7 | unnamed | RN702.3, U703.12 |
| N$98 | 7 | unnamed | TP702.1, U701.1, U701.2, R704.1, U702.13 |
| N$99 | 2 | unnamed | R207.2, R220.1, U202.11 |
| VCM_2V5 | 3 | global_port | TP305.1, U304.1, U304.4, U301.9 |

### 电源网络去耦统计（按 power_in 引脚所在网络）

| 电源网络 | PDF页 | power_in 引脚 | 电容数 | 电容位号 | 判定 |
| --- | --- | --- | --- | --- | --- |
| +12VA | 2, 4, 7 | U208.8, U204.7, U205.7, U201.7, U207.8, U702.16, U402.8 | 7 | C204, C205, C211, C215, C216, C406, C701 | OK |
| +3.3V | 2, 4, 7 | U206.8, U703.27, U403.5, U401.8, U405.5 | 5 | C319, C408, C409, C721, C722 | OK |
| +5VA | 3, 7 | U703.24, U304.5, U305.6, U301.5 | 5 | C322, C323, C324, C717, C718 | OK |
| +5VP | 2, 4 | U206.1, U401.1 | 2 | C201, C402 | OK |
| -12VA | 2, 4, 7 | U208.4, U207.4, U204.4, U205.4, U201.4, U702.7, U402.4 | 8 | C208, C209, C212, C213, C218, C219, C407, C702 | OK |
| GND | 2, 3, 4, 7 | U206.4, U702.8, U703.26, U703.20, U303.20, U301.13, U305.2, U306.4, U304.2, Y301.2, U403.2, U405.3 | 62 | C201, C204, C205, C207, C208, C209, C211, C212, C213, C214, C215, C216, C217, C218, C219, C223, C226, C303, C305, C306 | OK |
| N$117 | 3 | U303.3 | 0 |  | 未发现电容 |
| N$139 | 4 | U404.5 | 2 | C404, C405 | OK |
| N$142 | 7 | U701.8 | 1 | C704 | OK |
| N$151 | 7 | U701.4 | 1 | C708 | OK |
| N$168 | 3 | Y301.4 | 1 | C315 | OK |
| N$177 | 7 | U704.6 | 1 | C720 | OK |
| N$178 | 7 | U704.2 | 1 | C719 | OK |
| N$57 | 3 | U303.2 | 2 | C310, C313 | OK |
| N$76 | 3 | U306.2 | 1 | C320 | OK |

## 3. 设计审查发现

### 警告（20）

| # | PDF页 | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | `/` | ERC-lib_symbol_mismatch | 符号 'DRV8837' 与来源库 'Driver_Motor' 中的符号存在差异 |  | official |
| 2 | 1 | `/` | ERC-lib_symbol_mismatch | 符号 'DRV8837' 与来源库 'Driver_Motor' 中的符号存在差异 |  | official |
| 3 | 1 | `/` | ERC-lib_symbol_mismatch | 符号 'REF5050AD' 与来源库 'Reference_Voltage' 中的符号存在差异 |  | official |
| 4 | 1 | `/ / #PWR0109.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 5 | 1 | `/ / H104.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 6 | 0 | `/Analog Front End/ / #PWR0258.1` | ERC-multiple_net_names | GND 和 AFE_OUT_N 都连接到同一项上; 将使用 GND 作为网表中的网络名称 |  | official |
| 7 | 0 | `/Analog Front End/ / U201.4` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 8 | 0 | `/Analog Front End/ / U201.7` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 9 | 0 | `/Analog Front End/ / U206.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 10 | 0 | `/Analog Front End/ / U206.7` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 11 | 0 | `/Internal Reference Source/ / U701.4` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 12 | 0 | `/Internal Reference Source/ / U701.8` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 13 | 0 | `/Internal Reference Source/ / U704.2` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 14 | 0 | `/Internal Reference Source/ / U704.6` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 15 | 0 | `/Precision ADC Block/ / U301.5` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 16 | 0 | `/Precision ADC Block/ / U303.2` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 17 | 0 | `/Precision ADC Block/ / U303.3` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 18 | 0 | `/Precision ADC Block/ / U306.2` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 19 | 0 | `/Precision ADC Block/ / Y301.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 20 | 0 | `/Reference Input Scheme/ / U404.5` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |

### 提示（15）

| # | PDF页 | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | `/` | R103 | 9 个前缀的位号有缺号: C 缺445（C201..C722；段内缺号: C203, C210, C221, C222, C225, C228, C229, C230 …(+3)）, D 缺491（D201..D701）, FB 缺97（FB301..FB401）, J 缺595（J101..J701）, K 缺199（K201..K401）, R 缺551（R101..R721；段内缺号: R219）, RN 缺497（RN201..RN705）, TP 缺483（TP201..TP703）, U 缺481（U201..U704）。跨页编 hundreds 的工程跨段空号属正常（按页分段编号），段内缺号通常是迭代删除，仅供审阅时参考 |  | heuristic |
| 2 | 1 | `/` | R402 | 项目有 129 个未命名网络（N$，占网络总数 71%）；关键信号建议命名以便跨页追踪与复查。最大的几个: N$158(7 脚); N$107(5 脚); N$145(5 脚); N$162(5 脚); N$173(5 脚) | N$158, N$107, N$145 | heuristic |
| 3 | 1 | `/ / J101` | R304 | J101（Conn_02x40_Odd_Even）有 20 个引脚被标记为 no-connect: 6, 7, 8, 9, 21, 23, 38, 55, 59, 61, 62, 63 …(+8)（类型 passive）；请对照手册确认这些脚确实可悬空 |  | structural |
| 4 | 2 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | R701 | 8 个器件标记为不焊接（DNP）: TP201(TP), R221(0R), TP206(TP), TP205(TP), TP202(TP), TP204(TP), TP207(TP), TP203(TP)；其中 7 个为测试点/机械件，其余 1 个请确认 DNP 意图 |  | structural |
| 5 | 2 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / D203` | R801 | D203（BSD5C121V-ES）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(A1)->GND; 2(A2)->N$72 |  | structural |
| 6 | 2 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / D204` | R801 | D204（BSD5C121V-ES）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(A1)->GND; 2(A2)->N$84 |  | structural |
| 7 | 7 | `/69c97752-28d7-4ad3-888a-2beb501d4b85` | R701 | 3 个器件标记为不焊接（DNP）: TP702(TP), TP701(TP), TP703(TP)；其中 3 个为测试点/机械件，其余 0 个请确认 DNP 意图 |  | structural |
| 8 | 7 | `/69c97752-28d7-4ad3-888a-2beb501d4b85 / D701` | R801 | D701（BSD5C121V-ES）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(A1)->GND; 2(A2)->/Internal Reference Source/SRC_OUT |  | structural |
| 9 | 3 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | R701 | 7 个器件标记为不焊接（DNP）: TP304(TP), TP302(TP), TP305(TP), TP301(TP), TP303(TP), TP306(TP), TP307(TP)；其中 7 个为测试点/机械件，其余 0 个请确认 DNP 意图 |  | structural |
| 10 | 3 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / U303` | R304 | U303（ADS127L11）有 1 个引脚被标记为 no-connect: 6（类型 output）；请对照手册确认这些脚确实可悬空 |  | structural |
| 11 | 3 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / U303.3` | R501 | U303.3（ADS127L11）的电源网络 N$117 上没有检测到电容；请核对是否已就近放置去耦电容 | N$117 | heuristic |
| 12 | 3 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / U305` | R304 | U305（TPA5581）有 1 个引脚被标记为 no-connect: 5（类型 input）；请对照手册确认这些脚确实可悬空 |  | structural |
| 13 | 3 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / U306` | R304 | U306（TPR7050）有 4 个引脚被标记为 no-connect: 1, 3, 7, 8（类型 no_connect, passive）；请对照手册确认这些脚确实可悬空 |  | structural |
| 14 | 4 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | R701 | 9 个器件标记为不焊接（DNP）: C403(100pF), TP402(TP), TP403(TP), TP401(TP), R405(2k), C410(DNP), R411(910k), R410(100k), U405(74LVC1G08)；其中 3 个为测试点/机械件，其余 6 个请确认 DNP 意图 |  | structural |
| 15 | 4 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / D405` | R801 | D405（BSD5C121V-ES）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(A1)->GND; 2(A2)->N$61 |  | structural |

## 4. 工具与方法说明

- 网络表由纯 Python 几何连通域构建（导线端点 + 连接点 + 标签 + 电源符号），并完成分层图纸与全局标签合并。
- KiCad ERC 已运行: {'warning': 20}
- 悬空/单引脚等判定基于本工具解析结果；KiCad ERC 结果（如已运行）以 ERC-* 代码单独列出。
- 报告中的 info 级发现需要人工结合设计意图判断，不代表设计错误。
- 发现条目带"依据"级别：official=官方 ERC 转写；structural=原理图结构事实；declared=字段约定检查；heuristic=启发式建议（可结合设计意图忽略）。
