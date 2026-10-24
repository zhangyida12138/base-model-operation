"""第 20 章：ReAct。

ReAct = Reason + Act：模型先思考并决定调用工具，
执行工具把结果追加进会话，再让模型继续推理，直到不再需要工具。
这里手写这个循环，方便观察每一步的会话变化。
"""

from agent.model import Model
from agent.session import Session
from agent.tool import registry

if __name__ == "__main__":
    session = Session()
    session.add_message(
        {"role": "user", "content": "读取 README.md（如果为空就说文件为空）"}
    )
    model = Model()

    step = 0
    while True:
        step += 1
        result = model.invoke_stream(session)
        message = result.message
        print(f"[第 {step} 轮] assistant ->", message.get("content") or "(仅工具调用)")

        tool_messages = registry.invoke(session.messages[-1])
        if tool_messages is None:
            break

        for m in tool_messages:
            print(f"           tool {m['name']} -> {m['content'][:60]!r}")
        session.messages.extend(tool_messages)

    print("\n=== 最终会话 ===")
    session.print_friendly()
