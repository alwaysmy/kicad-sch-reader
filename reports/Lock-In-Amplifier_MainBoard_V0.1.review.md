# KiCad 原理图审查报告 — Lock-In-Amplifier_MainBoard_V0.1.review

> 由 kicad-sch-reader 自动生成，根原理图：`D:\MyProjects\AI\schematics_review_tool\examples\Lock-In-Amplifier_MainBoard_V0.1`

## 1. 工程概览

| 项目 | 值 |
| --- | --- |
| 图纸页数 | 5 |
| 元件符号数 | 484 |
| 网络数 | 182（命名网络 53） |
| 已解析引脚连接数 | 964 |
| 发现问题总数 | 48 |
| 问题分级 | error=0 / warning=20 / info=28 |
| KiCad ERC | {'warning': 20} |

### 图纸清单

| 路径 | 文件 | 标题 | 元件 | 导线 | 标签 | 连接点 | NC | 版本/生成器 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `/` | `Lock-In-Amplifier_MainBoard_V0.1.kicad_sch` | Digital Lock-In Amplifier | 43 | 139 | 72 | 10 | 20 | 20260306 / eeschema 10.0 |
| `/2cbef686-8f02-4c5f-bcf6-217497882ee3` | `lia_analog_front_end.kicad_sch` | Digital Lock-In Amplifier | 146 | 187 | 16 | 36 | 0 | 20260306 / eeschema 10.0 |
| `/69c97752-28d7-4ad3-888a-2beb501d4b85` | `lia_internal_ref_source.kicad_sch` | Digital Lock-In Amplifier | 110 | 195 | 25 | 29 | 0 | 20260306 / eeschema 10.0 |
| `/843e73eb-7d0e-401b-9de9-9eb1eb874e61` | `lia_adc_block.kicad_sch` | Digital Lock-In Amplifier | 105 | 153 | 11 | 33 | 3 | 20260306 / eeschema 10.0 |
| `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b` | `lia_ref_input.kicad_sch` | Digital Lock-In Amplifier | 80 | 106 | 7 | 19 | 0 | 20260306 / eeschema 10.0 |

## 2. 网络清单（按名称）

| 网络 | 引脚数 | 所在图纸 | 引脚示例 |
| --- | --- | --- | --- |
| +12VA | 42 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /69c97752-28d7-4ad3-888a-2beb501d4b85, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | #PWR0104.1, J102.1, D202.2, #PWR0235.1, U208.8, #PWR0228.1, … |
| +3.3V | 37 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /69c97752-28d7-4ad3-888a-2beb501d4b85, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | #PWR0112.1, J102.9, #PWR0220.1, U206.7, #PWR0227.1, U202.2, … |
| +5VA | 27 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | #PWR0108.1, J102.5, C718.2, #PWR0716.1, C717.2, U703.24, … |
| +5VP | 15 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | #PWR0114.1, J102.14, J102.16, J102.15, J101.3, J101.1, … |
| -12VA | 42 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /69c97752-28d7-4ad3-888a-2beb501d4b85, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | #PWR0105.1, J102.3, D202.1, #PWR0234.1, C209.1, #PWR0251.1, … |
| -5VA | 4 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J102.7, #PWR0109.1, #PWR0744.1, R717.2 |
| /Analog Front End/AFE_OUT_P | 5 | /2cbef686-8f02-4c5f-bcf6-217497882ee3, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C232.1, TP205.1, U208.7, R217.2, U302.2 |
| /Analog Front End/CAL_IN+ | 3 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R101.1, K201.4, K401.5 |
| /Analog Front End/GAIN_SW_A0 | 2 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3 | J101.75, RN201.8 |
| /Analog Front End/GAIN_SW_A1 | 2 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3 | J101.77, RN201.7 |
| /Analog Front End/IN_SW_C1 | 2 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3 | J101.76, RN201.6 |
| /Analog Front End/IN_SW_C2 | 2 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3 | J101.78, RN201.5 |
| /GAIN_A0 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | RN201.1, U202.1 |
| /GAIN_A1 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | RN201.2, U202.16 |
| /IN_SW_CTL1 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | RN201.3, U206.6 |
| /IN_SW_CTL2 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | RN201.4, U206.5 |
| /IOUT | 4 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R711.2, U703.22, R709.1, R721.1 |
| /Internal Reference Source/DAC_CLK | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.12, RN705.5 |
| /Internal Reference Source/DAC_D0 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.25, RN702.8 |
| /Internal Reference Source/DAC_D1 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.29, RN702.7 |
| /Internal Reference Source/DAC_D10 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.22, RN704.6 |
| /Internal Reference Source/DAC_D11 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.18, RN704.5 |
| /Internal Reference Source/DAC_D12 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.16, RN705.8 |
| /Internal Reference Source/DAC_D13 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.14, RN705.7 |
| /Internal Reference Source/DAC_D2 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.31, RN702.6 |
| /Internal Reference Source/DAC_D3 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.33, RN702.5 |
| /Internal Reference Source/DAC_D4 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.28, RN703.8 |
| /Internal Reference Source/DAC_D5 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.32, RN703.7 |
| /Internal Reference Source/DAC_D6 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.34, RN703.6 |
| /Internal Reference Source/DAC_D7 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.36, RN703.5 |
| /Internal Reference Source/DAC_D8 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.26, RN704.8 |
| /Internal Reference Source/DAC_D9 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.24, RN704.7 |
| /Internal Reference Source/DAC_PD | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.19, U703.15 |
| /Internal Reference Source/SRC_ATT_A0 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.52, RN701.6 |
| /Internal Reference Source/SRC_ATT_A1 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.54, RN701.7 |
| /Internal Reference Source/SRC_ATT_A2 | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.56, RN701.8 |
| /Internal Reference Source/SRC_ATT_EN | 2 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | J101.58, RN701.5 |
| /Internal Reference Source/SRC_OUT | 4 | /, /69c97752-28d7-4ad3-888a-2beb501d4b85 | R101.2, R701.1, J701.1, D701.2 |
| /Precision ADC Block/ADC_CS | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.51, RN301.2 |
| /Precision ADC Block/ADC_DRDY | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.46, RN302.2 |
| /Precision ADC Block/ADC_MISO | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.44, RN302.1 |
| /Precision ADC Block/ADC_MOSI | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.49, RN301.3 |
| /Precision ADC Block/ADC_RESET | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.53, RN301.1 |
| /Precision ADC Block/ADC_SCLK | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.48, RN301.4 |
| /Precision ADC Block/ADC_START | 2 | /, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | J101.42, RN302.3 |
| /Reference Input Scheme/LOCK_IND | 2 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.35, R413.2 |
| /Reference Input Scheme/REFIN_CMP | 3 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.39, U403.4, R412.2 |
| /Reference Input Scheme/REF_CAL_1 | 2 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.43, R414.1 |
| /Reference Input Scheme/REF_CAL_2 | 2 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.45, R415.1 |
| /Reference Input Scheme/REF_SW | 2 | /, /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | J101.41, R404.2 |
| /~{IOUT} | 4 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R712.1, R710.2, U703.21, R720.2 |
| GND | 314 | /, /2cbef686-8f02-4c5f-bcf6-217497882ee3, /69c97752-28d7-4ad3-888a-2beb501d4b85, /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | #PWR0130.1, J101.40, #PWR0115.1, J102.13, J102.11, J102.12, … |
| N$100 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R207.1, R208.2, U202.6 |
| N$101 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R720.1, U704.3, R718.2 |
| N$102 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R702.2, U701.6 |
| N$103 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U207.3, R209.2, C214.2 |
| N$104 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U702.3, U701.5 |
| N$105 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R303.2, U301.11 |
| N$106 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.11, RN301.6 |
| N$107 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.4, TP301.1, C303.2, R304.2, C304.1 |
| N$108 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.12, RN301.5 |
| N$109 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.19, RN302.6 |
| N$110 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.15, RN302.5 |
| N$111 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.14, RN302.7 |
| N$112 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.1, C311.1 |
| N$113 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.18, C308.1 |
| N$114 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.13, RN302.8 |
| N$115 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.10, RN301.7 |
| N$116 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.9, RN301.8 |
| N$117 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U303.3, R308.1 |
| N$118 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | C403.1, K401.6, R410.1, C401.1 |
| N$119 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | C403.2, R411.2, R410.2, U405.1 |
| N$120 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | D403.2, R412.1 |
| N$121 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | TP304.1, C316.1, U305.3, R312.1 |
| N$122 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U403.1, TP403.1, U405.4 |
| N$123 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U403.3, TP402.1, R407.2, C410.2 |
| N$124 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U403.6, R404.1 |
| N$126 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C306.1, FB301.2, C307.1, U303.16 |
| N$127 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R703.2, U704.5 |
| N$128 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R307.1, U304.3, R306.1, C321.2 |
| N$129 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.6, RN704.1 |
| N$130 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.18, R714.2 |
| N$131 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.3, RN704.4 |
| N$132 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.10, RN703.1 |
| N$133 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.8, RN703.3 |
| N$134 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.9, RN703.2 |
| N$135 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.4, RN704.3 |
| N$136 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.5, RN704.2 |
| N$137 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.7, RN703.4 |
| N$138 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | U703.23, C707.2 |
| N$139 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | C404.1, U404.5, FB401.2, C405.1 |
| N$140 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | D404.2, R413.1 |
| N$141 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R405.1, U405.2 |
| N$142 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C704.2, R707.2, U701.8 |
| N$143 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R409.1, U404.3, R408.2 |
| N$144 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R409.2, U404.1, R407.1 |
| N$145 | 5 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C705.2, U701.3, R708.2, C706.2, L701.1 |
| N$146 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN705.1, U703.2 |
| N$147 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN705.2, U703.1 |
| N$148 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN705.4, U703.28 |
| N$149 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R705.1, R704.2, U702.14 |
| N$150 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R706.1, R705.2, U702.15 |
| N$151 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C708.2, R713.1, U701.4 |
| N$152 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R211.2, U208.1, R216.1, C220.1 |
| N$153 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R311.2, Y301.3 |
| N$154 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R311.1, RN302.4 |
| N$156 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R212.2, U208.2, C220.2 |
| N$157 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R221.2, K201.7, J202.1 |
| N$158 | 7 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C312.1, U303.7, R307.2, TP303.1, R309.1, C309.1, … |
| N$159 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R213.1, U207.2, U207.1 |
| N$160 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R213.2, R215.1, C223.1, R214.1 |
| N$161 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R215.2, C227.2, U207.6 |
| N$162 | 5 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C712.2, L702.1, C709.2, C706.1, L701.2 |
| N$164 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R721.2, R719.1, U704.4 |
| N$165 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R218.1, C226.1, R216.2, R217.1 |
| N$166 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C314.1, U305.4, R310.2 |
| N$167 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C314.2, U305.1, R309.2 |
| N$168 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C315.1, Y301.1, Y301.4, FB303.2 |
| N$169 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C317.2, U306.6, R312.2 |
| N$170 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C318.1, U306.5 |
| N$171 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R414.2, U401.6 |
| N$172 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R415.2, U401.5 |
| N$173 | 5 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C714.2, C712.1, L703.1, L702.2, C713.2 |
| N$174 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C715.1, U703.17 |
| N$175 | 4 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R715.1, C714.1, L703.2, C716.2 |
| N$176 | 4 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R715.2, R719.2, TP701.1, U704.1 |
| N$177 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R716.2, U704.6, C720.2 |
| N$178 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C719.2, U704.2, R717.1 |
| N$180 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C232.2, R218.2, U208.6 |
| N$181 | 5 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C224.1, R209.1, TP204.1, U204.6, U203.1 |
| N$182 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C224.2, U203.7, U204.2, U203.8 |
| N$46 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | K201.2, J201.1 |
| N$47 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | K201.8, U206.2 |
| N$48 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | K201.1, U206.3 |
| N$53 | 5 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | TP201.1, U203.3, R205.1, U201.6, U202.4 |
| N$54 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R210.1, C227.1, U207.7, R214.2 |
| N$55 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R210.2, R212.1, R211.1, C217.1 |
| N$56 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U201.2, U202.8 |
| N$57 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C310.2, U303.2, C313.2, R308.2, FB302.1 |
| N$58 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C301.2, U301.4 |
| N$59 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R301.2, U301.12 |
| N$60 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U301.1, C302.1 |
| N$61 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | K401.2, D405.2, J401.2 |
| N$62 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | K401.1, U401.2 |
| N$63 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | K401.8, U401.3 |
| N$64 | 2 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | K401.7, J401.1 |
| N$65 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | R401.1, C401.2, R402.1 |
| N$66 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | C710.1, U703.19 |
| N$67 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN701.3, U702.11 |
| N$68 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN701.1, U702.9 |
| N$69 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN701.4, U702.6 |
| N$70 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN701.2, U702.10 |
| N$71 | 3 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | R701.2, R702.1, U701.7 |
| N$72 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C202.2, D203.2, K201.3 |
| N$73 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C202.1, R201.2, R202.1 |
| N$74 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | D202.3, U205.3, TP207.1, R204.2 |
| N$75 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R220.2, R206.1, U202.12 |
| N$76 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | C320.2, U306.2, R313.2 |
| N$77 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | TP302.1, U303.5, R305.1, C304.2, C305.1 |
| N$78 | 2 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | R302.1, U301.10 |
| N$79 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U203.6, C207.1, U204.3, U203.5 |
| N$80 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U302.5, U301.3, C302.2, TP307.1, U302.6 |
| N$81 | 5 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U302.7, U302.8, C301.1, U301.2, TP306.1 |
| N$82 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U302.1, R302.2, R304.1 |
| N$83 | 3 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | U302.4, R303.1, R305.2 |
| N$84 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | D204.2, C206.2, K201.6 |
| N$85 | 4 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | D402.3, R408.1, R406.2, R403.2 |
| N$86 | 5 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U402.3, U402.5, TP401.1, D401.3, R402.2 |
| N$87 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U402.7, U402.6, R403.1 |
| N$88 | 3 | /c46f7bf0-b3e5-4206-aa8d-e6d0679b809b | U402.1, U402.2, R406.1 |
| N$89 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R205.2, R208.1, U202.5 |
| N$90 | 5 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U205.6, TP202.1, R206.2, U203.2, U202.13 |
| N$91 | 2 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | U205.2, U202.9 |
| N$92 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | C206.1, R204.1, R203.2 |
| N$93 | 4 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | TP206.1, D201.3, U201.3, R202.2 |
| N$94 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN702.1, U703.14 |
| N$95 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN702.2, U703.13 |
| N$96 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN702.4, U703.11 |
| N$97 | 2 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | RN702.3, U703.12 |
| N$98 | 5 | /69c97752-28d7-4ad3-888a-2beb501d4b85 | TP702.1, U701.1, U701.2, R704.1, U702.13 |
| N$99 | 3 | /2cbef686-8f02-4c5f-bcf6-217497882ee3 | R207.2, R220.1, U202.11 |
| VCM_2V5 | 4 | /843e73eb-7d0e-401b-9de9-9eb1eb874e61 | TP305.1, U304.4, U304.1, U301.9 |

## 3. 设计审查发现

### 警告（20）

| # | 位置 | 代码 | 说明 | 网络 |
| --- | --- | --- | --- | --- |
| 1 | `/` | ERC-lib_symbol_mismatch | 符号 'DRV8837' 与来源库 'Driver_Motor' 中的符号存在差异 |  |
| 2 | `/` | ERC-lib_symbol_mismatch | 符号 'DRV8837' 与来源库 'Driver_Motor' 中的符号存在差异 |  |
| 3 | `/` | ERC-lib_symbol_mismatch | 符号 'REF5050AD' 与来源库 'Reference_Voltage' 中的符号存在差异 |  |
| 4 | `/ / #PWR0109.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 5 | `/ / H104.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 6 | `/Analog Front End/ / #PWR0258.1` | ERC-multiple_net_names | GND 和 AFE_OUT_N 都连接到同一项上; 将使用 GND 作为网表中的网络名称 |  |
| 7 | `/Analog Front End/ / U201.4` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 8 | `/Analog Front End/ / U201.7` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 9 | `/Analog Front End/ / U206.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 10 | `/Analog Front End/ / U206.7` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 11 | `/Internal Reference Source/ / U701.4` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 12 | `/Internal Reference Source/ / U701.8` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 13 | `/Internal Reference Source/ / U704.2` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 14 | `/Internal Reference Source/ / U704.6` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 15 | `/Precision ADC Block/ / U301.5` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 16 | `/Precision ADC Block/ / U303.2` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 17 | `/Precision ADC Block/ / U303.3` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 18 | `/Precision ADC Block/ / U306.2` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 19 | `/Precision ADC Block/ / Y301.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |
| 20 | `/Reference Input Scheme/ / U404.5` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  |

### 提示（28）

| # | 位置 | 代码 | 说明 | 网络 |
| --- | --- | --- | --- | --- |
| 1 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / R221` | R701 | R221（0R）被标记为不焊接（DNP） |  |
| 2 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / TP201` | R701 | TP201（TP）被标记为不焊接（DNP） |  |
| 3 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / TP202` | R701 | TP202（TP）被标记为不焊接（DNP） |  |
| 4 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / TP203` | R701 | TP203（TP）被标记为不焊接（DNP） |  |
| 5 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / TP204` | R701 | TP204（TP）被标记为不焊接（DNP） |  |
| 6 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / TP205` | R701 | TP205（TP）被标记为不焊接（DNP） |  |
| 7 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / TP206` | R701 | TP206（TP）被标记为不焊接（DNP） |  |
| 8 | `/2cbef686-8f02-4c5f-bcf6-217497882ee3 / TP207` | R701 | TP207（TP）被标记为不焊接（DNP） |  |
| 9 | `/69c97752-28d7-4ad3-888a-2beb501d4b85 / TP701` | R701 | TP701（TP）被标记为不焊接（DNP） |  |
| 10 | `/69c97752-28d7-4ad3-888a-2beb501d4b85 / TP702` | R701 | TP702（TP）被标记为不焊接（DNP） |  |
| 11 | `/69c97752-28d7-4ad3-888a-2beb501d4b85 / TP703` | R701 | TP703（TP）被标记为不焊接（DNP） |  |
| 12 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / TP301` | R701 | TP301（TP）被标记为不焊接（DNP） |  |
| 13 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / TP302` | R701 | TP302（TP）被标记为不焊接（DNP） |  |
| 14 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / TP303` | R701 | TP303（TP）被标记为不焊接（DNP） |  |
| 15 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / TP304` | R701 | TP304（TP）被标记为不焊接（DNP） |  |
| 16 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / TP305` | R701 | TP305（TP）被标记为不焊接（DNP） |  |
| 17 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / TP306` | R701 | TP306（TP）被标记为不焊接（DNP） |  |
| 18 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / TP307` | R701 | TP307（TP）被标记为不焊接（DNP） |  |
| 19 | `/843e73eb-7d0e-401b-9de9-9eb1eb874e61 / U303.3` | R501 | U303.3（ADS127L11）的电源网络 N$117 上没有检测到电容；请核对是否已就近放置去耦电容 | N$117 |
| 20 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / C403` | R701 | C403（100pF）被标记为不焊接（DNP） |  |
| 21 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / C410` | R701 | C410（DNP）被标记为不焊接（DNP） |  |
| 22 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / R405` | R701 | R405（2k）被标记为不焊接（DNP） |  |
| 23 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / R410` | R701 | R410（100k）被标记为不焊接（DNP） |  |
| 24 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / R411` | R701 | R411（910k）被标记为不焊接（DNP） |  |
| 25 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / TP401` | R701 | TP401（TP）被标记为不焊接（DNP） |  |
| 26 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / TP402` | R701 | TP402（TP）被标记为不焊接（DNP） |  |
| 27 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / TP403` | R701 | TP403（TP）被标记为不焊接（DNP） |  |
| 28 | `/c46f7bf0-b3e5-4206-aa8d-e6d0679b809b / U405` | R701 | U405（74LVC1G08）被标记为不焊接（DNP） |  |

## 4. 工具与方法说明

- 网络表由纯 Python 几何连通域构建（导线端点 + 连接点 + 标签 + 电源符号），并完成分层图纸与全局标签合并。
- KiCad ERC 已运行: {'warning': 20}
- 悬空/单引脚等判定基于本工具解析结果；KiCad ERC 结果（如已运行）以 ERC-* 代码单独列出。
- 报告中的 info 级发现需要人工结合设计意图判断，不代表设计错误。
