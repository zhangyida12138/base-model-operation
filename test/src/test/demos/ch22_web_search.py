"""第 22 章：Agent + 搜索引擎。

web_search / fetch_url 基于 Tavily，需要在 .env 中配置 TAVILY_API_KEY。
未配置时下面会直接给出提示，不会真正发起请求。
"""

from agent.config import tavily_settings
from agent.tool.web import fetch_url, web_search

if __name__ == "__main__":
    if not tavily_settings.api_key:
        print("未配置 TAVILY_API_KEY，跳过联网演示。")
        print("在 .env 中补充 TAVILY_API_KEY=tvly-xxx 后重试。")
    else:
        print(web_search(query="Python 3.14 新特性")[:500])
        print(fetch_url(urls=["https://docs.python.org/3/whatsnew/3.14.html"])[:500])
