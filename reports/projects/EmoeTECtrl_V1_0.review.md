# KiCad 原理图审查报告 — EmoeTECtrl_V1_0.review

> 由 kicad-sch-reader 自动生成，根原理图：`D:\MyProjects\EmoeR_D\NIM\EmoeTEController\0_HW\EmoeTECtrl_V1_0`

## 1. 工程概览

| 项目 | 值 |
| --- | --- |
| 图纸页数 | 8 |
| 元件符号数 | 374 |
| 网络数 | 118（命名网络 72） |
| 已解析引脚连接数 | 743 |
| 发现问题总数 | 80 |
| 问题分级 | error=25 / warning=18 / info=37 |
| KiCad ERC | errors=24, warnings=6 |

### 图纸清单

| 路径 | 文件 | 标题 | 元件 | 导线 | 标签 | 连接点 | NC | 版本/生成器 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `/` | `TEC Controller.kicad_sch` |  | 64 | 180 | 24 | 25 | 0 | 20260306 / eeschema 10.0 |
| `/668d544a-70e8-49ba-830c-d3873e1426ac` | `temp_sensor.kicad_sch` |  | 12 | 13 | 2 | 2 | 1 | 20260306 / eeschema 10.0 |
| `/6ede849c-c57a-4584-9fd2-0305562e0c11` | `current_sensing.kicad_sch` |  | 44 | 83 | 18 | 18 | 0 | 20260306 / eeschema 10.0 |
| `/76f28ac8-dd4b-4e99-b6e2-7e48909a0eb9` | `reference.kicad_sch` |  | 15 | 23 | 3 | 5 | 0 | 20260306 / eeschema 10.0 |
| `/9b345fb7-9566-4c4a-87ad-930dc3cdfe3e` | `power_stage.kicad_sch` |  | 28 | 70 | 19 | 11 | 0 | 20260306 / eeschema 10.0 |
| `/db77e02f-7774-4e79-bc53-5ef64c521c93` | `adc_block.kicad_sch` |  | 51 | 128 | 21 | 27 | 2 | 20260306 / eeschema 10.0 |
| `/e9a395f6-50a7-4d75-ad99-f567ff82083f` | `power_interface.kicad_sch` |  | 60 | 109 | 29 | 25 | 5 | 20260306 / eeschema 10.0 |
| `/fa325fb8-dd79-4291-b8c1-e39eddcb6818` | `controller.kicad_sch` |  | 100 | 222 | 191 | 21 | 2 | 20260306 / eeschema 10.0 |

## 2. 网络清单（按名称）

| 网络 | 引脚数 | 所在图纸 | 引脚示例 |
| --- | --- | --- | --- |
| /ADC Block/MISO | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R310.2, U1.41 |
| /ADC Block/MOSI | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R306.2, U1.42 |
| /ADC Block/SCLK | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R309.2, U1.40 |
| /Controller/ADC_DRDY | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R311.2, R3.1 |
| /Controller/ADC_RST | 3 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | U301.4, R4.1, C13.1 |
| /Controller/ADC_START | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | U301.15, R7.1 |
| /Controller/I_SENSE1 | 3 | /6ede849c-c57a-4584-9fd2-0305562e0c11, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R401.1, C402.1, U1.9 |
| /Controller/I_SENSE2 | 3 | /6ede849c-c57a-4584-9fd2-0305562e0c11, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | C403.1, R402.1, U1.14 |
| /Controller/SPI_CS1 | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U301.16, R2.1 |
| /Controller/USART1_RX | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U4.7, U1.43 |
| /Controller/USART1_TX | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U4.6, U1.32 |
| /Controller/V_SENSE1 | 4 | /6ede849c-c57a-4584-9fd2-0305562e0c11, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | C405.2, R410.1, R403.2, U1.8 |
| /Controller/V_SENSE2 | 4 | /6ede849c-c57a-4584-9fd2-0305562e0c11, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R409.1, C408.2, R404.2, U1.13 |
| /Current Sensing/IN+ | 7 | /6ede849c-c57a-4584-9fd2-0305562e0c11, /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e | R405.2, U6.2, C204.1, C201.1, C206.1, L201.1, … |
| /Current Sensing/IN- | 7 | /6ede849c-c57a-4584-9fd2-0305562e0c11, /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e | U5.2, R406.2, C201.2, L202.1, C205.1, C207.1, … |
| /Digital Temp Sensor/SCL | 5 | /668d544a-70e8-49ba-830c-d3873e1426ac, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R803.1, U801.1, U601.1, R6.1, U1.39 |
| /Digital Temp Sensor/SDA | 5 | /668d544a-70e8-49ba-830c-d3873e1426ac, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U801.6, R802.2, U1.44, U601.3, R5.2 |
| /EXTOB_IO0 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J3.3, U1.33 |
| /EXTOB_IO1 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J3.5, U1.34 |
| /EXTOB_IO2 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U1.15, J3.7 |
| /EXTOB_IO3 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J3.9, U1.12 |
| /FLASH_CLK | 1 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U501.6 |
| /FLASH_CS | 1 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U501.1 |
| /FLASH_IO0 | 1 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U501.5 |
| /FLASH_IO1 | 1 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U501.2 |
| /GPIO1 | 4 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J102.3, D501.10, U1.17, D501.1 |
| /GPIO2 | 4 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J102.4, U1.16, D501.2, D501.9 |
| /GPIO3 | 4 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J102.5, D501.7, D501.4, U1.25 |
| /GPIO4 | 4 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J102.6, U1.22, D501.5, D501.6 |
| /LCD_BL | 3 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J3.10, R511.1, U1.2 |
| /LCD_DC | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U1.26, J3.8 |
| /LED1 | 6 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R3.2, R510.1, R508.2, U1.18, R8.2, R509.1 |
| /MCU485_RX | 3 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U503.1, U1.11, R507.2 |
| /MCU485_TX | 3 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U503.4, U1.10, R506.1 |
| /MCU_485_EN | 6 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | C502.2, R503.1, R8.1, R505.2, J3.16, U1.7 |
| /OBJ IA | 3 | /, /db77e02f-7774-4e79-bc53-5ef64c521c93 | J101.1, R301.1, C15.2 |
| /OBJ IB | 3 | /, /db77e02f-7774-4e79-bc53-5ef64c521c93 | J101.2, R302.1, C16.1 |
| /OBJ UA | 4 | /, /db77e02f-7774-4e79-bc53-5ef64c521c93 | J101.3, C15.1, U301.9, C14.1 |
| /OBJ UB | 5 | /, /db77e02f-7774-4e79-bc53-5ef64c521c93 | J101.4, R_{REF}301.2, C16.2, R303.1, C14.2 |
| /OUT+ | 5 | /, /6ede849c-c57a-4584-9fd2-0305562e0c11 | J101.10, R405.1, U6.3, R403.1, C401.1 |
| /OUT- | 5 | /, /6ede849c-c57a-4584-9fd2-0305562e0c11 | J101.9, U5.3, R406.1, C401.2, R404.1 |
| /PA13 | 3 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J3.15, U1.37, R512.1 |
| /PA14 | 3 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U1.38, J3.13, R513.1 |
| /PB13 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U1.27, J3.14 |
| /PB15 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U1.29, J3.6 |
| /Power Stage/PWM1 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U201.8, U1.30 |
| /Power Stage/PWM2 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U202.8, U1.31 |
| /Power Stage/SKIP1 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U201.1, U1.3 |
| /Power Stage/SKIP2 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U202.1, U1.4 |
| /Power Stage/VCC_4V7_REG | 10 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e, /e9a395f6-50a7-4d75-ad99-f567ff82083f | U201.2, U202.2, C211.1, C210.1, C7.1, R202.1, … |
| /RS485_A | 7 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J102.9, R107.2, U503.6, D502.7, R506.2, D502.4, … |
| /RS485_B | 7 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J102.10, U503.7, R108.1, D502.6, R105.2, R507.1, … |
| /SHIELD | 3 | / | R102.2, C101.1, J101.5 |
| /SINK A | 5 | / | D101.1, L102.2, C103.1, R101.2, J101.6 |
| /SINK B | 4 | / | D101.2, C103.2, L101.1, J101.7 |
| /SINK SENSE | 3 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | C107.2, R103.1, U1.28 |
| /TTL_RX | 5 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J102.7, D502.1, D502.10, R504.2, U1.45 |
| /TTL_TX | 4 | /, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | J102.8, U1.46, D502.2, D502.9 |
| /USBC_D+ | 5 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | J1.A6, J1.B6, U3.3, U3.4, R606.1 |
| /USBC_D- | 5 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | J1.A7, J1.B7, U3.1, R607.2, U3.6 |
| /USBTTL_RXD | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | U602.9, U4.3 |
| /USBTTL_TXD | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | U602.8, U4.2 |
| /VBUS_USB_5V | 10 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | U4.1, C611.1, C608.1, C605.1, U602.7, J1.A4, … |
| /VCC_4V7_F | 5 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | C610.1, C10.1, U603.1, U603.3, FB1.2 |
| /VDDA_3V3_MCU | 4 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | C510.2, U1.21, FB501.1, C508.2 |
| /VREF_2V5 | 8 | /, /6ede849c-c57a-4584-9fd2-0305562e0c11, /76f28ac8-dd4b-4e99-b6e2-7e48909a0eb9, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | C102.1, R101.1, U5.7, U6.7, C705.1, C704.1, … |
| GND | 258 | /, /668d544a-70e8-49ba-830c-d3873e1426ac, /6ede849c-c57a-4584-9fd2-0305562e0c11, /76f28ac8-dd4b-4e99-b6e2-7e48909a0eb9 | #PWR034.1, R102.1, #PWR0104.1, #PWR0119.1, C107.1, #PWR0117.1, … |
| GNDS | 24 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | J1.A1, J1.A12, J1.B1, J1.B12, J1.S1, #PWR0603.1, … |
| N$102 | 3 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | Y1.3, U1.5, C1.2 |
| N$103 | 3 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | Y1.1, U1.6, C2.2 |
| N$104 | 4 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | U2.6, L1.2, D201.1, C5.2 |
| N$105 | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | U2.1, C5.1 |
| N$106 | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | U2.4, R201.2 |
| N$117 | 2 | /6ede849c-c57a-4584-9fd2-0305562e0c11 | U5.8, R402.2 |
| N$118 | 2 | /6ede849c-c57a-4584-9fd2-0305562e0c11 | U6.8, R401.2 |
| N$23 | 2 | / | J102.1, F1.2 |
| N$25 | 3 | / | L102.1, C104.1, R103.2 |
| N$26 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e | L201.2, U201.4 |
| N$31 | 2 | / | H103.1, C114.2 |
| N$32 | 3 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | L301.2, FB301.1, C314.2 |
| N$34 | 4 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | R301.2, C303.1, C304.1, U301.10 |
| N$38 | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | U301.20, R309.1 |
| N$39 | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | U301.18, R310.1 |
| N$40 | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | U301.17, R311.1 |
| N$47 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | U501.7, R501.1 |
| N$5 | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | R600.1, J1.A5 |
| N$50 | 3 | / | R106.2, H104.1, C115.2 |
| N$51 | 4 | /76f28ac8-dd4b-4e99-b6e2-7e48909a0eb9 | FB701.1, R701.1, C701.1, C702.1 |
| N$53 | 3 | /76f28ac8-dd4b-4e99-b6e2-7e48909a0eb9 | R701.2, U701.1, C703.1 |
| N$54 | 2 | /668d544a-70e8-49ba-830c-d3873e1426ac | R801.1, U801.4 |
| N$58 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e | U202.6, C209.1 |
| N$59 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e | U202.7, C209.2 |
| N$60 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e | U202.4, L202.2 |
| N$61 | 4 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | R302.2, C303.2, C305.2, U301.11 |
| N$62 | 4 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | R203.2, U2.3, R202.2, C8.1 |
| N$64 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R502.2, U501.3 |
| N$65 | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | U602.10, C604.1 |
| N$68 | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | U602.1, R606.2 |
| N$69 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e | C208.1, U201.6 |
| N$70 | 2 | /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e | C208.2, U201.7 |
| N$74 | 4 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | C306.1, C307.1, R303.2, U301.5 |
| N$76 | 2 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | R306.1, U301.19 |
| N$77 | 4 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | C308.2, C306.2, R304.2, U301.6 |
| N$8 | 2 | / | H101.1, C112.2 |
| N$81 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | D504.2, R509.2 |
| N$84 | 3 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R505.1, U503.2, U503.3 |
| N$85 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | D506.2, R512.2 |
| N$86 | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | R607.1, U602.2 |
| N$87 | 2 | / | C113.2, H102.1 |
| N$89 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R511.2, D505.2 |
| N$90 | 3 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | C312.2, C311.2, U301.7 |
| N$91 | 5 | /db77e02f-7774-4e79-bc53-5ef64c521c93 | C313.2, L301.1, C309.1, C310.1, U301.14 |
| N$92 | 2 | /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | R513.2, D507.2 |
| N$96 | 2 | /e9a395f6-50a7-4d75-ad99-f567ff82083f | J1.B5, R1.1 |
| VCC | 15 | /6ede849c-c57a-4584-9fd2-0305562e0c11 | #PWR0422.1, C409.1, U5.5, #PWR0408.1, #PWR0417.1, C407.1, … |
| VDD | 54 | /, /668d544a-70e8-49ba-830c-d3873e1426ac, /e9a395f6-50a7-4d75-ad99-f567ff82083f, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | #PWR0115.1, C801.1, #PWR0806.1, U801.5, #PWR0801.1, R803.2, … |
| VDDA | 18 | /, /6ede849c-c57a-4584-9fd2-0305562e0c11, /76f28ac8-dd4b-4e99-b6e2-7e48909a0eb9, /db77e02f-7774-4e79-bc53-5ef64c521c93 | #PWR0114.1, L401.2, C411.2, #PWR0427.1, FB701.2, #PWR0303.1, … |
| VIN | 17 | /, /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e, /e9a395f6-50a7-4d75-ad99-f567ff82083f, /fa325fb8-dd79-4291-b8c1-e39eddcb6818 | C105.1, C110.1, F1.1, C116.1, D1.1, #PWR0121.1, … |

## 3. 设计审查发现

### 错误（25）

| # | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` | R401 | 网络被命名为多个全局网络: GND, GNDA, GNDD；当前工具暂按 'GND' 归并，请用 KiCad ERC 复核 | GND | structural |
| 2 | `/Controller/ / J2.1` | ERC-pin_not_connected | Pin not connected |  | official |
| 3 | `/Controller/ / J2.10` | ERC-pin_not_connected | Pin not connected |  | official |
| 4 | `/Controller/ / J2.11` | ERC-pin_not_connected | Pin not connected |  | official |
| 5 | `/Controller/ / J2.12` | ERC-pin_not_connected | Pin not connected |  | official |
| 6 | `/Controller/ / J2.13` | ERC-pin_not_connected | Pin not connected |  | official |
| 7 | `/Controller/ / J2.14` | ERC-pin_not_connected | Pin not connected |  | official |
| 8 | `/Controller/ / J2.15` | ERC-pin_not_connected | Pin not connected |  | official |
| 9 | `/Controller/ / J2.16` | ERC-pin_not_connected | Pin not connected |  | official |
| 10 | `/Controller/ / J2.17` | ERC-pin_not_connected | Pin not connected |  | official |
| 11 | `/Controller/ / J2.18` | ERC-pin_not_connected | Pin not connected |  | official |
| 12 | `/Controller/ / J2.19` | ERC-pin_not_connected | Pin not connected |  | official |
| 13 | `/Controller/ / J2.2` | ERC-pin_not_connected | Pin not connected |  | official |
| 14 | `/Controller/ / J2.20` | ERC-pin_not_connected | Pin not connected |  | official |
| 15 | `/Controller/ / J2.3` | ERC-pin_not_connected | Pin not connected |  | official |
| 16 | `/Controller/ / J2.4` | ERC-pin_not_connected | Pin not connected |  | official |
| 17 | `/Controller/ / J2.5` | ERC-pin_not_connected | Pin not connected |  | official |
| 18 | `/Controller/ / J2.6` | ERC-pin_not_connected | Pin not connected |  | official |
| 19 | `/Controller/ / J2.7` | ERC-pin_not_connected | Pin not connected |  | official |
| 20 | `/Controller/ / J2.8` | ERC-pin_not_connected | Pin not connected |  | official |
| 21 | `/Controller/ / J2.9` | ERC-pin_not_connected | Pin not connected |  | official |
| 22 | `/Controller/ / J2.MP` | ERC-pin_not_connected | Pin not connected |  | official |
| 23 | `/Controller/ / U501.1` | ERC-pin_not_driven | Input pin not driven by any Output pins |  | official |
| 24 | `/Controller/ / U501.6` | ERC-pin_not_driven | Input pin not driven by any Output pins |  | official |
| 25 | `/Power and Interface/ / U4.3` | ERC-pin_not_driven | Input pin not driven by any Output pins |  | official |

### 警告（18）

| # | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` | R603 | 图纸 / 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 2 | `/` | ERC-footprint_link_issues | 在库 'Package_SO' 中找不到封装 'SOIC-8_5.23x5.23mm_P1.27mm' |  | official |
| 3 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 4 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 5 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 6 | `/` | ERC-isolated_pin_label | Label connected to only one pin |  | official |
| 7 | `/668d544a-70e8-49ba-830c-d3873e1426ac` | R603 | 图纸 /668d544a-70e8-49ba-830c-d3873e1426ac 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 8 | `/6ede849c-c57a-4584-9fd2-0305562e0c11` | R603 | 图纸 /6ede849c-c57a-4584-9fd2-0305562e0c11 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 9 | `/76f28ac8-dd4b-4e99-b6e2-7e48909a0eb9` | R603 | 图纸 /76f28ac8-dd4b-4e99-b6e2-7e48909a0eb9 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 10 | `/9b345fb7-9566-4c4a-87ad-930dc3cdfe3e` | R603 | 图纸 /9b345fb7-9566-4c4a-87ad-930dc3cdfe3e 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 11 | `/Controller/` | ERC-same_local_global_label | Local and global labels have same name |  | official |
| 12 | `/db77e02f-7774-4e79-bc53-5ef64c521c93` | R603 | 图纸 /db77e02f-7774-4e79-bc53-5ef64c521c93 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 13 | `/e9a395f6-50a7-4d75-ad99-f567ff82083f` | R603 | 图纸 /e9a395f6-50a7-4d75-ad99-f567ff82083f 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 14 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818` | R603 | 图纸 /fa325fb8-dd79-4291-b8c1-e39eddcb6818 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 15 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / U501.1` | R302 | 网络 /FLASH_CS 只有 U501.1 一个连接点，请确认是否悬空或遗漏连接 | /FLASH_CS | structural |
| 16 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / U501.2` | R302 | 网络 /FLASH_IO1 只有 U501.2 一个连接点，请确认是否悬空或遗漏连接 | /FLASH_IO1 | structural |
| 17 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / U501.5` | R302 | 网络 /FLASH_IO0 只有 U501.5 一个连接点，请确认是否悬空或遗漏连接 | /FLASH_IO0 | structural |
| 18 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / U501.6` | R302 | 网络 /FLASH_CLK 只有 U501.6 一个连接点，请确认是否悬空或遗漏连接 | /FLASH_CLK | structural |

### 提示（37）

| # | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` | R103 | 1 个位号不符合 字母前缀+数字 规范（如 DA、2、R_1）: R_{REF}301 |  | heuristic |
| 2 | `/` | R103 | 7 个前缀的位号有缺号: C 缺709（C1..C801；段内缺号: C9, C106, C503, C504, C505, C506, C515, C516 …(+4)）, D 缺498（D1..D507；段内缺号: D503）, FB 缺696（FB1..FB701）, J 缺97（J1..J102）, L 缺394（L1..L401）, R 缺749（R1..R803；段内缺号: R104, R305, R307, R308, R407, R408, R601, R602 …(+3)）, U 缺785（U1..U801；段内缺号: U502）。跨页编 hundreds 的工程跨段空号属正常（按页分段编号），段内缺号通常是迭代删除，仅供审阅时参考 |  | heuristic |
| 3 | `/` | R402 | 项目有 46 个未命名网络（N$，占网络总数 39%）；关键信号建议命名以便跨页追踪与复查。最大的几个: N$91(5 脚); N$104(4 脚); N$34(4 脚); N$51(4 脚); N$61(4 脚) | N$91, N$104, N$34 | heuristic |
| 4 | `/` | R701 | 10 个器件标记为不焊接（DNP）: H101(MH), FID2(Fiducial), FID6(Fiducial), FID4(Fiducial), H104(MH), FID1(Fiducial), FID3(Fiducial), H103(MH), FID5(Fiducial), H102(MH)；其中 4 个为测试点/机械件，其余 6 个请确认 DNP 意图 |  | structural |
| 5 | `/ / D1` | R801 | D1（SM6T33A）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(A1)->VIN; 2(A2)->GND |  | structural |
| 6 | `/ / D101` | R801 | D101（BSD5C051V）有 2 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(A1)->/SINK A; 2(A2)->/SINK B |  | structural |
| 7 | `/668d544a-70e8-49ba-830c-d3873e1426ac / U801` | R304 | U801（TMP112AIDRLR）有 1 个引脚被标记为 no-connect: 3（类型 open_collector）；请对照手册确认这些脚确实可悬空 |  | structural |
| 8 | `/db77e02f-7774-4e79-bc53-5ef64c521c93` | R701 | 3 个器件标记为不焊接（DNP）: C15(3.3nF), C16(3.3nF), C14(3.3nF) |  | structural |
| 9 | `/db77e02f-7774-4e79-bc53-5ef64c521c93 / U301` | R304 | U301（ADS1247）有 2 个引脚被标记为 no-connect: 3, 12（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 10 | `/e9a395f6-50a7-4d75-ad99-f567ff82083f` | R701 | 2 个器件标记为不焊接（DNP）: D201(SS24FL), C8(100pF) |  | structural |
| 11 | `/e9a395f6-50a7-4d75-ad99-f567ff82083f / J1` | R304 | J1（GT-USB-7010AN）有 2 个引脚被标记为 no-connect: A8, B8（类型 bidirectional）；请对照手册确认这些脚确实可悬空 |  | structural |
| 12 | `/e9a395f6-50a7-4d75-ad99-f567ff82083f / U602` | R304 | U602（CH340E）有 3 个引脚被标记为 no-connect: 4, 5, 6（类型 input, output）；请对照手册确认这些脚确实可悬空 |  | structural |
| 13 | `/e9a395f6-50a7-4d75-ad99-f567ff82083f / U603` | R304 | U603（LP5907MFX-3.3）有 1 个引脚被标记为 no-connect: 4（类型 no_connect）；请对照手册确认这些脚确实可悬空 |  | structural |
| 14 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818` | R701 | 15 个器件标记为不焊接（DNP）: R506(DNP), R511(2.2k), R105(120R), R504(100k), D504(GREEN), R507(DNP), R502(10k), R8(22R), U501(W25Q16JVSSIQ), J2(FPC-05F-20PH20), D505(GREEN), C501(100nF), R3(22R), R509(2.2k), R501(10k) |  | structural |
| 15 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / D501` | R801 | D501（RCLAMP0524PATCT）有 9 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(?)->/GPIO1; 10(?)->/GPIO1; 2(?)->/GPIO2; 4(?)->/GPIO3; 5(?)->/GPIO4; 6(?)->/GPIO4 |  | structural |
| 16 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / D502` | R801 | D502（RCLAMP0524PATCT）有 9 个引脚名无法归一为阳极/阴极（A/K/C/+/-/ANODE/CATHODE 之外），涉及时请查手册确认极性: 1(?)->/TTL_RX; 10(?)->/TTL_RX; 2(?)->/TTL_TX; 4(?)->/RS485_A; 5(?)->/RS485_B; 6(?)->/RS485_B |  | structural |
| 17 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.1` | R301 | J2.1（Pin_1，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 18 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.10` | R301 | J2.10（Pin_10，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 19 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.11` | R301 | J2.11（Pin_11，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 20 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.12` | R301 | J2.12（Pin_12，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 21 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.13` | R301 | J2.13（Pin_13，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 22 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.14` | R301 | J2.14（Pin_14，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 23 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.15` | R301 | J2.15（Pin_15，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 24 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.16` | R301 | J2.16（Pin_16，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 25 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.17` | R301 | J2.17（Pin_17，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 26 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.18` | R301 | J2.18（Pin_18，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 27 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.19` | R301 | J2.19（Pin_19，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 28 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.2` | R301 | J2.2（Pin_2，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 29 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.20` | R301 | J2.20（Pin_20，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 30 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.3` | R301 | J2.3（Pin_3，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 31 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.4` | R301 | J2.4（Pin_4，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 32 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.5` | R301 | J2.5（Pin_5，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 33 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.6` | R301 | J2.6（Pin_6，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 34 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.7` | R301 | J2.7（Pin_7，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 35 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.8` | R301 | J2.8（Pin_8，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 36 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.9` | R301 | J2.9（Pin_9，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |
| 37 | `/fa325fb8-dd79-4291-b8c1-e39eddcb6818 / J2.MP` | R301 | J2.MP（MountPin，类型 passive）没有导线/标签连接，也未放置 no-connect 标记 |  | structural |

## 4. 工具与方法说明

- 网络表由纯 Python 几何连通域构建（导线端点 + 连接点 + 标签 + 电源符号），并完成分层图纸与全局标签合并。
- KiCad ERC 已运行: {'warning': 6, 'error': 24}
- 悬空/单引脚等判定基于本工具解析结果；KiCad ERC 结果（如已运行）以 ERC-* 代码单独列出。
- 报告中的 info 级发现需要人工结合设计意图判断，不代表设计错误。
- 发现条目带"依据"级别：official=官方 ERC 转写；structural=原理图结构事实；declared=字段约定检查；heuristic=启发式建议（可结合设计意图忽略）。
