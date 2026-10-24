"""第 17 章：会话（Session）。

Session 持有 system 提示词、历史消息和工具定义，
并支持保存到 sessions/ 目录后按 id 重新加载。
"""

from agent.session import Session
from agent.tool import registry

if __name__ == "__main__":
    session = Session()  # 默认：渲染 system 提示词 + 注册全部工具
    print("会话 ID:", session.id)
    print("工具数量:", len(session.tools), "| registry:", len(registry.schemas()))

    session.add_message({"role": "user", "content": "你好，请介绍一下你自己"})
    session.print_friendly()

    # 持久化
    session.save()
    loaded = Session.load(session.id)
    print("重新加载后的消息条数:", len(loaded.messages))
