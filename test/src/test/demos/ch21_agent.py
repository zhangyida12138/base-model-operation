"""第 21 章：Agent。

把第 20 章手写的 ReAct 循环封装进 Agent 类，
并通过监听器（ModelPrinterListener）以事件的方式实时打印流式输出。
"""

from agent.agent import Agent
from agent.printer import ModelPrinterListener

if __name__ == "__main__":
    agent = Agent(model_listener=ModelPrinterListener())
    agent.invoke("用 bash_command 执行 dir src 命令，然后简要告诉我 src 下有哪些目录")
    print("\n=== 会话 ===")
    agent.session.print_friendly()
