# KiCad 原理图审查报告 — srb_v03.review

> 由 kicad-sch-reader 自动生成，根原理图：`D:\MyProjects\EmoeR_D\NIM\SuperResistanceBridge\SuperResistantBridge_MAIN_BRD_V0.3`

## 1. 工程概览

| 项目 | 值 |
| --- | --- |
| 图纸页数 | 12 |
| 元件符号数 | 1365 |
| 网络数 | 427（命名网络 201） |
| 已解析引脚连接数 | 2570 |
| 发现问题总数 | 265 |
| 问题分级 | error=40 / warning=174 / info=51 |
| KiCad ERC | errors=39, warnings=113 |

### 图纸清单

| 路径 | 文件 | 标题 | 元件 | 导线 | 标签 | 连接点 | NC | 版本/生成器 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `/` | `SuperResistantBridge_MAIN_BRD_V0.3.kicad_sch` |  | 109 | 229 | 70 | 16 | 15 | 20260306 / eeschema 10.0 |
| `/18f82026-7301-46f4-a5fb-c832a7fa5dde` | `analog_input_mux_array.kicad_sch` |  | 92 | 110 | 27 | 14 | 0 | 20260306 / eeschema 10.0 |
| `/32ec778c-7eba-4751-b4ef-324dd1b4de11` | `reference_brd_connector.kicad_sch` |  | 151 | 181 | 6 | 42 | 0 | 20260306 / eeschema 10.0 |
| `/484b9cec-0fcd-4b61-a421-fef2c149a552` | `precision_pgia.kicad_sch` |  | 77 | 91 | 5 | 19 | 0 | 20260306 / eeschema 10.0 |
| `/4b194535-7038-4ccf-881a-9da0ecfd7dd5` | `adc_channel_switch.kicad_sch` |  | 52 | 78 | 73 | 0 | 1 | 20260306 / eeschema 10.0 |
| `/54a3213f-6fa5-45cd-98cf-e5adff6b4b08` | `current_source.kicad_sch` |  | 134 | 194 | 12 | 46 | 5 | 20260306 / eeschema 10.0 |
| `/808ee41c-9861-4343-95d8-bf495bc90f75` | `analog_input_mux_array_without_cal.kicad_sch` |  | 78 | 93 | 20 | 11 | 0 | 20260306 / eeschema 10.0 |
| `/953a2742-667a-458f-ae96-334224d84db4` | `power_supply.kicad_sch` |  | 281 | 443 | 11 | 111 | 13 | 20260306 / eeschema 10.0 |
| `/c142b3aa-f761-44e5-bac6-1e851f77c5d9` | `adc_brd_connector.kicad_sch` |  | 45 | 130 | 29 | 25 | 5 | 20260306 / eeschema 10.0 |
| `/da12ad2c-a218-4f65-9f1a-c5abb68e5160` | `precision_pgia.kicad_sch` |  | 77 | 91 | 5 | 19 | 0 | 20260306 / eeschema 10.0 |
| `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a` | `controller_unit.kicad_sch` |  | 122 | 166 | 85 | 17 | 3 | 20260306 / eeschema 10.0 |
| `/e0d8101f-0eb7-4516-af8f-412fe166df93` | `reference_resistor.kicad_sch` |  | 147 | 145 | 77 | 15 | 12 | 20260306 / eeschema 10.0 |

## 2. 网络清单（按名称）

| 网络 | 引脚数 | 所在图纸 | 引脚示例 |
| --- | --- | --- | --- |
| +12VA | 20 | /953a2742-667a-458f-ae96-334224d84db4 | U702.20, U702.1, C705.1, C706.1, R705.1, C711.2, … |
| +15VA | 172 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde, /32ec778c-7eba-4751-b4ef-324dd1b4de11, /484b9cec-0fcd-4b61-a421-fef2c149a552 | U101.11, #PWR0106.1, U204.11, #PWR0243.1, U205.11, #PWR0244.1, … |
| +3.3V | 106 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde, /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | #PWR0104.1, R142.2, #PWR0259.1, R202.2, #PWR0836.1, U803.24, … |
| +5V5A | 19 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08, /953a2742-667a-458f-ae96-334224d84db4, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | C606.1, C608.2, U610.8, #PWR0610.1, #PWR0775.1, TP710.1, … |
| +6VA | 22 | /32ec778c-7eba-4751-b4ef-324dd1b4de11, /484b9cec-0fcd-4b61-a421-fef2c149a552, /953a2742-667a-458f-ae96-334224d84db4, /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | C1020.1, #PWR01030.1, #PWR01008.1, U1.6, #PWR01009.1, R1009.2, … |
| -15VA | 156 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde, /484b9cec-0fcd-4b61-a421-fef2c149a552, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U101.17, #PWR0103.1, U101.3, #PWR0105.1, U204.3, #PWR0242.1, … |
| -2V5 | 8 | /484b9cec-0fcd-4b61-a421-fef2c149a552, /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | C516.1, #PWR0535.1, U505.6, #PWR0515.1, C416.1, #PWR0435.1, … |
| -2V5A | 26 | /32ec778c-7eba-4751-b4ef-324dd1b4de11, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08, /953a2742-667a-458f-ae96-334224d84db4 | C1024.1, #PWR01048.1, #PWR01029.1, C1019.1, #PWR01042.1, U1009.4, … |
| /+5V_VOUT | 8 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | C1034.2, R1016.1, R1017.1, U1002.3, R1011.1, C1033.2, … |
| /100R_REF_EXC_SW | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1212.15, U1211.15, U1212.14 |
| /10R_REF_EXC_SW | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1206.14, U1211.17, U1206.15 |
| /10k_REF_EXC_SW | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1205.6, U1205.7, U1211.13 |
| /25mV_CAL | 9 | /32ec778c-7eba-4751-b4ef-324dd1b4de11, /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R1013.1, C1013.1, R1015.1, TP1011.1, U801.11, U802.11, … |
| /400R_REF_EXC_SW | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1212.7, U1211.14, U1212.6 |
| /40R_REF_EXC_SW | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1211.16, U1206.6, U1206.7 |
| /5V_VREF | 9 | /32ec778c-7eba-4751-b4ef-324dd1b4de11, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R1007.1, R1005.2, R1001.1, C1005.1, R620.2, C901.1, … |
| /ADC BRD/ADC_CS | 3 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R137.2, U901.14, J902.12 |
| /ADC BRD/ADC_IO1 | 2 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R101.2, J902.5 |
| /ADC BRD/ADC_IO10 | 2 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R129.2, J903.10 |
| /ADC BRD/ADC_IO11 | 1 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | J903.8 |
| /ADC BRD/ADC_IO12 | 2 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R131.2, J903.6 |
| /ADC BRD/ADC_IO2 | 2 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R104.2, J902.7 |
| /ADC BRD/ADC_IO3 | 2 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R107.2, J902.9 |
| /ADC BRD/ADC_IO4 | 2 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R109.2, J902.11 |
| /ADC BRD/ADC_IO5 | 1 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | J903.5 |
| /ADC BRD/ADC_IO6 | 1 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | J903.7 |
| /ADC BRD/ADC_IO7 | 1 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | J903.9 |
| /ADC BRD/ADC_IO8 | 1 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | J903.11 |
| /ADC BRD/ADC_IO9 | 1 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | J903.12 |
| /ADC BRD/ADC_MISO | 3 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R132.2, U901.12, J902.8 |
| /ADC BRD/ADC_MOSI | 3 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R136.2, U901.13, J902.10 |
| /ADC BRD/ADC_SCLK | 3 | /, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R134.2, J902.6, U901.11 |
| /ADC BRD/IN1_N | 7 | /484b9cec-0fcd-4b61-a421-fef2c149a552, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | C502.2, C504.2, R509.2, U506.1, J901.5, R905.2, … |
| /ADC BRD/IN1_P | 7 | /484b9cec-0fcd-4b61-a421-fef2c149a552, /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | U506.4, R510.1, C504.1, C505.2, J901.3, R904.1, … |
| /ADC BRD/IN2_N | 7 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9, /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | J901.9, R903.2, TP904.1, C402.2, C404.2, R409.2, … |
| /ADC BRD/IN2_P | 7 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9, /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | J901.7, TP903.1, R902.1, U406.4, R410.1, C404.1, … |
| /ADC Channel Switch/MUX_RESET | 2 | /, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R128.2, U803.3 |
| /ADC Channel Switch/MUX_SCL1 | 2 | /, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R120.2, U803.22 |
| /ADC Channel Switch/MUX_SDA1 | 2 | /, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R124.2, U803.23 |
| /ADC Channel Switch/PGIA_IN1+_CH1 | 4 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R114.1, U205.8, U205.2, U801.4 |
| /ADC Channel Switch/PGIA_IN1+_CH2 | 3 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /808ee41c-9861-4343-95d8-bf495bc90f75 | U801.5, U303.2, U303.8 |
| /ADC Channel Switch/PGIA_IN1+_CH3 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | J206.4, U801.6 |
| /ADC Channel Switch/PGIA_IN1+_CH4 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /808ee41c-9861-4343-95d8-bf495bc90f75 | U801.7, J306.4 |
| /ADC Channel Switch/PGIA_IN1-_CH1 | 4 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R117.1, U205.10, U205.16, U804.4 |
| /ADC Channel Switch/PGIA_IN1-_CH2 | 3 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /808ee41c-9861-4343-95d8-bf495bc90f75 | U804.5, U303.16, U303.10 |
| /ADC Channel Switch/PGIA_IN1-_CH3 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | J206.1, U804.6 |
| /ADC Channel Switch/PGIA_IN1-_CH4 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /808ee41c-9861-4343-95d8-bf495bc90f75 | U804.7, J306.1 |
| /ADC Channel Switch/PGIA_IN1_+ | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R501.1, R502.1, U801.8 |
| /ADC Channel Switch/PGIA_IN1_- | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R504.1, R503.1, U804.8 |
| /ADC Channel Switch/PGIA_IN2+_CH1 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U802.4, U1201.8 |
| /ADC Channel Switch/PGIA_IN2+_CH2 | 1 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U802.5 |
| /ADC Channel Switch/PGIA_IN2+_CH3 | 1 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U802.6 |
| /ADC Channel Switch/PGIA_IN2+_CH4 | 2 | /, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R114.2, U802.7 |
| /ADC Channel Switch/PGIA_IN2-_CH1 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U805.4, U1202.8 |
| /ADC Channel Switch/PGIA_IN2-_CH2 | 1 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U805.5 |
| /ADC Channel Switch/PGIA_IN2-_CH3 | 1 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U805.6 |
| /ADC Channel Switch/PGIA_IN2-_CH4 | 2 | /, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R117.2, U805.7 |
| /ADC Channel Switch/PGIA_IN2_+ | 3 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | U802.8, R401.1, R402.1 |
| /ADC Channel Switch/PGIA_IN2_- | 3 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | U805.8, R404.1, R403.1 |
| /Analog Input MUX Array CH2/CURR_IO_A | 2 | /, /808ee41c-9861-4343-95d8-bf495bc90f75 | U101.2, U301.16 |
| /Analog Input MUX Array CH2/CURR_IO_B | 2 | /, /808ee41c-9861-4343-95d8-bf495bc90f75 | U101.10, U301.10 |
| /Analog Input MUX Array CH2/INPUT_MUX_AR_EN | 4 | /, /808ee41c-9861-4343-95d8-bf495bc90f75 | R141.2, U301.12, U303.12, U302.12 |
| /Analog Input MUX Array CH2/IN_MUX_CURR_SW | 3 | /, /808ee41c-9861-4343-95d8-bf495bc90f75 | R140.2, U301.6, U301.15 |
| /Analog Input MUX Array CH2/IN_MUX_DUTSW | 3 | /, /808ee41c-9861-4343-95d8-bf495bc90f75 | R139.2, U302.6, U302.15 |
| /Analog Input MUX Array CH2/IN_MUX_VOLT_SW | 3 | /, /808ee41c-9861-4343-95d8-bf495bc90f75 | R138.2, U303.15, U303.6 |
| /Analog Input MUX Array CH2/MEAS_MODE_SEL | 3 | /, /808ee41c-9861-4343-95d8-bf495bc90f75 | R106.2, R302.2, Q301.1 |
| /Analog Input MUX Array/CURR_IO_A | 2 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde | U101.16, U203.8 |
| /Analog Input MUX Array/CURR_IO_B | 2 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde | U101.8, U203.2 |
| /Analog Input MUX Array/INPUT_MUX_AR_EN | 5 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde | R122.2, U204.12, U205.12, U203.12, U201.12 |
| /Analog Input MUX Array/IN_MUX_CALSW | 3 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde | R113.2, U201.6, U201.15 |
| /Analog Input MUX Array/IN_MUX_CURR_SW | 3 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde | R110.2, U203.6, U203.15 |
| /Analog Input MUX Array/IN_MUX_DUTSW | 3 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde | R118.2, U204.6, U204.15 |
| /Analog Input MUX Array/IN_MUX_VOLT_SW | 3 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde | R126.2, U205.6, U205.15 |
| /Analog Input MUX Array/MEAS_MODE_SEL | 3 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde | R103.2, R203.2, Q201.1 |
| /Analog Input MUX Array/REF_RES1_A | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U201.16, U1213.2 |
| /Analog Input MUX Array/REF_RES1_B | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U201.8, U1213.10 |
| /Analog Input MUX Array/REF_RES2_A | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U201.2, U1214.2 |
| /Analog Input MUX Array/REF_RES2_B | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U201.10, U1214.10 |
| /CURR_CHANNEL_SW | 3 | / | U101.6, R150.2, U101.15 |
| /CURR_GUARD | 1 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R601.2 |
| /Controller Unit/PD1 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R112.1, U1102.82 |
| /Controller Unit/PD2 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R144.1, U1102.83 |
| /Controller Unit/PD3 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R143.1, U1102.84 |
| /Controller Unit/PE10 | 1 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.40 |
| /Controller Unit/PE9 | 1 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.39 |
| /Controller Unit/SPI1_SCK | 1 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.29 |
| /Controller Unit/SPI3_CS | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R146.1, U1102.79 |
| /Controller Unit/SPI3_LDAC | 1 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.81 |
| /Controller Unit/SPI3_MOSI | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R147.1, U1102.80 |
| /Controller Unit/SPI3_SCK | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R148.1, U1102.78 |
| /EXT_REF_EXC_SW | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1205.15, U1205.14, U1211.20 |
| /I2C1_SCL | 4 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R105.1, R120.1, R1116.1, U1102.92 |
| /I2C1_SDA | 4 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R124.1, R108.1, R1117.1, U1102.93 |
| /I2C3_SCL | 3 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1108.1, U1103.6, U1102.67 |
| /I2C3_SDA | 3 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1103.5, R1109.1, U1102.66 |
| /I2C4_SCL | 5 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1111.1, U1104.4, U1104.1, J1105.9, U1102.59 |
| /I2C4_SDA | 4 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.60, R1110.1, U1104.6, J1105.8 |
| /INT_CAL_100R | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1211.9, U1213.6, U1213.15 |
| /INT_CAL_10R | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1214.6, U1214.15, U1211.8 |
| /Internal Reference Resistor/CURR_DIR_SW | 3 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | R102.2, U1203.6, U1204.6 |
| /Internal Reference Resistor/CURR_IO_A | 2 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U101.1, U1204.8 |
| /Internal Reference Resistor/CURR_IO_B | 2 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U101.9, U1203.10 |
| /Internal Reference Resistor/MUX_RESET | 2 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | R111.2, U1211.3 |
| /Internal Reference Resistor/MUX_SCL1 | 3 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | R105.2, U1211.22, U1209.1 |
| /Internal Reference Resistor/MUX_SDA1 | 3 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | R108.2, U1211.23, U1209.6 |
| /LPUART1_RX | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1106.4, U1102.69 |
| /LPUART1_TX | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1106.6, U1102.68 |
| /NRST | 5 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | C1106.2, U1102.14, R1103.1, J1104.3, SW1101.2 |
| /PB0 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | J1105.4, U1102.34 |
| /PB1 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | J1105.5, U1102.35 |
| /PB2 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | J1105.6, U1102.36 |
| /PB3 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R101.1, U1102.89 |
| /PB5 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R115.1, U1102.91 |
| /PB8 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R113.1, U1102.95 |
| /PB9 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R110.1, U1102.96 |
| /PC13 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1113.2, U1102.7 |
| /PC14 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.8, R1114.2 |
| /PC15 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.9, R1115.2 |
| /PC4 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.32, J1105.7 |
| /PC8 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1103.7, U1102.65 |
| /PD10 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R107.1, U1102.57 |
| /PD11 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R109.1, U1102.58 |
| /PD8 | 1 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.55 |
| /PD9 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R104.1, U1102.56 |
| /PE0 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R126.1, U1102.97 |
| /PE1 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R122.1, U1102.98 |
| /PE11 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R150.1, U1102.41 |
| /PE12 | 1 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.42 |
| /PE13 | 1 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.43 |
| /PE14 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R102.1, U1102.44 |
| /PE15 | 3 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R128.1, R111.1, U1102.45 |
| /PE2 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R118.1, U1102.1 |
| /PE3 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R141.1, U1102.2 |
| /PE4 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R140.1, U1102.3 |
| /PE5 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R139.1, U1102.4 |
| /PE6 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R138.1, U1102.5 |
| /PE7 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R106.1, U1102.37 |
| /PE8 | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R103.1, U1102.38 |
| /PGIA1_NMUX_A0 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U803.8, U804.1 |
| /PGIA1_NMUX_A1 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U803.9, U804.16 |
| /PGIA1_NMUX_A2 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U803.10, U804.15 |
| /PGIA1_NMUX_EN | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U803.11, U804.2 |
| /PGIA1_PMUX_A0 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U801.1, U803.4 |
| /PGIA1_PMUX_A1 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U801.16, U803.5 |
| /PGIA1_PMUX_A2 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U801.15, U803.6 |
| /PGIA1_PMUX_EN | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U801.2, U803.7 |
| /PGIA2_NMUX_A0 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U805.1, U803.17 |
| /PGIA2_NMUX_A1 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U803.18, U805.16 |
| /PGIA2_NMUX_A2 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U803.19, U805.15 |
| /PGIA2_NMUX_EN | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U805.2, U803.20 |
| /PGIA2_PMUX_A0 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U803.13, U802.1 |
| /PGIA2_PMUX_A1 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U802.16, U803.14 |
| /PGIA2_PMUX_A2 | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U802.15, U803.15 |
| /PGIA2_PMUX_EN | 2 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | U803.16, U802.2 |
| /REF_RES_100R_A | 4 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1201.10, U1213.1, U1212.16, R1203.1 |
| /REF_RES_100R_B | 4 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1212.13, R1203.2, U1213.9, U1202.10 |
| /REF_RES_10R_A | 4 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | R1201.1, U1206.16, U1214.1, U1201.12 |
| /REF_RES_10R_B | 4 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | R1201.2, U1206.13, U1214.9, U1202.12 |
| /REF_RES_10k_A | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1201.6, R1205.1, U1205.8 |
| /REF_RES_10k_B | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | R1205.2, U1205.5, U1202.6 |
| /REF_RES_400R_A | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | R1204.1, U1212.8, U1201.9 |
| /REF_RES_400R_B | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | R1204.2, U1212.5, U1202.9 |
| /REF_RES_40R_A | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1206.8, R1202.1, U1201.11 |
| /REF_RES_40R_B | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1206.5, R1202.2, U1202.11 |
| /REF_RES_MUX_A0 | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1201.1, U1202.1, U1211.4 |
| /REF_RES_MUX_A1 | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1211.5, U1201.16, U1202.16 |
| /REF_RES_MUX_A2 | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1211.6, U1201.15, U1202.15 |
| /REF_RES_MUX_EN | 5 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1201.2, U1202.2, U1203.12, U1204.12, U1211.11 |
| /RES_RES_CAL_EN | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1211.10, U1214.12, U1213.12 |
| /Reference BRD/250mV_CAL | 9 | /32ec778c-7eba-4751-b4ef-324dd1b4de11, /4b194535-7038-4ccf-881a-9da0ecfd7dd5 | R1010.1, TP1006.1, U1008.8, R1008.1, C1006.1, U802.12, … |
| /Reference BRD/2V5_VCM | 8 | /32ec778c-7eba-4751-b4ef-324dd1b4de11, /484b9cec-0fcd-4b61-a421-fef2c149a552, /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R1003.1, R1006.1, TP1003.1, C1001.1, C501.1, U505.2, … |
| /SPI1_MISO | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R129.1, U1102.30 |
| /SPI2_CS | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R137.1, U1102.51 |
| /SPI2_MISO | 3 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R132.1, R131.1, U1102.53 |
| /SPI2_MOSI | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R136.1, U1102.54 |
| /SPI2_SCK | 2 | /, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R134.1, U1102.52 |
| /SWCLK | 3 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | J1102.3, J1104.4, U1102.76 |
| /SWDIO | 3 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | J1104.2, U1102.72, J1102.2 |
| /USB_DM | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1101.6, U1102.70 |
| /USB_DP | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.71, U1101.4 |
| /VDACO | 7 | /4b194535-7038-4ccf-881a-9da0ecfd7dd5, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U802.9, U805.9, U801.9, U804.9, R621.1, U607.5, … |
| /VREG1A | 3 | /953a2742-667a-458f-ae96-334224d84db4 | U703.4, C714.1, U703.14 |
| /VREG1B | 3 | /953a2742-667a-458f-ae96-334224d84db4 | U710.4, C757.1, U710.14 |
| /Voltage Controlled Current Source/CURR_REF_SW | 3 | /, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R143.2, U609.15, U609.6 |
| /Voltage Controlled Current Source/CURR_SRC_PWR_SW | 3 | /, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R115.2, R622.2, Q610.1 |
| /Voltage Controlled Current Source/DAC_CAL_SW | 3 | /, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R112.2, R608.2, Q603.1 |
| /Voltage Controlled Current Source/DAC_CS | 2 | /, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R146.2, U610.4 |
| /Voltage Controlled Current Source/DAC_MOSI | 2 | /, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R147.2, U610.6 |
| /Voltage Controlled Current Source/DAC_SCLK | 2 | /, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R148.2, U610.5 |
| /Voltage Controlled Current Source/compliance | 5 | /, /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R144.2, R603.1, U602.1, R605.2, TP602.1 |
| /~{EXT_REF_EXC_SW} | 3 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1204.15, U1203.15, U1211.19 |
| CLK_1.2M | 2 | /953a2742-667a-458f-ae96-334224d84db4 | R737.2, R735.2 |
| CLK_2.4M | 8 | /953a2742-667a-458f-ae96-334224d84db4 | R736.2, R716.1, U707.1, TP709.1, R712.2, U703.2, … |
| CLK_24M | 4 | /953a2742-667a-458f-ae96-334224d84db4, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U712.4, TP716.1, R1105.2, U1102.12 |
| CURR_SRC_EXC | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08, /e0d8101f-0eb7-4516-af8f-412fe166df93 | U604.4, U1204.10, U1203.8 |
| EXT_REF_SENSE1 | 4 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | C101.1, FB101.2, D104.2, U1201.4 |
| EXT_REF_SENSE2 | 4 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | C102.1, FB102.2, D103.2, U1202.4 |
| EXT_REF_TERM_1 | 4 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | FB103.2, D101.2, C103.1, U1205.16 |
| EXT_REF_TERM_2 | 4 | /, /e0d8101f-0eb7-4516-af8f-412fe166df93 | D102.2, FB104.2, C104.1, U1205.13 |
| GND | 819 | /, /18f82026-7301-46f4-a5fb-c832a7fa5dde, /32ec778c-7eba-4751-b4ef-324dd1b4de11, /484b9cec-0fcd-4b61-a421-fef2c149a552 | #PWR0107.1, R116.1, C105.2, #PWR0101.1, U101.4, #PWR0116.1, … |
| N$10 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1001.1, U1001.2 |
| N$103 | 6 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1204.16, U1205.4, U1206.12, U1206.4, U1212.12, U1212.4 |
| N$104 | 2 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1204.1, U1204.9 |
| N$105 | 2 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1204.2, U1205.12 |
| N$107 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | C1025.2, U1003.5 |
| N$11 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | C1002.2, R1002.1 |
| N$114 | 4 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | FB201.1, C201.1, D201.2, U204.2 |
| N$115 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | FB201.2, J201.1 |
| N$118 | 2 | / | J102.1, FB102.1 |
| N$119 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | Q201.3, U206.1 |
| N$129 | 2 | / | FB103.1, J103.1 |
| N$13 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | C1030.2, U1005.6, R1014.2 |
| N$130 | 4 | /808ee41c-9861-4343-95d8-bf495bc90f75 | D301.2, U302.2, FB301.1, C301.1 |
| N$131 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | J301.1, FB301.2 |
| N$134 | 2 | / | FB104.1, J104.1 |
| N$139 | 3 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R410.2, U405.4, C406.1 |
| N$140 | 2 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R401.2, U401.3 |
| N$145 | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R510.2, U505.4, C506.1 |
| N$146 | 2 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R501.2, U501.3 |
| N$147 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | C601.1, U601.6, R602.1 |
| N$148 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | C601.2, U601.2, R604.2 |
| N$149 | 3 | / | H106.1, R116.2, C105.1 |
| N$15 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1003.2, C1003.1, U1002.7 |
| N$150 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | L601.2, C605.2, D603.2 |
| N$151 | 4 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | TP610.1, U609.16, U609.8, R618.1 |
| N$152 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | Q601.3, D602.2, R610.1 |
| N$153 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | Q601.1, R611.2, D604.1 |
| N$156 | 5 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R601.1, TP604.1, U606.6, U606.7, R606.1 |
| N$158 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U601.3, R620.1 |
| N$159 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | FB710.1, C752.2, C702.2, L706.2 |
| N$16 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1004.6, R1011.2, C1027.2 |
| N$160 | 5 | /953a2742-667a-458f-ae96-334224d84db4 | D701.1, C713.2, R706.2, L708.1, C712.2 |
| N$161 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | L701.2, D701.2, U703.20 |
| N$162 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | L701.1, U703.1 |
| N$17 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1004.5, C1028.2 |
| N$177 | 2 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | U901.4, C906.1 |
| N$178 | 2 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | U901.9, R906.1 |
| N$179 | 2 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | U901.2, R903.1 |
| N$18 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1005.1, U1.4, R1002.2 |
| N$180 | 2 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | U901.3, C906.2 |
| N$181 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | FB202.1, J202.1 |
| N$182 | 3 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | R202.1, R203.1, Q201.2 |
| N$183 | 4 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | C203.1, D202.2, FB203.1, U205.1 |
| N$184 | 4 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | D203.2, FB202.2, U204.10, C202.1 |
| N$185 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | J203.1, FB203.2 |
| N$186 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | J302.1, FB302.1 |
| N$187 | 3 | /808ee41c-9861-4343-95d8-bf495bc90f75 | R302.1, Q301.2, R303.1 |
| N$188 | 3 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | U203.1, U201.9, U204.9 |
| N$189 | 4 | /808ee41c-9861-4343-95d8-bf495bc90f75 | U302.10, C302.1, FB302.2, D303.2 |
| N$19 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1005.5, C1031.2 |
| N$190 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | U302.8, J306.2 |
| N$191 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | U302.16, J306.3 |
| N$192 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | U302.1, U301.1 |
| N$193 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | U302.9, U301.9 |
| N$194 | 5 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | FB204.2, C204.1, U205.9, D204.2, U206.4 |
| N$195 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | FB204.1, J204.1 |
| N$196 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | U204.8, J206.2 |
| N$197 | 3 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | U204.1, U201.1, U203.9 |
| N$198 | 2 | /18f82026-7301-46f4-a5fb-c832a7fa5dde | U204.16, J206.3 |
| N$199 | 2 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | U402.3, R403.2 |
| N$20 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1006.2, C1003.2, U1002.6 |
| N$200 | 3 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | U402.6, U402.2, R407.1 |
| N$202 | 2 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | U502.3, R503.2 |
| N$203 | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | U502.6, U502.2, R507.1 |
| N$204 | 5 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | C602.1, R604.1, R602.2, C603.1, U610.3 |
| N$207 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | Q602.3, U606.3, U605.1 |
| N$208 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | Q602.1, R612.2 |
| N$209 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | Q602.2, U609.1 |
| N$21 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1006.7, U1006.8, R1018.1 |
| N$210 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U602.3, R606.2, R605.1 |
| N$211 | 4 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U602.2, R607.2, D601.1, U602.6 |
| N$212 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | L702.2, D702.1, U703.18 |
| N$213 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R720.1, U707.5, R718.2 |
| N$215 | 6 | /953a2742-667a-458f-ae96-334224d84db4 | U702.13, U702.15, U702.16, TP703.1, FB703.2, C710.2 |
| N$216 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | U702.14, C715.2 |
| N$217 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | U702.3, R705.2, C711.1, R708.1 |
| N$22 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1006.4, U1006.2 |
| N$225 | 4 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | C902.1, FB901.1, Y901.1, Y901.4 |
| N$226 | 2 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R902.2, U901.1 |
| N$227 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | J303.1, FB303.2 |
| N$228 | 4 | /808ee41c-9861-4343-95d8-bf495bc90f75 | U303.1, C303.1, FB303.1, D302.2 |
| N$229 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | FB304.1, J304.1 |
| N$230 | 5 | /808ee41c-9861-4343-95d8-bf495bc90f75 | U304.4, C304.1, D304.2, FB304.2, U303.9 |
| N$231 | 2 | /808ee41c-9861-4343-95d8-bf495bc90f75 | U304.1, Q301.3 |
| N$232 | 2 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | U403.3, R402.2 |
| N$233 | 2 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | U503.3, R502.2 |
| N$234 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | TP603.1, U607.3, U610.1 |
| N$235 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | Q603.3, U603.1 |
| N$236 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | C703.2, C709.2, L708.2, FB703.1 |
| N$237 | 5 | /953a2742-667a-458f-ae96-334224d84db4 | D703.1, C755.2, C756.2, L706.1, R726.2 |
| N$238 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | L703.2, U707.9 |
| N$239 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | L703.1, U707.11 |
| N$24 | 4 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1007.2, R1012.1, U1.1, C1002.1 |
| N$240 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R730.1, R731.1, U710.11 |
| N$242 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | U703.6, R703.2 |
| N$25 | 4 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1008.6, U1007.5, C1012.1, U1008.5 |
| N$257 | 2 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R404.2, U404.3 |
| N$259 | 2 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R504.2, U504.3 |
| N$26 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1008.3, U1008.2 |
| N$260 | 3 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R405.1, U401.6, U401.2 |
| N$261 | 2 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | U405.7, R411.1 |
| N$262 | 3 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R406.2, U406.2, R405.2 |
| N$263 | 3 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R406.1, U403.6, U403.2 |
| N$265 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U604.1, Q610.3 |
| N$266 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U604.3, D602.1 |
| N$267 | 4 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | U406.5, U406.6, U405.1, C406.2 |
| N$268 | 4 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | U406.7, C403.2, U405.8, U406.8 |
| N$269 | 5 | /953a2742-667a-458f-ae96-334224d84db4 | C740.1, U706.1, U706.2, FB708.1, R715.1 |
| N$27 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1008.1, U1008.4 |
| N$270 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | L704.2, D703.2, U710.20 |
| N$271 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | L704.1, U710.1 |
| N$272 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R704.1, U703.7, U703.9 |
| N$273 | 8 | /953a2742-667a-458f-ae96-334224d84db4 | U704.5, U704.13, U704.1, U704.3, U704.2, TP704.1, … |
| N$274 | 5 | /953a2742-667a-458f-ae96-334224d84db4 | U704.12, U704.10, U704.11, FB705.1, C727.2 |
| N$275 | 3 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R408.1, U404.6, U404.2 |
| N$276 | 3 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R408.2, U406.3, R407.2 |
| N$279 | 2 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R904.2, U901.20 |
| N$28 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | C1009.1, U1007.1, R1008.2 |
| N$280 | 3 | /da12ad2c-a218-4f65-9f1a-c5abb68e5160 | R409.1, C403.1, U405.5 |
| N$281 | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R505.1, U501.6, U501.2 |
| N$282 | 2 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | U505.7, R511.1 |
| N$283 | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R506.2, U506.2, R505.2 |
| N$284 | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R506.1, U503.6, U503.2 |
| N$286 | 4 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | U506.5, U506.6, U505.1, C506.2 |
| N$287 | 4 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | U506.7, C503.2, U505.8, U506.8 |
| N$288 | 6 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U605.7, U605.6, C604.2, L601.1, U605.8, TP601.1 |
| N$289 | 5 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U605.2, Q601.2, U605.3, R609.2, TP605.1 |
| N$29 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1009.3, R1004.1 |
| N$290 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | C750.2, R723.1 |
| N$291 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | L705.2, D704.1, U710.18 |
| N$292 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | U705.10, U705.9, FB706.1, C735.2 |
| N$293 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | U705.7, R714.1, C736.2 |
| N$294 | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R508.1, U504.6, U504.2 |
| N$295 | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R508.2, U506.3, R507.2 |
| N$30 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1009.2, R1001.2, C1007.2 |
| N$302 | 5 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | C905.1, U901.15, FB901.2, C903.1, U902.5 |
| N$303 | 3 | /484b9cec-0fcd-4b61-a421-fef2c149a552 | R509.1, C503.1, U505.5 |
| N$304 | 2 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R905.1, U901.19 |
| N$306 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U606.5, R610.2 |
| N$307 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U606.1, D604.2, C610.2 |
| N$308 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | C760.1, R730.2, U710.12 |
| N$309 | 4 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U607.7, TP607.1, R612.1, C611.2 |
| N$31 | 3 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | FB1101.2, C1101.1, Y1101.4 |
| N$310 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U607.6, R616.1, C611.1 |
| N$311 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | U706.3, R721.1, R715.2 |
| N$312 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R608.1, Q603.2, R613.1 |
| N$313 | 5 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U608.6, U608.7, U608.8, C612.1, U607.2 |
| N$314 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U608.4, U608.3, U608.2 |
| N$315 | 5 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U608.5, TP606.1, C612.2, U607.1, U603.3 |
| N$316 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R609.1, U606.2, C610.1 |
| N$317 | 2 | /c142b3aa-f761-44e5-bac6-1e851f77c5d9 | R906.2, Y901.3 |
| N$318 | 4 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U609.2, U609.10, TP609.1, R617.1 |
| N$319 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | U609.12, R619.1 |
| N$32 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | J1101.2, R1104.2 |
| N$320 | 5 | /953a2742-667a-458f-ae96-334224d84db4 | FB707.2, C739.1, U706.5, U706.8, U706.7 |
| N$321 | 8 | /953a2742-667a-458f-ae96-334224d84db4 | FB707.1, C738.1, R719.1, C732.2, U707.7-8, TP707.1, … |
| N$322 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | C707.2, R703.1 |
| N$323 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R707.2, R706.1, U703.5 |
| N$324 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | U707.3, C743.1 |
| N$325 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | L709.2, C704.2, C721.2, FB704.1 |
| N$326 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | R709.2, U703.10 |
| N$327 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | U709.3, R728.1, R725.2, C754.1 |
| N$328 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | U709.14, C758.2 |
| N$33 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1101.1, Y1101.1 |
| N$332 | 2 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1211.2, R1206.1 |
| N$336 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1113.1, D1101.2 |
| N$338 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1114.1, D1102.2 |
| N$339 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | C1116.1, U1102.48 |
| N$340 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | C1117.1, U1102.73 |
| N$35 | 3 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | C1102.2, J1101.1, U1101.5 |
| N$359 | 5 | /953a2742-667a-458f-ae96-334224d84db4 | R711.2, C719.2, C720.2, L709.1, D702.2 |
| N$360 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R711.1, U703.11, R710.1 |
| N$361 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | U711.3, R733.1, R732.2, C771.1 |
| N$362 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | U711.14, C772.2 |
| N$37 | 4 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1012.2, U1009.6, U1.3, C1007.1 |
| N$373 | 6 | /953a2742-667a-458f-ae96-334224d84db4 | TP712.1, U709.13, U709.15, U709.16, FB710.2, C753.2 |
| N$374 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | U712.1, U712.7 |
| N$375 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | U712.13, R735.1 |
| N$38 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1102.1, U1101.3 |
| N$387 | 6 | /953a2742-667a-458f-ae96-334224d84db4 | TP713.1, FB701.2, U711.16, U711.13, U711.15, C767.2 |
| N$39 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1102.2, J1101.3 |
| N$390 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R713.1, U704.8, C728.2 |
| N$4 | 5 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | C1010.1, U1006.6, U1007.3, U1006.5, R1018.2 |
| N$404 | 2 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R616.2, U609.9 |
| N$405 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | C716.2, R709.1 |
| N$406 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | C717.1, U703.12, R710.2 |
| N$407 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | R717.2, U707.14 |
| N$408 | 6 | /953a2742-667a-458f-ae96-334224d84db4 | R717.1, R716.2, FB711.2, C730.2, U707.12-13, C731.2 |
| N$409 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | R719.2, U707.2 |
| N$410 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1.5, R1009.1 |
| N$411 | 3 | /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 | R622.1, R623.1, Q610.2 |
| N$412 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | R723.2, U710.6 |
| N$413 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | C742.1, U706.6 |
| N$414 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R724.1, U710.7, U710.9 |
| N$415 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R727.2, U710.5, R726.1 |
| N$416 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | R729.2, U710.10 |
| N$417 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U2.5, C1008.2 |
| N$418 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R734.2, U712.2, U712.14 |
| N$419 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | R736.1, U712.3, U712.15 |
| N$422 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | R738.1, D705.2 |
| N$423 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | C746.2, FB709.1, U708.10, U708.9 |
| N$424 | 3 | /953a2742-667a-458f-ae96-334224d84db4 | C747.2, R722.1, U708.7 |
| N$425 | 5 | /953a2742-667a-458f-ae96-334224d84db4 | C765.2, C764.2, R731.2, D704.2, L707.1 |
| N$426 | 2 | /953a2742-667a-458f-ae96-334224d84db4 | C759.2, R729.1 |
| N$427 | 4 | /953a2742-667a-458f-ae96-334224d84db4 | C766.2, C701.2, FB701.1, L707.2 |
| N$47 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1102.20, R1107.1 |
| N$5 | 6 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | TP1001.1, U1001.8, U1002.2, U1002.1, R1004.2, U1006.1 |
| N$59 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | D1103.2, R1115.1 |
| N$61 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1013.2, C1014.1, U1007.7 |
| N$64 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | C1014.2, R1015.2, U1007.6 |
| N$66 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1104.1, U1101.1 |
| N$7 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1010.2, C1009.2, U1007.2 |
| N$70 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1105.2, Y1101.3 |
| N$71 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1105.4, R1105.1 |
| N$73 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1016.2, C1023.2, U1003.6 |
| N$74 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | R1106.2, U1102.94 |
| N$77 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1106.3, J1103.3 |
| N$78 | 2 | /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | U1106.1, J1103.2 |
| N$79 | 3 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | R1017.2, U2.6, C1011.2 |
| N$8 | 2 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1001.4, U1001.3 |
| N$81 | 2 | / | FB101.1, J101.1 |
| N$9 | 4 | /32ec778c-7eba-4751-b4ef-324dd1b4de11 | U1001.6, U1001.7, C1004.1, U1002.5 |
| N$96 | 2 | / | U101.12, R142.1 |
| N$97 | 6 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1203.16, U1205.9, U1206.1, U1212.9, U1212.1, U1206.9 |
| N$98 | 2 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1203.1, U1203.9 |
| N$99 | 2 | /e0d8101f-0eb7-4516-af8f-412fe166df93 | U1203.2, U1205.1 |
| VBUS | 26 | /953a2742-667a-458f-ae96-334224d84db4, /db7d6b1f-9df6-4919-b552-4c0b97a52f9a | #PWR0874.1, J701.2, #PWR0789.1, U710.17, U710.16, U710.15, … |

## 3. 设计审查发现

### 错误（40）

| # | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` | R401 | 网络被命名为多个全局网络: GND, GNDA；当前工具暂按 'GND' 归并，请用 KiCad ERC 复核 | GND | structural |
| 2 | `/` | ERC-pin_not_connected | Pin not connected |  | official |
| 3 | `/` | ERC-pin_not_connected | Pin not connected |  | official |
| 4 | `/` | ERC-pin_not_connected | Pin not connected |  | official |
| 5 | `/` | ERC-pin_not_connected | Pin not connected |  | official |
| 6 | `/` | ERC-pin_not_connected | Pin not connected |  | official |
| 7 | `/` | ERC-pin_not_connected | Pin not connected |  | official |
| 8 | `/` | ERC-pin_not_connected | Pin not connected |  | official |
| 9 | `/ADC BRD/ / Y901.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 10 | `/Controller Unit/ / U1102.15` | ERC-pin_not_connected | Pin not connected |  | official |
| 11 | `/Controller Unit/ / U1102.16` | ERC-pin_not_connected | Pin not connected |  | official |
| 12 | `/Controller Unit/ / U1102.17` | ERC-pin_not_connected | Pin not connected |  | official |
| 13 | `/Controller Unit/ / U1102.18` | ERC-pin_not_connected | Pin not connected |  | official |
| 14 | `/Controller Unit/ / U1102.22` | ERC-pin_not_connected | Pin not connected |  | official |
| 15 | `/Controller Unit/ / U1102.23` | ERC-pin_not_connected | Pin not connected |  | official |
| 16 | `/Controller Unit/ / U1102.24` | ERC-pin_not_connected | Pin not connected |  | official |
| 17 | `/Controller Unit/ / U1102.25` | ERC-pin_not_connected | Pin not connected |  | official |
| 18 | `/Controller Unit/ / U1102.28` | ERC-pin_not_connected | Pin not connected |  | official |
| 19 | `/Controller Unit/ / U1102.31` | ERC-pin_not_connected | Pin not connected |  | official |
| 20 | `/Controller Unit/ / U1102.33` | ERC-pin_not_connected | Pin not connected |  | official |
| 21 | `/Controller Unit/ / U1102.46` | ERC-pin_not_connected | Pin not connected |  | official |
| 22 | `/Controller Unit/ / U1102.47` | ERC-pin_not_connected | Pin not connected |  | official |
| 23 | `/Controller Unit/ / U1102.61` | ERC-pin_not_connected | Pin not connected |  | official |
| 24 | `/Controller Unit/ / U1102.62` | ERC-pin_not_connected | Pin not connected |  | official |
| 25 | `/Controller Unit/ / U1102.63` | ERC-pin_not_connected | Pin not connected |  | official |
| 26 | `/Controller Unit/ / U1102.64` | ERC-pin_not_connected | Pin not connected |  | official |
| 27 | `/Controller Unit/ / U1102.77` | ERC-pin_not_connected | Pin not connected |  | official |
| 28 | `/Controller Unit/ / U1102.85` | ERC-pin_not_connected | Pin not connected |  | official |
| 29 | `/Controller Unit/ / U1102.86` | ERC-pin_not_connected | Pin not connected |  | official |
| 30 | `/Controller Unit/ / U1102.87` | ERC-pin_not_connected | Pin not connected |  | official |
| 31 | `/Controller Unit/ / U1102.88` | ERC-pin_not_connected | Pin not connected |  | official |
| 32 | `/Controller Unit/ / U1102.90` | ERC-pin_not_connected | Pin not connected |  | official |
| 33 | `/Controller Unit/ / Y1101.4` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 34 | `/PGIA2/ / U505.6` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 35 | `/Power Supply/ / U702.1` | ERC-pin_to_pin | 类型为 Output 和 Output 的引脚已连接 |  | official |
| 36 | `/Power Supply/ / U703.15` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 37 | `/Power Supply/ / U704.1` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 38 | `/Power Supply/ / U709.1` | ERC-pin_to_pin | 类型为 Output 和 Output 的引脚已连接 |  | official |
| 39 | `/Power Supply/ / U711.1` | ERC-pin_to_pin | 类型为 Output 和 Output 的引脚已连接 |  | official |
| 40 | `/Voltage Controlled Current Source/ / U610.2` | ERC-pin_to_pin | 类型为 Output 和 Power output 的引脚已连接 |  | official |

### 警告（174）

| # | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` | R603 | 图纸 / 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 2 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 3 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 4 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 5 | `/` | ERC-lib_symbol_mismatch | 符号 'TCA9539' 与来源库 'Emoe_Interfaces' 中的符号存在差异 |  | official |
| 6 | `/` | ERC-lib_symbol_mismatch | 符号 '2N7002H' 与来源库 'Transistor_FET' 中的符号存在差异 |  | official |
| 7 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 8 | `/` | ERC-unconnected_wire_endpoint | 未连接的连线端点 |  | official |
| 9 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 10 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 11 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 12 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 13 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 14 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 15 | `/` | ERC-lib_symbol_mismatch | 符号 'USB_B' 与来源库 'Connector' 中的符号存在差异 |  | official |
| 16 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 17 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 18 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 19 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 20 | `/` | ERC-lib_symbol_mismatch | 符号 'TCA9539' 与来源库 'Emoe_Interfaces' 中的符号存在差异 |  | official |
| 21 | `/ / #PWR0105.1` | ERC-no_connect_connected | A pin with a "no connection" flag is connected |  | official |
| 22 | `/ / #PWR0108.1` | R304 | #PWR0108.1（+15VA，power_in）被标记为 no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认 |  | structural |
| 23 | `/ / #PWR0108.1` | ERC-no_connect_connected | A pin with a "no connection" flag is connected |  | official |
| 24 | `/ / #PWR0109.1` | R304 | #PWR0109.1（-15VA，power_in）被标记为 no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认 |  | structural |
| 25 | `/ / #PWR0110.1` | R304 | #PWR0110.1（+12VA，power_in）被标记为 no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认 |  | structural |
| 26 | `/ / #PWR0110.1` | ERC-no_connect_connected | A pin with a "no connection" flag is connected |  | official |
| 27 | `/ / #PWR0111.1` | R304 | #PWR0111.1（-2V5A，power_in）被标记为 no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认 |  | structural |
| 28 | `/ / #PWR0111.1` | ERC-no_connect_connected | A pin with a "no connection" flag is connected |  | official |
| 29 | `/ / #PWR0112.1` | R304 | #PWR0112.1（+6VA，power_in）被标记为 no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认 |  | structural |
| 30 | `/ / #PWR0112.1` | ERC-no_connect_connected | A pin with a "no connection" flag is connected |  | official |
| 31 | `/ / #PWR0113.1` | R304 | #PWR0113.1（+5V5A，power_in）被标记为 no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认 |  | structural |
| 32 | `/ / #PWR0113.1` | ERC-no_connect_connected | A pin with a "no connection" flag is connected |  | official |
| 33 | `/ / #PWR0114.1` | R304 | #PWR0114.1（+3.3V，power_in）被标记为 no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认 |  | structural |
| 34 | `/ / #PWR0114.1` | ERC-no_connect_connected | A pin with a "no connection" flag is connected |  | official |
| 35 | `/ / #PWR0115.1` | R304 | #PWR0115.1（+5VD，power_in）被标记为 no-connect——电源输入引脚被 NC 尤为可疑，请对照手册确认 |  | structural |
| 36 | `/ / U101.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 37 | `/ / U101.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 38 | `/18f82026-7301-46f4-a5fb-c832a7fa5dde` | R603 | 图纸 /18f82026-7301-46f4-a5fb-c832a7fa5dde 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 39 | `/32ec778c-7eba-4751-b4ef-324dd1b4de11` | R603 | 图纸 /32ec778c-7eba-4751-b4ef-324dd1b4de11 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 40 | `/484b9cec-0fcd-4b61-a421-fef2c149a552` | R603 | 图纸 /484b9cec-0fcd-4b61-a421-fef2c149a552 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 41 | `/4b194535-7038-4ccf-881a-9da0ecfd7dd5` | R603 | 图纸 /4b194535-7038-4ccf-881a-9da0ecfd7dd5 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 42 | `/4b194535-7038-4ccf-881a-9da0ecfd7dd5 / U802.5` | R302 | 网络 /ADC Channel Switch/PGIA_IN2+_CH2 只有 U802.5 一个连接点，请确认是否悬空或遗漏连接 | /ADC Channel Switch/PGIA_IN2+_CH2 | structural |
| 43 | `/4b194535-7038-4ccf-881a-9da0ecfd7dd5 / U802.6` | R302 | 网络 /ADC Channel Switch/PGIA_IN2+_CH3 只有 U802.6 一个连接点，请确认是否悬空或遗漏连接 | /ADC Channel Switch/PGIA_IN2+_CH3 | structural |
| 44 | `/4b194535-7038-4ccf-881a-9da0ecfd7dd5 / U805.5` | R302 | 网络 /ADC Channel Switch/PGIA_IN2-_CH2 只有 U805.5 一个连接点，请确认是否悬空或遗漏连接 | /ADC Channel Switch/PGIA_IN2-_CH2 | structural |
| 45 | `/4b194535-7038-4ccf-881a-9da0ecfd7dd5 / U805.6` | R302 | 网络 /ADC Channel Switch/PGIA_IN2-_CH3 只有 U805.6 一个连接点，请确认是否悬空或遗漏连接 | /ADC Channel Switch/PGIA_IN2-_CH3 | structural |
| 46 | `/54a3213f-6fa5-45cd-98cf-e5adff6b4b08` | R603 | 图纸 /54a3213f-6fa5-45cd-98cf-e5adff6b4b08 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 47 | `/54a3213f-6fa5-45cd-98cf-e5adff6b4b08 / R601.2` | R302 | 网络 /CURR_GUARD 只有 R601.2 一个连接点，请确认是否悬空或遗漏连接 | /CURR_GUARD | structural |
| 48 | `/808ee41c-9861-4343-95d8-bf495bc90f75` | R603 | 图纸 /808ee41c-9861-4343-95d8-bf495bc90f75 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 49 | `/953a2742-667a-458f-ae96-334224d84db4` | R603 | 图纸 /953a2742-667a-458f-ae96-334224d84db4 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 50 | `/ADC BRD/ / U901.15` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 51 | `/ADC BRD/ / U901.16` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 52 | `/ADC BRD/ / U901.17` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 53 | `/ADC BRD/ / U901.6` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 54 | `/ADC Channel Switch/ / U801.10` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 55 | `/ADC Channel Switch/ / U802.10` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 56 | `/ADC Channel Switch/ / U803.12` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 57 | `/ADC Channel Switch/ / U803.2` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 58 | `/ADC Channel Switch/ / U803.21` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 59 | `/ADC Channel Switch/ / U804.10` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 60 | `/ADC Channel Switch/ / U805.10` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 61 | `/Analog Input MUX Array CH2/ / U301.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 62 | `/Analog Input MUX Array CH2/ / U301.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 63 | `/Analog Input MUX Array CH2/ / U302.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 64 | `/Analog Input MUX Array CH2/ / U302.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 65 | `/Analog Input MUX Array CH2/ / U303.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 66 | `/Analog Input MUX Array CH2/ / U303.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 67 | `/Analog Input MUX Array/ / U201.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 68 | `/Analog Input MUX Array/ / U201.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 69 | `/Analog Input MUX Array/ / U203.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 70 | `/Analog Input MUX Array/ / U203.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 71 | `/Analog Input MUX Array/ / U204.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 72 | `/Analog Input MUX Array/ / U204.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 73 | `/Analog Input MUX Array/ / U205.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 74 | `/Analog Input MUX Array/ / U205.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 75 | `/Controller Unit/ / U1104.7` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 76 | `/Internal Reference Resistor/ / U1203.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 77 | `/Internal Reference Resistor/ / U1203.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 78 | `/Internal Reference Resistor/ / U1204.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 79 | `/Internal Reference Resistor/ / U1204.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 80 | `/Internal Reference Resistor/ / U1205.3` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 81 | `/Internal Reference Resistor/ / U1206.3` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 82 | `/Internal Reference Resistor/ / U1209.7` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 83 | `/Internal Reference Resistor/ / U1211.12` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 84 | `/Internal Reference Resistor/ / U1211.21` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 85 | `/Internal Reference Resistor/ / U1212.3` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 86 | `/Internal Reference Resistor/ / U1213.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 87 | `/Internal Reference Resistor/ / U1213.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 88 | `/Internal Reference Resistor/ / U1214.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 89 | `/Internal Reference Resistor/ / U1214.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 90 | `/PGIA1/ / U506.9` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 91 | `/PGIA2/ / U506.9` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 92 | `/Power Supply/ / J1101.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 93 | `/Power Supply/ / U702.17` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 94 | `/Power Supply/ / U702.18` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 95 | `/Power Supply/ / U702.19` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 96 | `/Power Supply/ / U702.2` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 97 | `/Power Supply/ / U702.21` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 98 | `/Power Supply/ / U702.7` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 99 | `/Power Supply/ / U706.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 100 | `/Power Supply/ / U707.10` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 101 | `/Power Supply/ / U707.15` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 102 | `/Power Supply/ / U707.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 103 | `/Power Supply/ / U707.6` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 104 | `/Power Supply/ / U709.17` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 105 | `/Power Supply/ / U709.18` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 106 | `/Power Supply/ / U709.19` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 107 | `/Power Supply/ / U709.2` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 108 | `/Power Supply/ / U709.21` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 109 | `/Power Supply/ / U709.7` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 110 | `/Power Supply/ / U711.10` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 111 | `/Power Supply/ / U711.11` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 112 | `/Power Supply/ / U711.12` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 113 | `/Power Supply/ / U711.17` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 114 | `/Power Supply/ / U711.18` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 115 | `/Power Supply/ / U711.19` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 116 | `/Power Supply/ / U711.2` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 117 | `/Power Supply/ / U711.21` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 118 | `/Power Supply/ / U711.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 119 | `/Power Supply/ / U711.5` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 120 | `/Power Supply/ / U711.6` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 121 | `/Power Supply/ / U711.7` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 122 | `/Power Supply/ / U711.8` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 123 | `/Power Supply/ / U711.9` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 124 | `/Reference BRD/ / U1001.5` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 125 | `/Reference BRD/ / U1001.9` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 126 | `/Reference BRD/ / U1006.3` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 127 | `/Reference BRD/ / U1006.9` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 128 | `/Reference BRD/ / U1008.7` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 129 | `/Reference BRD/ / U1008.9` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 130 | `/Voltage Controlled Current Source/ / #PWR0616.1` | ERC-multiple_net_names | GND 和 GNDA 都连接到同一项上; 将使用 GND 作为网表中的网络名称 |  | official |
| 131 | `/Voltage Controlled Current Source/ / U605.9` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 132 | `/Voltage Controlled Current Source/ / U608.9` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 133 | `/Voltage Controlled Current Source/ / U609.13` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 134 | `/Voltage Controlled Current Source/ / U609.4` | ERC-pin_to_pin | 类型为 Bidirectional 和 Power output 的引脚已连接 |  | official |
| 135 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9` | R603 | 图纸 /c142b3aa-f761-44e5-bac6-1e851f77c5d9 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 136 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / J903.11` | R302 | 网络 /ADC BRD/ADC_IO8 只有 J903.11 一个连接点，请确认是否悬空或遗漏连接 | /ADC BRD/ADC_IO8 | structural |
| 137 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / J903.12` | R302 | 网络 /ADC BRD/ADC_IO9 只有 J903.12 一个连接点，请确认是否悬空或遗漏连接 | /ADC BRD/ADC_IO9 | structural |
| 138 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / J903.5` | R302 | 网络 /ADC BRD/ADC_IO5 只有 J903.5 一个连接点，请确认是否悬空或遗漏连接 | /ADC BRD/ADC_IO5 | structural |
| 139 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / J903.7` | R302 | 网络 /ADC BRD/ADC_IO6 只有 J903.7 一个连接点，请确认是否悬空或遗漏连接 | /ADC BRD/ADC_IO6 | structural |
| 140 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / J903.8` | R302 | 网络 /ADC BRD/ADC_IO11 只有 J903.8 一个连接点，请确认是否悬空或遗漏连接 | /ADC BRD/ADC_IO11 | structural |
| 141 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / J903.9` | R302 | 网络 /ADC BRD/ADC_IO7 只有 J903.9 一个连接点，请确认是否悬空或遗漏连接 | /ADC BRD/ADC_IO7 | structural |
| 142 | `/da12ad2c-a218-4f65-9f1a-c5abb68e5160` | R603 | 图纸 /da12ad2c-a218-4f65-9f1a-c5abb68e5160 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 143 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a` | R603 | 图纸 /db7d6b1f-9df6-4919-b552-4c0b97a52f9a 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 144 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.15` | R301 | U1102.15（PC0，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 145 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.16` | R301 | U1102.16（PC1，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 146 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.17` | R301 | U1102.17（PC2_C，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 147 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.18` | R301 | U1102.18（PC3_C，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 148 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.22` | R301 | U1102.22（PA0，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 149 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.23` | R301 | U1102.23（PA1，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 150 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.24` | R301 | U1102.24（PA2，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 151 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.25` | R301 | U1102.25（PA3，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 152 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.28` | R301 | U1102.28（PA4，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 153 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.29` | R302 | 网络 /Controller Unit/SPI1_SCK 只有 U1102.29 一个连接点，请确认是否悬空或遗漏连接 | /Controller Unit/SPI1_SCK | structural |
| 154 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.31` | R301 | U1102.31（PA7，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 155 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.33` | R301 | U1102.33（PC5，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 156 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.39` | R302 | 网络 /Controller Unit/PE9 只有 U1102.39 一个连接点，请确认是否悬空或遗漏连接 | /Controller Unit/PE9 | structural |
| 157 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.40` | R302 | 网络 /Controller Unit/PE10 只有 U1102.40 一个连接点，请确认是否悬空或遗漏连接 | /Controller Unit/PE10 | structural |
| 158 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.42` | R302 | 网络 /PE12 只有 U1102.42 一个连接点，请确认是否悬空或遗漏连接 | /PE12 | structural |
| 159 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.43` | R302 | 网络 /PE13 只有 U1102.43 一个连接点，请确认是否悬空或遗漏连接 | /PE13 | structural |
| 160 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.46` | R301 | U1102.46（PB10，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 161 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.47` | R301 | U1102.47（PB11，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 162 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.55` | R302 | 网络 /PD8 只有 U1102.55 一个连接点，请确认是否悬空或遗漏连接 | /PD8 | structural |
| 163 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.61` | R301 | U1102.61（PD14，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 164 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.62` | R301 | U1102.62（PD15，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 165 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.63` | R301 | U1102.63（PC6，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 166 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.64` | R301 | U1102.64（PC7，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 167 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.77` | R301 | U1102.77（PA15，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 168 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.81` | R302 | 网络 /Controller Unit/SPI3_LDAC 只有 U1102.81 一个连接点，请确认是否悬空或遗漏连接 | /Controller Unit/SPI3_LDAC | structural |
| 169 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.85` | R301 | U1102.85（PD4，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 170 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.86` | R301 | U1102.86（PD5，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 171 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.87` | R301 | U1102.87（PD6，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 172 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.88` | R301 | U1102.88（PD7，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 173 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102.90` | R301 | U1102.90（PB4，类型 bidirectional）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 174 | `/e0d8101f-0eb7-4516-af8f-412fe166df93` | R603 | 图纸 /e0d8101f-0eb7-4516-af8f-412fe166df93 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |

### 提示（51）

| # | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` | R103 | 11 个前缀的位号有缺号: C 缺895（C101..C1226；段内缺号: C206, C211, C607, C609, C618, C718, C722, C737 …(+6)）, D 缺979（D101..D1103）, FB 缺977（FB101..FB1101；段内缺号: FB702）, H 缺1092（H101..H1204）, J 缺980（J101..J1105）, L 缺99（L601..L709）, Q 缺404（Q201..Q610；段内缺号: Q604, Q605, Q606, Q607, Q608, Q609）, R 缺938（R101..R1206；段内缺号: R119, R121, R123, R125, R127, R130, R133, R135 …(+5)）, TP 缺867（TP101..TP1011；段内缺号: TP608, TP1008, TP1009, TP1010）, U 缺1136（U1..U1214；段内缺号: U202, U1207, U1208, U1210）, Y 缺199（Y901..Y1101）。跨页编 hundreds 的工程跨段空号属正常（按页分段编号），段内缺号通常是迭代删除，仅供审阅时参考 |  | heuristic |
| 2 | `/` | R402 | 项目有 226 个未命名网络（N$，占网络总数 53%）；关键信号建议命名以便跨页追踪与复查。最大的几个: N$273(8 脚); N$321(8 脚); N$103(6 脚); N$215(6 脚); N$288(6 脚) | N$273, N$321, N$103 | heuristic |
| 3 | `/` | R701 | 1 个器件标记为不焊接（DNP）: R131(33R) |  | structural |
| 4 | `/ / D101` | R801 | D101（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->EXT_REF_TERM_1; 1(A1)->GND |  | structural |
| 5 | `/ / D102` | R801 | D102（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->EXT_REF_TERM_2; 1(A1)->GND |  | structural |
| 6 | `/ / D103` | R801 | D103（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->EXT_REF_SENSE2; 1(A1)->GND |  | structural |
| 7 | `/ / D104` | R801 | D104（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->EXT_REF_SENSE1; 1(A1)->GND |  | structural |
| 8 | `/ / U101` | R304 | U101（ADG1436YCPZ）有 3 个引脚被标记为 no-connect: 5, 7, 14（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 9 | `/18f82026-7301-46f4-a5fb-c832a7fa5dde / D201` | R801 | D201（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->N$114; 1(A1)->GND |  | structural |
| 10 | `/18f82026-7301-46f4-a5fb-c832a7fa5dde / D202` | R801 | D202（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->N$183; 1(A1)->GND |  | structural |
| 11 | `/18f82026-7301-46f4-a5fb-c832a7fa5dde / D203` | R801 | D203（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->N$184; 1(A1)->GND |  | structural |
| 12 | `/18f82026-7301-46f4-a5fb-c832a7fa5dde / D204` | R801 | D204（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->N$194; 1(A1)->GND |  | structural |
| 13 | `/32ec778c-7eba-4751-b4ef-324dd1b4de11` | R701 | 3 个器件标记为不焊接（DNP）: C1034(10uF), R1012(0R), R1018(0R) |  | structural |
| 14 | `/4b194535-7038-4ccf-881a-9da0ecfd7dd5 / U803` | R304 | U803（TCA9539PWR）有 1 个引脚被标记为 no-connect: 1（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 15 | `/54a3213f-6fa5-45cd-98cf-e5adff6b4b08 / U601` | R304 | U601（OPA189IDR）有 3 个引脚被标记为 no-connect: 1, 8, 5（类型 bidirectional, no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 16 | `/54a3213f-6fa5-45cd-98cf-e5adff6b4b08 / U602` | R304 | U602（LM393DR2G）有 1 个引脚被标记为 no-connect: 7（类型 open_collector）；请对照手册确认这些脚确实可悬空 |  | structural |
| 17 | `/54a3213f-6fa5-45cd-98cf-e5adff6b4b08 / U605` | R304 | U605（LHE5400-6）有 2 个引脚被标记为 no-connect: 4, 5（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 18 | `/54a3213f-6fa5-45cd-98cf-e5adff6b4b08 / U609` | R304 | U609（ADG1436YCPZ）有 3 个引脚被标记为 no-connect: 5, 14, 7（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 19 | `/808ee41c-9861-4343-95d8-bf495bc90f75 / D301` | R801 | D301（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->N$130; 1(A1)->GND |  | structural |
| 20 | `/808ee41c-9861-4343-95d8-bf495bc90f75 / D302` | R801 | D302（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->N$228; 1(A1)->GND |  | structural |
| 21 | `/808ee41c-9861-4343-95d8-bf495bc90f75 / D303` | R801 | D303（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->N$189; 1(A1)->GND |  | structural |
| 22 | `/808ee41c-9861-4343-95d8-bf495bc90f75 / D304` | R801 | D304（ESD601DPYRQ1）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 2(A2)->N$230; 1(A1)->GND |  | structural |
| 23 | `/953a2742-667a-458f-ae96-334224d84db4` | R701 | 2 个器件标记为不焊接（DNP）: R716(100k), R712(100k) |  | structural |
| 24 | `/953a2742-667a-458f-ae96-334224d84db4 / U702` | R304 | U702（TPS7A4701RGWR）有 8 个引脚被标记为 no-connect: 9, 10, 12, 6, 11, 5, 4, 8（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 25 | `/953a2742-667a-458f-ae96-334224d84db4 / U703` | R304 | U703（ADP5071ACPZ）有 2 个引脚被标记为 no-connect: 3, 8（类型 input, passive）；请对照手册确认这些脚确实可悬空 |  | structural |
| 26 | `/953a2742-667a-458f-ae96-334224d84db4 / U704` | R304 | U704（LT3094EDD）有 2 个引脚被标记为 no-connect: 4, 7（类型 open_collector, passive）；请对照手册确认这些脚确实可悬空 |  | structural |
| 27 | `/953a2742-667a-458f-ae96-334224d84db4 / U705` | R304 | U705（GM1200ACPZ）有 1 个引脚被标记为 no-connect: 4（类型 open_collector）；请对照手册确认这些脚确实可悬空 |  | structural |
| 28 | `/953a2742-667a-458f-ae96-334224d84db4 / U708` | R304 | U708（GM1200ACPZ）有 1 个引脚被标记为 no-connect: 4（类型 open_collector）；请对照手册确认这些脚确实可悬空 |  | structural |
| 29 | `/953a2742-667a-458f-ae96-334224d84db4 / U709` | R304 | U709（TPS7A4701RGWR）有 8 个引脚被标记为 no-connect: 9, 10, 12, 6, 11, 5, 4, 8（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 30 | `/953a2742-667a-458f-ae96-334224d84db4 / U710` | R304 | U710（ADP5071ACPZ）有 2 个引脚被标记为 no-connect: 3, 8（类型 input, passive）；请对照手册确认这些脚确实可悬空 |  | structural |
| 31 | `/953a2742-667a-458f-ae96-334224d84db4 / U712` | R304 | U712（74HC390D）有 5 个引脚被标记为 no-connect: 6, 5, 9, 10, 11（类型 output）；请对照手册确认这些脚确实可悬空 |  | structural |
| 32 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9` | R701 | 3 个器件标记为不焊接（DNP）: U901(LHA7532B), U901(LHA7532B), Y901(SX3M4.9152M20F30TNN) |  | structural |
| 33 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / J901` | R304 | J901（2.54mm_2x6P）有 2 个引脚被标记为 no-connect: 1, 11（类型 passive）；请对照手册确认这些脚确实可悬空 |  | structural |
| 34 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / U901` | R304 | U901（LHA7532B）有 3 个引脚被标记为 no-connect: 7, 8, 10（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 35 | `/c142b3aa-f761-44e5-bac6-1e851f77c5d9 / U902` | R304 | U902（LP5907MFX-3.3）有 1 个引脚被标记为 no-connect: 4（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 36 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a` | R701 | 2 个器件标记为不焊接（DNP）: J1105(2.54mm_Header_10P), R1107(0R) |  | structural |
| 37 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / J1104` | R304 | J1104（TC2030-NL）有 1 个引脚被标记为 no-connect: 6（类型 input）；请对照手册确认这些脚确实可悬空 |  | structural |
| 38 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1102` | R304 | U1102（STM32H7B0VBT6）有 1 个引脚被标记为 no-connect: 13（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 39 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1104` | R304 | U1104（TMP117AIDRV）有 1 个引脚被标记为 no-connect: 3（类型 open_collector）；请对照手册确认这些脚确实可悬空 |  | structural |
| 40 | `/db7d6b1f-9df6-4919-b552-4c0b97a52f9a / U1105` | R304 | U1105（SN74LVC1G14DBV）有 1 个引脚被标记为 no-connect: 1（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 41 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1201` | R304 | U1201（ADG1408YRUZ）有 2 个引脚被标记为 no-connect: 5, 7（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 42 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1202` | R304 | U1202（ADG1408YRUZ）有 2 个引脚被标记为 no-connect: 5, 7（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 43 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1203` | R304 | U1203（ADG1436YCPZ）有 3 个引脚被标记为 no-connect: 7, 5, 14（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 44 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1204` | R304 | U1204（ADG1436YCPZ）有 3 个引脚被标记为 no-connect: 7, 5, 14（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 45 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1205` | R304 | U1205（ADG1412YCPZ）有 1 个引脚被标记为 no-connect: 10（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 46 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1206` | R304 | U1206（ADG1412YCPZ）有 1 个引脚被标记为 no-connect: 10（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 47 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1209` | R304 | U1209（TMP117AIDRV）有 1 个引脚被标记为 no-connect: 3（类型 open_collector）；请对照手册确认这些脚确实可悬空 |  | structural |
| 48 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1211` | R304 | U1211（TCA9539PWR）有 3 个引脚被标记为 no-connect: 1, 7, 18（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 49 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1212` | R304 | U1212（ADG1412YCPZ）有 1 个引脚被标记为 no-connect: 10（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 50 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1213` | R304 | U1213（ADG1436YCPZ）有 5 个引脚被标记为 no-connect: 8, 5, 7, 14, 16（类型 no_connect, passive）；请对照手册确认这些脚确实可悬空 |  | structural |
| 51 | `/e0d8101f-0eb7-4516-af8f-412fe166df93 / U1214` | R304 | U1214（ADG1436YCPZ）有 5 个引脚被标记为 no-connect: 8, 5, 7, 14, 16（类型 no_connect, passive）；请对照手册确认这些脚确实可悬空 |  | structural |

## 4. 工具与方法说明

- 网络表由纯 Python 几何连通域构建（导线端点 + 连接点 + 标签 + 电源符号），并完成分层图纸与全局标签合并。
- KiCad ERC 已运行: {'error': 39, 'warning': 113}
- 悬空/单引脚等判定基于本工具解析结果；KiCad ERC 结果（如已运行）以 ERC-* 代码单独列出。
- 报告中的 info 级发现需要人工结合设计意图判断，不代表设计错误。
- 发现条目带"依据"级别：official=官方 ERC 转写；structural=原理图结构事实；declared=字段约定检查；heuristic=启发式建议（可结合设计意图忽略）。
