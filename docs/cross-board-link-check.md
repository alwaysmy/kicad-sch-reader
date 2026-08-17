# 跨板连接器核对结果

命令：

```bat
python kicad-sch-reader.py link-check ^
  examples\Lock-In-Amplifier_MainBoard_V0.1 ^
  examples\Lock-In-Amplifier_PowerBoard_V0.1
```

## 结论

MainBoard 与 PowerBoard 之间可以通过连接器对识别：

| 候选对 | 型号 | 逐 pin 网络一致 | 差异 |
| --- | --- | --- | --- |
| **MainBoard J102 ↔ PowerBoard J103** | Conn_01x16 | **16 / 16** | 0 |
| MainBoard J101 ↔ PowerBoard J103 | Conn_02x40 vs Conn_01x16 | 5 / 16 | 11（非物理对插，忽略） |

因此 `J102 <-> J103` 是唯一完全一致的 16-pin 板间电源/信号连接候选：
+12VA、-12VA、+5VA、-5VA、+3.3V、+5VP、GND 等逐 pin 对齐。

## 边界说明

与 `lceda-sch-reader` 的连接器语义一致：**同名网络逐 pin 一致只是候选
证据**，实际是否对插、连接器方向与型号仍需要人工/LLM 确认。工具不会把
两个工程自动合并成一个网络空间。
