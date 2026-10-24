from dotenv import load_dotenv
import os
from pathlib import Path


def _find_env_file() -> Path:
    """向上查找项目根目录下的 .env 文件。"""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / ".env"
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("未找到 .env 文件")


_env_file = _find_env_file()

load_dotenv(_env_file)

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")  # type: ignore
OPENAI_BASE_URL: str = os.environ.get("OPENAI_BASE_URL")  # type: ignore
OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL")  # type: ignore

__all__ = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"]
