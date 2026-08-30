# kicad-sch-reader MCP 工具 schema 修复说明

修复日期：2026-08-30

## 问题现象

opencode 切换到 deepseek 模型后，新对话报错：

```
AI_APICallError: Invalid schema for function 'kicad-sch-reader_components':
["project"] is not of types "boolean", "object"
```

## 根因

`scripts/mcp_server.py` 的 `tools/list` 实现，把 `required` 数组错误地混进了
`inputSchema.properties`。生成出的错误 schema 长这样：

```json
"inputSchema": {
  "type": "object",
  "properties": {
    "project": {"type": "string"},
    "filter": {"type": "string"},
    "required": ["project"]
  },
  "required": ["project"]
}
```

严格校验 schema 的 provider（例如 deepseek）会把 `properties.required` 的值
`["project"]` 当成一个子 schema，而数组既不是 boolean 也不是 object，于是整个
对话流直接失败。该文件里的 10 个工具全部受影响，不只是 components。

## 修复

生成 schema 时，把 `required` 从 `properties` 中剔除，只保留真正的参数定义：

```python
elif method == "tools/list":
    _rpc(req_id, {"tools": [
        {"name": name, "description": desc, "inputSchema": {
            "type": "object",
            "properties": {k: v for k, v in props.items() if k != "required"},
            "required": props.get("required", []),
        }}
        for name, desc, props in _TOOL_META
    ]})
```

## 验证结果

- 10 个工具的 `properties` 中混入 `required` 的数量为 0
- `components` 的 schema 已是标准格式
- `python scripts/mcp_server.py --selftest`
  输出 `SELFTEST PASS: tools=10 parse sheets=5 GND nets=1`

## 留痕

- commit: d6af5f4
- 改前备份: scripts/mcp_server.py.bak_20260830_192559
