# agent-core 学习工程（第 15–23 章）

把课程 `15. 模型接口契约` → `23. Skill` 的示例代码整理到这个 uv 工程里，形成一份可以持续演进的
Agent 实现。

- `src/test/` —— 第 15 章的原始接口调用示例（`main.py`）
- `src/agent/` —— 第 16–23 章逐步累积出来的 Agent 实现（最终形态即第 23 章）
- `src/test/demos/` —— 对应各章知识点的可运行示例

> `uv_build` 的 editable 安装会把 `src` 整个目录加入 `sys.path`（见 `.venv/Lib/site-packages/test.pth`），
> 因此 `src/agent` 可以直接以 `agent` 为顶级包导入，与课程代码的 `from agent.xxx import ...` 完全一致。

## 目录结构

```
test/
├── .env
├── pyproject.toml
└── src/
    ├── agent/                        # 16–23 章整合后的 Agent
    │   ├── config.py                 # pydantic-settings 读取 .env（OpenAI / Tavily）
    │   ├── events.py                 # Event 常量 + EventEmitter
    │   ├── listener.py               # ModelListener 抽象基类
    │   ├── model.py                  # Model：invoke / invoke_stream + 流式聚合 Builder
    │   ├── printer.py                # ModelPrinterListener：彩色流式打印
    │   ├── prompt.py                 # Jinja2 渲染系统提示词 / 扫描 Skill
    │   ├── session.py                # 会话：messages + tools，保存/加载
    │   ├── agent.py                  # Agent：ReAct 主循环
    │   ├── prompt/system.j2          # 系统提示词模板
    │   ├── .agents/skills/           # Skill 定义（SKILL.md）
    │   ├── skills-lock.json
    │   └── tool/
    │       ├── __init__.py           # registry：注册 / schemas / invoke
    │       ├── read_file.py
    │       ├── write_file.py
    │       ├── bash_command.py
    │       ├── web.py                # Tavily 的 web_search / fetch_url
    │       ├── use_skill.py
    │       └── core/                 # Tool 类、@tool 装饰器、参数模型生成
    └── test/
        ├── main.py                   # 第 15 章：直接调用模型接口（流式）
        ├── utils/                    # config / img_base64 / stream_resp / stream_print
        └── demos/
            ├── ch16_system_prompt.py
            ├── ch17_session.py
            ├── ch18_tools.py
            ├── ch20_react.py
            ├── ch21_agent.py
            ├── ch22_web_search.py
            └── ch23_skill.py
```

## 章节与代码对应关系

| 章节               | 知识点                                     | 落点                                                            |
| ------------------ | ------------------------------------------ | --------------------------------------------------------------- |
| 15. 模型接口契约   | Chat Completions 请求/响应、流式 chunk     | `src/test/main.py`、`src/test/utils/`                           |
| 16. 系统提示词     | Jinja2 模板 + 环境变量注入                 | `agent/prompt.py`、`agent/prompt/system.j2`                     |
| 17. 会话           | messages 列表、system 消息、持久化         | `agent/session.py`                                              |
| 18. tools          | function calling 的 schema 与 tool 消息    | `agent/tool/__init__.py`、`agent/tool/core/`                    |
| 19. 封装 tools     | `Tool` 类 + `@tool` 装饰器 + pydantic 校验 | `agent/tool/core/tool.py`、`core/utils.py`                      |
| 20. ReAct          | 工具调用循环                               | `demos/ch20_react.py`（手写）                                   |
| 21. Agent          | 循环封装 + 事件监听打印                    | `agent/agent.py`、`agent/model.py`、`agent/printer.py`          |
| 22. Agent 搜索引擎 | Tavily 搜索/抓取工具                       | `agent/tool/web.py`                                             |
| 23. Skill          | 按需加载的提示词模块                       | `agent/prompt.py`、`agent/tool/use_skill.py`、`.agents/skills/` |

## 运行

```powershell
cd F:\data\duyi\agent-core\test

# 第 15 章示例
uv run python -m test.main

# 各章演示
uv run python src/test/demos/ch16_system_prompt.py
uv run python src/test/demos/ch17_session.py
uv run python src/test/demos/ch18_tools.py
uv run python src/test/demos/ch20_react.py
uv run python src/test/demos/ch21_agent.py
uv run python src/test/demos/ch22_web_search.py
uv run python src/test/demos/ch23_skill.py
```

## 环境变量（`.env`）

```dotenv
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=http://192.168.0.98:18089/v1   # 只写到 /v1，SDK 自己拼接路径
OPENAI_MODEL=deepseek-v4-flash
TAVILY_API_KEY=tvly-xxx                        # 第 22 章联网搜索需要
```

`agent/config.py` 和 `test/utils/config.py` 都会从当前文件向上查找 `.env`，因此移动目录后无需改路径。

## 相对课程原版做的调整

1. `.env` 定位改为向上查找（原代码写死 `../.env`，整合后层级变化会失效）。
2. `Model` 的 OpenAI 客户端改为用 `openai_settings` 显式构造：pydantic-settings 只读取配置，
   不会写入 `os.environ`，原来的 `OpenAI()` 在干净环境下会因缺少 api_key 而报错。
   （注意 `OPENAI_BASE_URL` 必须只写到 `/v1`，多写 `/chat/completions` 会让 `/models` 等接口 404/405。）
3. `Session.__init__` 里自定义的 `system_prompt` 原来被忽略，现已真正使用。
4. `registry.invoke` 用 `self._tools.get(name)`，工具名不存在时返回提示文本而不是 `KeyError`。
5. `tools` 为空时传 `None` 给接口，避免部分网关拒绝空数组。
6. `bash_command` 在 Windows 下用 `%COMSPEC%`（`cmd.exe`）作为 `executable`：原代码传 `"cmd"`
   时 `CreateProcess` 不会自动补 `.exe`，会报 `FileNotFoundError`。

第 17 章的 `Session.save()` 会把会话写到 `src/agent/sessions/`，属于运行时产物，可随时删除。
