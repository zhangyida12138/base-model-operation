"""第 16 章：系统提示词。

把 Jinja2 模板 prompt/system.j2 渲染成最终的系统提示词，
模板变量（cwd / os / is_git / skills）在 prompt.py 中注入。
"""

from agent.prompt import get_cwd, get_is_git, get_os, list_skills, render_prompt

if __name__ == "__main__":
    print("cwd     :", get_cwd())
    print("os      :", get_os())
    print("is_git  :", get_is_git())
    print("skills  :", [name for item in list_skills() for name in item])
    print("=" * 60)
    print(render_prompt("system"))
