from pathlib import Path

from pydantic_settings import BaseSettings


def _find_env_file() -> Path:
    """向上查找项目根目录下的 .env 文件。"""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / ".env"
        if candidate.is_file():
            return candidate
    return Path()


_env_file = _find_env_file()


class BaseSettingsWithEnv(BaseSettings):
    model_config = {"env_file": str(_env_file), "extra": "ignore"}


class OpenAISettings(BaseSettingsWithEnv):
    api_key: str = ""
    base_url: str = ""
    model: str = ""

    model_config = {"env_prefix": "OPENAI_"}


class TavilySettings(BaseSettingsWithEnv):
    api_key: str = ""
    model_config = {"env_prefix": "TAVILY_"}


openai_settings = OpenAISettings()
tavily_settings = TavilySettings()
