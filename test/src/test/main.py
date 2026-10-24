"""第 15 章：模型接口契约。

直接使用 OpenAI SDK 调用兼容接口，观察请求参数与流式响应。
后续章节（16 起）把这套调用封装进了 `src/agent`。
"""

import os

from openai import OpenAI

from test.utils import config
from test.utils.img_base64 import to_dataurl
from test.utils.stream_print import print_stream

client = OpenAI(
    api_key=config.OPENAI_API_KEY,
    base_url=config.OPENAI_BASE_URL,
)


def chat(text: str) -> None:
    """纯文本对话（流式）。"""
    stream = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "少思考，简洁回答"},
            {"role": "user", "content": text},
        ],
        stream=True,
    )
    print_stream(stream)


def chat_with_image(image_path: str, text: str = "请描述这张图片的内容") -> None:
    """多模态对话：把本地图片转成 data URL 后随文本一起发送。

    需要模型支持视觉输入，例如把 .env 中的 OPENAI_MODEL 换成视觉模型，
    并把 image_path 指向真实存在的图片（png / jpg / gif / webp）。
    """
    dataurl = to_dataurl(image_path)
    stream = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": {"url": dataurl}},
                ],
            }
        ],
        stream=True,
    )
    print_stream(stream)


if __name__ == "__main__":
    # 查看网关支持的模型
    print([m.id for m in client.models.list()])
    chat("从 1 数到 10")

    # 有图时再启用多模态示例
    # image_path = os.path.join(os.path.dirname(__file__), "menu.png")
    # if os.path.exists(image_path):
    #     chat_with_image(image_path)
