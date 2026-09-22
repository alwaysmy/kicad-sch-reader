# ChatGPT discussion: interface direction heuristic


结论：

IFC901 适合保留为通用启发式规则，但不应视为强语义/确定性 ERC。

建议：

通用层：interface_direction_semantics，默认 opt-in，或放入 strict/heuristic profile。

工程层：针对明确接口拓扑、FPGA 管脚角色、连接器定义，再做 project-specific rule。

严重度固定 info/warning，不要升级为 error。

默认排除 FPGA、连接器、双向口、差分网络，除非已有明确 pin-role 元数据。

IFC901 建议改成有语义的 ID，例如 SEM_INTERFACE_DIRECTION，避免和电阻位号混淆。

核心定位就是：通用规则负责发现可疑语义，工程规则负责判定是否真的接错。

