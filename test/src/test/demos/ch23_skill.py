"""第 23 章：Skill。

Skill = 按需加载的提示词模块。
- 平时只把每个 Skill 的 description 渲染进系统提示词（见 prompt/system.j2）
- 用户问题命中场景时，模型调用 use_skill 工具取回完整指令，注入上下文

这里的目录是 agent/.agents/skills/<name>/SKILL.md。
"""

import json

from agent.prompt import list_skills
from agent.tool.use_skill import use_skill

if __name__ == "__main__":
    skills = list_skills()
    print("可用 Skill:")
    for item in skills:
        for name, meta in item.items():
            print(f"  - {name}: {meta.get('description', '')}")

    if skills:
        first_name = next(iter(skills[0]))
        print(f"\n=== 加载 {first_name} ===")
        data = json.loads(use_skill(skill_name=first_name))
        print("meta:", data["meta"])
        print("path:", data["path"])
        print("content 前 200 字:", data["content"][:200])
