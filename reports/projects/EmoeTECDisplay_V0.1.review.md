# KiCad 原理图审查报告 — EmoeTECDisplay_V0.1.review

> 由 kicad-sch-reader 自动生成，根原理图：`D:\MyProjects\EmoeR_D\NIM\EmoeTEController\0_HW\EmoeTECDisplay_V0.1`

## 1. 工程概览

| 项目 | 值 |
| --- | --- |
| 图纸页数 | 1 |
| 元件符号数 | 60 |
| 网络数 | 17（命名网络 15） |
| 已解析引脚连接数 | 109 |
| 发现问题总数 | 21 |
| 问题分级 | error=2 / warning=19 / info=0 |
| KiCad ERC | errors=2, warnings=18 |

### 图纸清单

| 路径 | 文件 | 标题 | 元件 | 导线 | 标签 | 连接点 | NC | 版本/生成器 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `/` | `EmoeTECDisplay_V0.1.kicad_sch` |  | 60 | 80 | 41 | 8 | 0 | 20260306 / eeschema 10.0 |

## 2. 网络清单（按名称）

| 网络 | 引脚数 | 所在图纸 | 引脚示例 |
| --- | --- | --- | --- |
| /EXTOB_IO0 | 5 | / | SW101.2, R104.2, C101.2, D101.1, J101.3 |
| /EXTOB_IO1 | 5 | / | SW102.2, R103.2, D102.1, C102.2, J101.5 |
| /EXTOB_IO2 | 5 | / | R102.2, SW103.2, C103.2, D103.1, J101.7 |
| /EXTOB_IO3 | 5 | / | C104.2, D104.1, J101.9, SW104.2, R101.2 |
| /LCD_BL | 2 | / | J101.10, R105.1 |
| /LCD_DC | 2 | / | J101.8, J102.7 |
| /LCD_RST | 3 | / | J102.11, R108.2, C105.1 |
| /LEDK | 2 | / | J102.2, R107.1 |
| /NRST | 2 | / | J103.1, J101.16 |
| /PB13 | 2 | / | J101.14, J102.9 |
| /PB15 | 2 | / | J101.6, J102.10 |
| /SWCLK | 2 | / | J101.13, J103.2 |
| /SWDIO | 2 | / | J101.15, J103.3 |
| GND | 48 | / | J102.12, #PWR0123.1, #PWR0102.1, J101.11, #PWR0103.1, SW101.1, … |
| N$17 | 3 | / | R105.2, R106.1, Q101.1 |
| N$8 | 2 | / | Q101.3, R107.2 |
| VDD | 17 | / | #PWR0120.1, J102.3, J102.4, #PWR0111.1, R104.1, R101.1, … |

## 3. 设计审查发现

### 错误（2）

| # | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |
| 2 | `/` | ERC-power_pin_not_driven | Input Power pin not driven by any Output Power pins |  | official |

### 警告（19）

| # | 位置 | 代码 | 说明 | 网络 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | `/` | R603 | 图纸 / 的 title_block 缺少全部关键字段（title/date/rev/company） |  | declared |
| 2 | `/` | ERC-multiple_net_names | EXTOB_IO0 和 USBFS_D- 都连接到同一项上; 将使用 EXTOB_IO0 作为网表中的网络名称 |  | official |
| 3 | `/` | ERC-multiple_net_names | EXTOB_IO1 和 USBFS_D+ 都连接到同一项上; 将使用 EXTOB_IO1 作为网表中的网络名称 |  | official |
| 4 | `/` | ERC-multiple_net_names | EXTOB_IO2 和 PA7 都连接到同一项上; 将使用 EXTOB_IO2 作为网表中的网络名称 |  | official |
| 5 | `/` | ERC-multiple_net_names | EXTOB_IO3 和 PA4 都连接到同一项上; 将使用 EXTOB_IO3 作为网表中的网络名称 |  | official |
| 6 | `/` | ERC-multiple_net_names | GND 和 SPI2_CS 都连接到同一项上; 将使用 GND 作为网表中的网络名称 |  | official |
| 7 | `/` | ERC-lib_symbol_mismatch | 符号 'VDD' 与来源库 'power' 中的符号存在差异 |  | official |
| 8 | `/` | ERC-lib_symbol_mismatch | 符号 'VDD' 与来源库 'power' 中的符号存在差异 |  | official |
| 9 | `/` | ERC-multiple_net_names | LCD_DC 和 PB12 都连接到同一项上; 将使用 LCD_DC 作为网表中的网络名称 |  | official |
| 10 | `/` | ERC-multiple_net_names | LCD_BL 和 PC13 都连接到同一项上; 将使用 LCD_BL 作为网表中的网络名称 |  | official |
| 11 | `/` | ERC-lib_symbol_mismatch | 符号 'VDD' 与来源库 'power' 中的符号存在差异 |  | official |
| 12 | `/` | ERC-lib_symbol_mismatch | 符号 'VDD' 与来源库 'power' 中的符号存在差异 |  | official |
| 13 | `/` | ERC-lib_symbol_mismatch | 符号 'VDD' 与来源库 'power' 中的符号存在差异 |  | official |
| 14 | `/` | ERC-lib_symbol_mismatch | 符号 'VDD' 与来源库 'power' 中的符号存在差异 |  | official |
| 15 | `/` | ERC-lib_symbol_mismatch | 符号 'VDD' 与来源库 'power' 中的符号存在差异 |  | official |
| 16 | `/` | ERC-lib_symbol_mismatch | 符号 'VDD' 与来源库 'power' 中的符号存在差异 |  | official |
| 17 | `/` | ERC-multiple_net_names | VDD 和 LEDA 都连接到同一项上; 将使用 VDD 作为网表中的网络名称 |  | official |
| 18 | `/` | ERC-multiple_net_names | PB13 和 SPI2_SCK 都连接到同一项上; 将使用 PB13 作为网表中的网络名称 |  | official |
| 19 | `/` | ERC-multiple_net_names | PB15 和 SPI2_MOSI 都连接到同一项上; 将使用 PB15 作为网表中的网络名称 |  | official |

## 4. 工具与方法说明

- 网络表由纯 Python 几何连通域构建（导线端点 + 连接点 + 标签 + 电源符号），并完成分层图纸与全局标签合并。
- KiCad ERC 已运行: {'error': 2, 'warning': 18}
- 悬空/单引脚等判定基于本工具解析结果；KiCad ERC 结果（如已运行）以 ERC-* 代码单独列出。
- 报告中的 info 级发现需要人工结合设计意图判断，不代表设计错误。
- 发现条目带"依据"级别：official=官方 ERC 转写；structural=原理图结构事实；declared=字段约定检查；heuristic=启发式建议（可结合设计意图忽略）。
