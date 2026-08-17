# 多工程跨板检查报告

- `Lock-In-Amplifier_MainBoard_V0.1` [kicad] — 连接器 6 个
- `Lock-In-Amplifier_PowerBoard_V0.1` [kicad] — 连接器 3 个
- `EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd` [lceda] — 连接器 15 个

| A | B | 一致 pin | 共同 pin | score | confidence | 差异示例 |
| --- | --- | --- | --- | --- | --- | --- |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | 16 | 16 | 1.0 | detected |  |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | 1 | 2 | 0.5 | candidate | 1: +5VP != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | 1 | 2 | 0.5 | candidate | 1: +12VA != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | 1 | 2 | 0.5 | candidate | 1: N$46 != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | 1 | 2 | 0.5 | candidate | 1: N$46 != +12VA |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | 1 | 2 | 0.5 | candidate | 1: N$157 != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | 1 | 2 | 0.5 | candidate | 1: N$157 != +12VA |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | 1 | 2 | 0.5 | candidate | 1: /Internal Reference Source/SRC_OUT != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | 1 | 2 | 0.5 | candidate | 1: /Internal Reference Source/SRC_OUT != +12VA |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | 5 | 12 | 0.4167 | candidate | 1: +5VP != +12VA; 12: /Internal Reference Source/DAC_CLK != GND; 14: /Internal Reference Source/DAC_D13 != +5VP |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | 1 | 4 | 0.25 | candidate | 1: +5VP != N$5; 2: GND != N$5; 3: +5VP != GND |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | 1 | 4 | 0.25 | candidate | 1: +12VA != N$5; 2: GND != N$5; 3: -12VA != GND |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | 0 | 2 | 0.0 | candidate | 1: N$46 != N$5; 2: GND != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | 0 | 2 | 0.0 | candidate | 1: N$157 != N$5; 2: GND != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | 0 | 2 | 0.0 | candidate | 1: N$64 != N$5; 2: N$61 != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | 0 | 2 | 0.0 | candidate | 1: N$64 != N$5; 2: N$61 != GND |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | 0 | 2 | 0.0 | candidate | 1: N$64 != +12VA; 2: N$61 != GND |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | 0 | 2 | 0.0 | candidate | 1: /Internal Reference Source/SRC_OUT != N$5; 2: GND != N$5 |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 60 | 0.0 | candidate | 1: +5VP != VCC_5V_BTBIN; 10: GND != DXN_0; 11: GND != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 16 | 0.0 | candidate | 1: +12VA != VCC_5V_BTBIN; 10: GND != DXN_0; 11: GND != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 10 | 0.0 | candidate | 1: +12VA != MCU_SWCLK; 10: GND != DXN_0; 2: GND != MCU_SWCLK |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 6 | 0.0 | candidate | 1: +5VP != MCU_SWCLK; 10: GND != DXN_0; 2: GND != MCU_SWCLK |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 6 | 0.0 | candidate | 1: +12VA != VCC_SCEEN_LPOWER; 2: GND != SCREEN_UART_TX_R; 3: -12VA != SCREEN_UART_RX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 5 | 0.0 | candidate | 1: +5VP != RS485_A_R; 2: GND != RS485_B_R; 3: +5VP != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 5 | 0.0 | candidate | 1: +5VP != RS232_RX_R; 2: GND != RS232_TX_R; 3: +5VP != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 5 | 0.0 | candidate | 1: +5VP != VCC_SCEEN_LPOWER; 2: GND != SCREEN_UART_TX_R; 3: +5VP != SCREEN_UART_RX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 5 | 0.0 | candidate | 1: +12VA != RS485_A_R; 2: GND != RS485_B_R; 3: -12VA != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 5 | 0.0 | candidate | 1: +12VA != RS232_RX_R; 2: GND != RS232_TX_R; 3: -12VA != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J101 (Connector_Generic:Conn_02x40_Odd_Even) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 3 | 0.0 | candidate | 1: +5VP != DBG_MCU_SWCLK; 2: GND != DBG_MCU_SWDIO; 3: +5VP != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J102 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 3 | 0.0 | candidate | 1: +12VA != DBG_MCU_SWCLK; 2: GND != DBG_MCU_SWDIO; 3: -12VA != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: N$46 != RS485_A_R; 2: GND != RS485_B_R |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: N$46 != RS232_RX_R; 2: GND != RS232_TX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 2 | 0.0 | candidate | 1: N$46 != VCC_5V_BTBIN; 2: GND != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 2 | 0.0 | candidate | 1: N$46 != DBG_MCU_SWCLK; 2: GND != DBG_MCU_SWDIO |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 2 | 0.0 | candidate | 1: N$46 != MCU_SWCLK; 2: GND != MCU_SWCLK |
| Lock-In-Amplifier_MainBoard_V0.1 J201 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 2 | 0.0 | candidate | 1: N$46 != VCC_SCEEN_LPOWER; 2: GND != SCREEN_UART_TX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: N$157 != RS485_A_R; 2: GND != RS485_B_R |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: N$157 != RS232_RX_R; 2: GND != RS232_TX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 2 | 0.0 | candidate | 1: N$157 != VCC_5V_BTBIN; 2: GND != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 2 | 0.0 | candidate | 1: N$157 != DBG_MCU_SWCLK; 2: GND != DBG_MCU_SWDIO |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 2 | 0.0 | candidate | 1: N$157 != MCU_SWCLK; 2: GND != MCU_SWCLK |
| Lock-In-Amplifier_MainBoard_V0.1 J202 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 2 | 0.0 | candidate | 1: N$157 != VCC_SCEEN_LPOWER; 2: GND != SCREEN_UART_TX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: N$64 != RS485_A_R; 2: N$61 != RS485_B_R |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: N$64 != RS232_RX_R; 2: N$61 != RS232_TX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 2 | 0.0 | candidate | 1: N$64 != VCC_5V_BTBIN; 2: N$61 != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 2 | 0.0 | candidate | 1: N$64 != DBG_MCU_SWCLK; 2: N$61 != DBG_MCU_SWDIO |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 2 | 0.0 | candidate | 1: N$64 != MCU_SWCLK; 2: N$61 != MCU_SWCLK |
| Lock-In-Amplifier_MainBoard_V0.1 J401 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 2 | 0.0 | candidate | 1: N$64 != VCC_SCEEN_LPOWER; 2: N$61 != SCREEN_UART_TX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: /Internal Reference Source/SRC_OUT != RS485_A_R; 2: GND != RS485_B_R |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: /Internal Reference Source/SRC_OUT != RS232_RX_R; 2: GND != RS232_TX_R |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 2 | 0.0 | candidate | 1: /Internal Reference Source/SRC_OUT != VCC_5V_BTBIN; 2: GND != DXN_0 |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 2 | 0.0 | candidate | 1: /Internal Reference Source/SRC_OUT != DBG_MCU_SWCLK; 2: GND != DBG_MCU_SWDIO |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 2 | 0.0 | candidate | 1: /Internal Reference Source/SRC_OUT != MCU_SWCLK; 2: GND != MCU_SWCLK |
| Lock-In-Amplifier_MainBoard_V0.1 J701 (Connector:Conn_Coaxial) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 2 | 0.0 | candidate | 1: /Internal Reference Source/SRC_OUT != VCC_SCEEN_LPOWER; 2: GND != SCREEN_UART_TX_R |
| Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 16 | 0.0 | candidate | 1: +12VA != VCC_5V_BTBIN; 10: GND != DXN_0; 11: GND != DXN_0 |
| Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 10 | 0.0 | candidate | 1: +12VA != MCU_SWCLK; 10: GND != DXN_0; 2: GND != MCU_SWCLK |
| Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 6 | 0.0 | candidate | 1: +12VA != VCC_SCEEN_LPOWER; 2: GND != SCREEN_UART_TX_R; 3: -12VA != SCREEN_UART_RX_R |
| Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 5 | 0.0 | candidate | 1: +12VA != RS485_A_R; 2: GND != RS485_B_R; 3: -12VA != DXN_0 |
| Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 5 | 0.0 | candidate | 1: +12VA != RS232_RX_R; 2: GND != RS232_TX_R; 3: -12VA != DXN_0 |
| Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 4 | 0.0 | candidate | 1: N$5 != RS485_A_R; 2: N$5 != RS485_B_R; 3: GND != DXN_0 |
| Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 4 | 0.0 | candidate | 1: N$5 != RS232_RX_R; 2: N$5 != RS232_TX_R; 3: GND != DXN_0 |
| Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 4 | 0.0 | candidate | 1: N$5 != VCC_5V_BTBIN; 2: N$5 != DXN_0; 3: GND != VCC_5V_BTBIN |
| Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 4 | 0.0 | candidate | 1: N$5 != MCU_SWCLK; 2: N$5 != MCU_SWCLK; 3: GND != JTAG_VREF |
| Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 4 | 0.0 | candidate | 1: N$5 != VCC_SCEEN_LPOWER; 2: N$5 != SCREEN_UART_TX_R; 3: GND != SCREEN_UART_RX_R |
| Lock-In-Amplifier_PowerBoard_V0.1 J101 (Connector_Generic:Conn_01x04) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 3 | 0.0 | candidate | 1: N$5 != DBG_MCU_SWCLK; 2: N$5 != DBG_MCU_SWDIO; 3: GND != DXN_0 |
| Lock-In-Amplifier_PowerBoard_V0.1 J103 (Connector_Generic:Conn_01x16) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 3 | 0.0 | candidate | 1: +12VA != DBG_MCU_SWCLK; 2: GND != DBG_MCU_SWDIO; 3: -12VA != DXN_0 |
| Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN1 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: N$5 != RS485_A_R; 2: GND != RS485_B_R |
| Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN2 (HX-GH1.25-3PWT) | 0 | 2 | 0.0 | candidate | 1: N$5 != RS232_RX_R; 2: GND != RS232_TX_R |
| Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd CN7 (X0802FVS-80AS-LPV01) | 0 | 2 | 0.0 | candidate | 1: N$5 != VCC_5V_BTBIN; 2: GND != DXN_0 |
| Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd H5 (PinHeader_1x03_P2.54mm_Vertical) | 0 | 2 | 0.0 | candidate | 1: N$5 != DBG_MCU_SWCLK; 2: GND != DBG_MCU_SWDIO |
| Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U16 (ZX-SH1.0-8PWT) | 0 | 2 | 0.0 | candidate | 1: N$5 != MCU_SWCLK; 2: GND != MCU_SWCLK |
| Lock-In-Amplifier_PowerBoard_V0.1 J102 (Connector:Barrel_Jack) | EmoeSOM_A7_DDR_RevA-锁定放大器专用4层.brd U9 (WAFER-GH1.25-4PWB) | 0 | 2 | 0.0 | candidate | 1: N$5 != VCC_SCEEN_LPOWER; 2: GND != SCREEN_UART_TX_R |

> 说明：同名网络逐 pin 一致仍只是候选证据；只有用户声明或工程 metadata
> 声明连接器对插后才应视为 confirmed。