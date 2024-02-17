from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Points Pydantic to the env file."""

    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Override Config class
class GlobalConfig(BaseConfig):
    """Define variables collected from env file. It will strip the prefix."""

    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    """Config used for development."""

    model_config = SettingsConfigDict(env_prefix="DEV_", extra="ignore")


class ProdConfig(GlobalConfig):
    """Config used for production."""

    model_config = SettingsConfigDict(env_prefix="PROD_", extra="ignore")


class TestConfig(GlobalConfig):
    """Config used for testing. Setup should always be the same for everyone."""

    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_", extra="ignore")


@lru_cache()
def get_config(env_state: str):
    """Cache the (param => return) results when function is invoked again"""

    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
