"""第 18/19 章：tools 与工具封装。

Tool 装饰器把普通函数包装成对象：
- schema() 生成 OpenAI 的 function calling 定义
- __call__ 先用 pydantic 校验参数，再执行函数，异常转成字符串返回
"""

import json

from agent.tool import registry

if __name__ == "__main__":
    print("注册的工具:", list(registry._tools))

    print("\n=== read_file 的 schema ===")
    schema = next(s for s in registry.schemas() if s["function"]["name"] == "read_file")
    print(json.dumps(schema, ensure_ascii=False, indent=2))

    print("\n=== 直接执行工具 ===")
    message = {
        "tool_calls": [
            {
                "id": "call_1",
                "function": {
                    "name": "read_file",
                    "arguments": json.dumps({"filepath": "README.md"}),
                },
            }
        ]
    }
    for result in registry.invoke(message) or []:
        print(result["role"], result["name"])
        print(result["content"][:80] or "(空)")
