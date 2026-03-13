import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _get_env_int(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError:
        return default


@dataclass(frozen=True)
class EnvironmentConfig:
    PORT: int = _get_env_int("PORT", 8000)
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()


environment = EnvironmentConfig()