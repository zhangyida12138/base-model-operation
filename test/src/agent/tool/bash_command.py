import os
import subprocess
from sys import platform

from agent.tool.core import tool


@tool(command="要执行的 bash/shell 命令")
def bash_command(command: str) -> str:
    """执行 bash/shell 命令，返回命令输出结果"""

    # Windows 下 executable 不会自动补 .exe，需用 COMSPEC（cmd.exe）
    if platform == "win32":
        shell_flag = os.environ.get("COMSPEC", "cmd.exe")
    else:
        shell_flag = "/bin/bash"

    result = subprocess.run(
        command,
        shell=True,
        executable=shell_flag,
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode == 0:
        return result.stdout.strip() or "(命令执行成功，无输出)"
    else:
        return f"[退出码 {result.returncode}]\n{result.stderr.strip() or result.stdout.strip()}"
