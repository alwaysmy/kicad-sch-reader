# LCEDA `.epro` 审查报告 — EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd

> 数据来源：`D:\MyProjects\AI\schematics_review_tool\examples\LIA_DigitalBoard_RevA\ProPrj_XC7A35TCSG325_EmoeSOM_2026-05-18.epro`
> 主原理图：EmoeSOM_A7_DDR_RevA_ForLIA_4L.sch（13 页）

## 1. CBB 模块实例

| 母图页 | 位号 | CBB 模块 | 引脚→母图网络 | 母图位置 |
| --- | --- | --- | --- | --- |
| EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB | CBB4 | _CBB_接口_通用TypeC-5V带数据供电 | VBUS=VBUS_5V_USB, D+=USBC_D_PE, D-=USBC_D_NE, GND=GND | (190, 865) |
| EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB | CBB2 | _CBB_接口_通用TypeC-5V带数据供电 | VBUS=VBUS_5V_DBG, D+=USBDBG_D_PE, D-=USBDBG_D_NE, GND=GND | (190, 975) |
| EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::SYS_POWER | CBB1 | _CBB_SMPS_TPS563201_BUCK_2L | VIN=VCC_5V, VOUT=VCC_1V5, GND=GND, EN=VCC_1V8 | (345, 590) |
| EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::SYS_POWER | CBB3 | _CBB_SMPS_EA3059_4CH_BUCK_2L_TINY | VIN=VCC_5V, GND=GND, VOUT1=VCC_1V0, VOUT2=VCC_1V8, VOUT3=VCC_2V5, VOUT4=VCC_3V3, EN1=VCC_5V, EN2=VCC_5V, EN3=VCC_5V, EN4=VCC_5V | (345, 750) |

## 2. 设计审查发现

### 警告（5）

| # | 位置 | 代码 | 说明 |
| --- | --- | --- | --- |
| 1 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CBB4.D+` | CBB_PIN_TYPE_SUSPECT | CBB 模块 _CBB_接口_通用TypeC-5V带数据供电 引脚 D+ 标记为 IN，但按名称应为输出/双向 |
| 2 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CBB4.D-` | CBB_PIN_TYPE_SUSPECT | CBB 模块 _CBB_接口_通用TypeC-5V带数据供电 引脚 D- 标记为 IN，但按名称应为输出/双向 |
| 3 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CBB2.D+` | CBB_PIN_TYPE_SUSPECT | CBB 模块 _CBB_接口_通用TypeC-5V带数据供电 引脚 D+ 标记为 IN，但按名称应为输出/双向 |
| 4 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CBB2.D-` | CBB_PIN_TYPE_SUSPECT | CBB 模块 _CBB_接口_通用TypeC-5V带数据供电 引脚 D- 标记为 IN，但按名称应为输出/双向 |
| 5 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::SYS_POWER / CBB1.VOUT` | CBB_PIN_TYPE_SUSPECT | CBB 模块 _CBB_SMPS_TPS563201_BUCK_2L 引脚 VOUT 标记为 IN，但按名称应为输出/双向 |

### 提示（122）

| # | 位置 | 代码 | 说明 |
| --- | --- | --- | --- |
| 1 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::SYS_POWER / CBB3.GND` | CBB_PIN_TYPE_SUSPECT | CBB 模块 _CBB_SMPS_EA3059_4CH_BUCK_2L_TINY 引脚 GND 类型为 BI，建议确认 |
| 2 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / U1` | MULTI_UNIT_OR_REUSED_REF | 位号 U1 跨 4 页出现（多单元器件或复用，需人工确认） |
| 3 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::MCU(JTAG) / U5` | SINGLE_PIN_NET | 网络 DBG_SPI_CLK 仅 U5.PB13/SPI2SCK/UART3CTS/CAN2TX 一个引脚 |
| 4 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::MCU(JTAG) / U5` | SINGLE_PIN_NET | 网络 DBG_SPI_CS 仅 U5.PB12/SPI2NSS/CAN2RX 一个引脚 |
| 5 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::MCU(JTAG) / U5` | SINGLE_PIN_NET | 网络 DBG_SPI_MISO 仅 U5.PB14/SPI2MISO/UART3RTS 一个引脚 |
| 6 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::MCU(JTAG) / U5` | SINGLE_PIN_NET | 网络 DBG_SPI_MOSI 仅 U5.PB15/SPI2MOSI/UART1TX2 一个引脚 |
| 7 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / R110` | SINGLE_PIN_NET | 网络 FPGA_CCLK 仅 R110.1 一个引脚 |
| 8 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / R116` | SINGLE_PIN_NET | 网络 FPGA_M0 仅 R116.1 一个引脚 |
| 9 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / U15` | SINGLE_PIN_NET | 网络 FPGA_QSPI_DQ0 仅 U15.DI 一个引脚 |
| 10 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / U15` | SINGLE_PIN_NET | 网络 FPGA_QSPI_DQ1 仅 U15.DO 一个引脚 |
| 11 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / U15` | SINGLE_PIN_NET | 网络 FPGA_QSPI_DQ2 仅 U15.IO2 一个引脚 |
| 12 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / U15` | SINGLE_PIN_NET | 网络 FPGA_QSPI_DQ3 仅 U15.IO3 一个引脚 |
| 13 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / R25` | SINGLE_PIN_NET | 网络 FPGA_TDO 仅 R25.1 一个引脚 |
| 14 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / R30` | SINGLE_PIN_NET | 网络 INIT_B 仅 R30.1 一个引脚 |
| 15 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L10N_T1_34 仅 CN7.35 一个引脚 |
| 16 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L10P_T1_34 仅 CN7.33 一个引脚 |
| 17 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L12N_T1_MRCC_34 仅 CN7.39 一个引脚 |
| 18 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L12P_T1_MRCC_34 仅 CN7.41 一个引脚 |
| 19 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L13N_T2_MRCC_14 仅 CN7.71 一个引脚 |
| 20 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L13N_T2_MRCC_34 仅 CN7.28 一个引脚 |
| 21 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L13P_T2_MRCC_14 仅 CN7.69 一个引脚 |
| 22 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L13P_T2_MRCC_34 仅 CN7.26 一个引脚 |
| 23 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L14N_T2_SRCC_34 仅 CN7.43 一个引脚 |
| 24 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L14P_T2_SRCC_34 仅 CN7.45 一个引脚 |
| 25 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L15N_T2_DQS_34 仅 CN7.34 一个引脚 |
| 26 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L15P_T2_DQS_34 仅 CN7.32 一个引脚 |
| 27 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L16N_T2_34 仅 CN7.36 一个引脚 |
| 28 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / TP3` | SINGLE_PIN_NET | 网络 IO_L16N_T2_A15_D31_14 仅 TP3.1 一个引脚 |
| 29 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L16P_T2_34 仅 CN7.38 一个引脚 |
| 30 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / TP4` | SINGLE_PIN_NET | 网络 IO_L16P_T2_CSI_B_14 仅 TP4.1 一个引脚 |
| 31 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L17N_T2_34 仅 CN7.49 一个引脚 |
| 32 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L17N_T2_A13_D29_14 仅 CN7.77 一个引脚 |
| 33 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L17P_T2_34 仅 CN7.51 一个引脚 |
| 34 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L17P_T2_A14_D30_14 仅 CN7.75 一个引脚 |
| 35 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L18N_T2_34 仅 CN7.44 一个引脚 |
| 36 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L18P_T2_34 仅 CN7.42 一个引脚 |
| 37 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L19N_T3_A09_D25_VREF_14 仅 CN7.63 一个引脚 |
| 38 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L19P_T3_A10_D26_14 仅 CN7.65 一个引脚 |
| 39 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L20N_T3_34 仅 CN7.46 一个引脚 |
| 40 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L20N_T3_A07_D23_14 仅 CN7.76 一个引脚 |
| 41 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L20P_T3_34 仅 CN7.48 一个引脚 |
| 42 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L20P_T3_A08_D24_14 仅 CN7.78 一个引脚 |
| 43 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L21N_T3_DQS_34 仅 CN7.55 一个引脚 |
| 44 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L21N_T3_DQS_A06_D22_14 仅 CN7.74 一个引脚 |
| 45 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L21P_T3_DQS_14 仅 CN7.72 一个引脚 |
| 46 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L21P_T3_DQS_34 仅 CN7.53 一个引脚 |
| 47 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L22N_T3_34 仅 CN7.61 一个引脚 |
| 48 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L22P_T3_34 仅 CN7.59 一个引脚 |
| 49 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L23N_T3_34 仅 CN7.52 一个引脚 |
| 50 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L23N_T3_A02_D18_14 仅 CN7.66 一个引脚 |
| 51 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L23P_T3_34 仅 CN7.54 一个引脚 |
| 52 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L23P_T3_A03_D19_14 仅 CN7.68 一个引脚 |
| 53 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L24N_T3_34 仅 CN7.56 一个引脚 |
| 54 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L24N_T3_A00_D16_14 仅 CN7.64 一个引脚 |
| 55 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L24P_T3_34 仅 CN7.58 一个引脚 |
| 56 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L24P_T3_A01_D17_14 仅 CN7.62 一个引脚 |
| 57 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L3N_T0_DQS_34 仅 CN7.14 一个引脚 |
| 58 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L3P_T0_DQS_34 仅 CN7.12 一个引脚 |
| 59 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L4N_T0_34 仅 CN7.19 一个引脚 |
| 60 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L4P_T0_34 仅 CN7.21 一个引脚 |
| 61 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L5N_T0_34 仅 CN7.25 一个引脚 |
| 62 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L5P_T0_34 仅 CN7.23 一个引脚 |
| 63 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L6N_T0_VREF_34 仅 CN7.31 一个引脚 |
| 64 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L6P_T0_34 仅 CN7.29 一个引脚 |
| 65 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L7N_T1_34 仅 CN7.18 一个引脚 |
| 66 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L7P_T1_34 仅 CN7.16 一个引脚 |
| 67 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L9N_T1_DQS_34 仅 CN7.24 一个引脚 |
| 68 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 IO_L9P_T1_DQS_34 仅 CN7.22 一个引脚 |
| 69 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::CLOCK / C15` | SINGLE_PIN_NET | 网络 MGT_CLK0_N 仅 C15.2 一个引脚 |
| 70 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::CLOCK / C14` | SINGLE_PIN_NET | 网络 MGT_CLK0_P 仅 C14.2 一个引脚 |
| 71 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 MGT_RX3_N 仅 CN7.15 一个引脚 |
| 72 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 MGT_RX3_P 仅 CN7.13 一个引脚 |
| 73 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 MGT_TX3_N 仅 CN7.6 一个引脚 |
| 74 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::USB&BTB / CN7` | SINGLE_PIN_NET | 网络 MGT_TX3_P 仅 CN7.8 一个引脚 |
| 75 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A0 仅 U24.A0 一个引脚 |
| 76 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A1 仅 U24.A1 一个引脚 |
| 77 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A10 仅 U24.A10/AP 一个引脚 |
| 78 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A11 仅 U24.A11 一个引脚 |
| 79 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A12 仅 U24.A12/BC# 一个引脚 |
| 80 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A13 仅 U24.A13 一个引脚 |
| 81 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A14 仅 U24.A14 一个引脚 |
| 82 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A15 仅 U24.NC 一个引脚 |
| 83 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A2 仅 U24.A2 一个引脚 |
| 84 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A3 仅 U24.A3 一个引脚 |
| 85 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A4 仅 U24.A4 一个引脚 |
| 86 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A5 仅 U24.A5 一个引脚 |
| 87 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A6 仅 U24.A6 一个引脚 |
| 88 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A7 仅 U24.A7 一个引脚 |
| 89 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A8 仅 U24.A8 一个引脚 |
| 90 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_A9 仅 U24.A9 一个引脚 |
| 91 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_BA0 仅 U24.BA0 一个引脚 |
| 92 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_BA1 仅 U24.BA1 一个引脚 |
| 93 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_BA2 仅 U24.BA2 一个引脚 |
| 94 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_CAS_B 仅 U24.CAS# 一个引脚 |
| 95 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_CKE 仅 U24.CKE 一个引脚 |
| 96 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_CS_B 仅 U24.CS# 一个引脚 |
| 97 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DM0 仅 U24.LDM 一个引脚 |
| 98 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DM1 仅 U24.UDM 一个引脚 |
| 99 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ0 仅 U24.DQ0 一个引脚 |
| 100 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ1 仅 U24.DQ1 一个引脚 |
| 101 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ10 仅 U24.DQ10 一个引脚 |
| 102 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ11 仅 U24.DQ11 一个引脚 |
| 103 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ12 仅 U24.DQ12 一个引脚 |
| 104 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ13 仅 U24.DQ13 一个引脚 |
| 105 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ14 仅 U24.DQ14 一个引脚 |
| 106 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ15 仅 U24.DQ15 一个引脚 |
| 107 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ2 仅 U24.DQ2 一个引脚 |
| 108 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ3 仅 U24.DQ3 一个引脚 |
| 109 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ4 仅 U24.DQ4 一个引脚 |
| 110 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ5 仅 U24.DQ5 一个引脚 |
| 111 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ6 仅 U24.DQ6 一个引脚 |
| 112 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ7 仅 U24.DQ7 一个引脚 |
| 113 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ8 仅 U24.DQ8 一个引脚 |
| 114 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQ9 仅 U24.DQ9 一个引脚 |
| 115 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQS0_N 仅 U24.LDQS# 一个引脚 |
| 116 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQS0_P 仅 U24.LDQS 一个引脚 |
| 117 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQS1_N 仅 U24.UDQS# 一个引脚 |
| 118 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_DQS1_P 仅 U24.UDQS 一个引脚 |
| 119 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_ODT 仅 U24.ODT 一个引脚 |
| 120 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_RAS_B 仅 U24.RAS# 一个引脚 |
| 121 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::DRAM / U24` | SINGLE_PIN_NET | 网络 PL_DDR_WE_B 仅 U24.WE# 一个引脚 |
| 122 | `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd::FPGA CONFIG / R29` | SINGLE_PIN_NET | 网络 PROGRAM_B 仅 R29.1 一个引脚 |

## 3. 展平 BOM（含 CBB 内部器件）

共 81 行 / 260 个位号。

| 器件/值 | 封装 | 数量 | 位号 |
| --- | --- | --- | --- |
| 0402B221K500NT | 5e09589c82772842 | 4 | C21, C31, C36, C44 |
| 0402CG100J500NT | 5e09589c82772842 | 4 | C51, C52, C204, C205 |
| 0402WGF1000TCE | b0a21af130e22d73 | 1 | R1 |
| 0402WGF1001TCE | b0a21af130e22d73 | 5 | R26, R94, R95, R115, R116 |
| 0402WGF1002TCE | b0a21af130e22d73 | 2 | R32, R34 |
| 0402WGF1003TCE | e240cef0a04b2f7e | 4 | R18, R20, R27, R31 |
| 0402WGF1802TCE | fab321e682bfdefa | 1 | R113 |
| 0402WGF2003TCE | e240cef0a04b2f7e | 1 | R19 |
| 0402WGF220JTCE | b0a21af130e22d73 | 25 | R12, R15, R21, R25, R35, R36, R39, R40, R41, R42, R43, R44, R45, R46, R48, R49, R52, R91, R92, R110, R134, R135, R136, R137, R138 |
| 0402WGF2400TCE | b0a21af130e22d73 | 1 | R5 |
| 0402WGF3163TCE | b0a21af130e22d73 | 1 | R24 |
| 0402WGF4701TCE | b0a21af130e22d73 | 6 | R29, R30, R47, R60, R131, R139 |
| 0402WGF5100TCE | b0a21af130e22d73 | 2 | R22, R23 |
| 0402WGF510JTCE | b0a21af130e22d73 | 1 | R96 |
| 0402WGF6200TCE | b0a21af130e22d73 | 2 | R11, R13 |
| 0402WGF6802TCE | e240cef0a04b2f7e | 1 | R17 |
| 0603WAJ0512T5E | ff86949838e23dbc | 4 | R6, R7, R8, R9 |
| 8132H-50.000ML33DTL | 88fef3f7feee8bbc | 1 | OSC2 |
| AC0402FR-07453KL | e240cef0a04b2f7e | 1 | R28 |
| AFE201612S1R5MBT | 52abc3e55eb1bd5f | 4 | L1, L2, L3, L4 |
| AT24C16M5/TR | bdbfb87a99c1c663 | 1 | U10 |
| BLM15PD121SN1D | 5dd6ab62108302c1 | 3 | FB4, FB6, FB8 |
| BLM18PG121SN1D | a4ed4ce4a5915003 | 1 | FB7 |
| C0402 | fc384027295dde45 | 2 | C14, C15 |
| CC0402JRNPO9BN100 | 5e09589c82772842 | 1 | C42 |
| CC0402KRX7R6BB474 | 5e09589c82772842 | 12 | C4, C5, C6, C7, C161, C162, C163, C164, C177, C178, C180, C181 |
| CC0402KRX7R9BB103 | 5e09589c82772842 | 4 | C43, C97, C98, C170 |
| CC0402KRX7R9BB104 | 0d12e6d9028f6bfe | 19 | C9, C10, C11, C12, C13, C16, C17, C46, C47, C48, C49, C50, C53, C54, C55, C56, C201, C202, C203 |
| CC0603KRX7R9BB105 | 391e3edc5506eb64 | 3 | C1, C8, C39 |
| CH32V305GBU6 | 7b2bb61c380a2ff0 | 1 | U5 |
| CH32V307RCT6 | 14f70959027070c3 | 1 | U3 |
| CL05B104KB54PNC | 5e09589c82772842 | 1 | C37 |
| DSHP01TSGET | 9f4cb0e4b2e9ea6c | 1 | SW8 |
| EA3059 | 7cb5afc1c98d8bf8 | 1 | U7 |
| ESD5Z3.3T1G-MS | bbca3490b4aa7f7a | 1 | D9 |
| ESD5Z3.3_SOD523 | 6653e02a67429e5d | 1 | D7 |
| FTC252010S4R7MBCA | 76b7249dfa5994fc | 1 | L5 |
| GRM155R61A106ME11D | 5e09589c82772842 | 3 | C157, C158, C159 |
| GRM155R61A225KE95D | 5e09589c82772842 | 1 | C30 |
| GRM155R70J105KA12D | 5e09589c82772842 | 10 | C58, C103, C105, C106, C107, C112, C113, C118, C119, C120 |
| GRM155Z71A105KE01D | 5e09589c82772842 | 2 | C33, C34 |
| GRM155Z71A225KE01D | df3454e5cddc18c5 | 19 | C23, C24, C25, C26, C160, C171, C173, C174, C175, C176, C186, C187, C188, C189, C193, C194, C195, C197, C199 |
| GRM188R61A226ME15D | fab803fd171fd310 | 4 | C22, C27, C28, C29 |
| GRM188Z71A106KA73D | 584735e579b1db0d | 2 | C206, C207 |
| GRM188Z71A475KE15D | 600c280db6051593 | 10 | C2, C3, C57, C165, C166, C179, C182, C185, C198, C200 |
| GRM21BR61E226ME44L | b5d6eca0b2a622a3 | 7 | C18, C32, C35, C38, C40, C41, C45 |
| GRM21BZ71A226ME15L | fac18ca13d2804bd | 2 | C19, C20 |
| HR913550A | d5ee7794719fec6c | 1 | RJ2 |
| HX-GH1.25-3PWT | 8ebc3a0692152796 | 2 | CN1, CN2 |
| M2.5螺丝安装孔_金属化 | 64e681b05239eabf | 4 | H1, H2, H3, H4 |
| MARK_d1D2 | 009575afca1d25fc | 6 | MARK1, MARK2, MARK3, MARK4, MARK5, MARK6 |
| MT41K256M16TW-107 IT:P | ccbb826e57c42ccb | 2 | U24, U24 |
| NCD0603G1 | 3d4e8ed3d2e4b8ea | 3 | LED2, LED5, LED6 |
| PinHeader_1x03_P2.54mm_Vertical | 0a8c153fa1376670 | 1 | H5 |
| RC-02K9101FT | b0a21af130e22d73 | 1 | R33 |
| RC-02W80R6FT | b0a21af130e22d73 | 1 | R57 |
| RC0402FR-0710KL | b0a21af130e22d73 | 6 | R2, R3, R4, R53, R111, R112 |
| RC0402FR-074K7L | b0a21af130e22d73 | 2 | R37, R38 |
| RC0603FR-07120RL | 9fbf295d3572874b | 1 | R10 |
| RCLAMP0522P.TCT | 9ee9f6f1c3b37740 | 1 | D10 |
| RCLAMP0524P_C907837 | b79e65294ca11c18 | 3 | D6, D13, D14 |
| RT0402BRD0710KL | b0a21af130e22d73 | 4 | R14, R16, R50, R51 |
| SKRPACE010 | 3c4b44725af0273e | 1 | SW6 |
| SMD0603-050-12 | 9bf0ff41909dc346 | 4 | F2, F3, F4, F5 |
| SMF15CA_C19077510 | d1636e5f67ee04fd | 2 | D11, D12 |
| SMF6.5CA_C19077501 | d1636e5f67ee04fd | 2 | D3, D5 |
| TF PUSH | 8d6ce1d245f6ed65 | 1 | CARD1 |
| TLV73312PQDRVRQ1 | 8fea1ce2bc21bfcd | 1 | U4 |
| TMP112AIDRLR | c099e4bf18e51be4 | 1 | U12 |
| TPS563201DDCR | 10b425e02863b853 | 1 | U6 |
| TPT3232E-TS3R | a3c81d0dfc52614d | 1 | U2 |
| TPT75176HL1-DF6R | 3225285726d70a95 | 1 | U11 |
| TYPEC-304-ACP16 | f8c1d5c91b1cb4a2 | 2 | USB1, USB2 |
| TestPoint_D0.8_SMD | 933a9edd26c749c3 | 4 | TP1, TP2, TP3, TP4 |
| USBLC6-2P6_C49451919 | da41640c161f1dd5 | 3 | D1, D2, D4 |
| W25Q128JVSIQ | e7ce8df8d6a1041e | 1 | U15 |
| WAFER-GH1.25-4PWB | fd4b7e8c8c7bc2e5 | 1 | U9 |
| X0802FVS-80AS-LPV01 | 31b30b69f2f07c43 | 1 | CN7 |
| XC7A35T-2CSG325C | 33b4aa6051808efd | 7 | U1, U1, U1, U1, U1, U1, U1 |
| XL2EL89COI-111YLC-8M | b6f81d50502e1b07 | 2 | X1, X2 |
| ZX-SH1.0-8PWT | 6f313c475ee9e6f4 | 1 | U16 |
