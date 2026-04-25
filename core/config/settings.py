from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Browser(StrEnum):
    CHROME = "chrome"
    FIREFOX = "firefox"


class RunMode(StrEnum):
    LOCAL = "local"
    SELENOID = "selenoid"


class Settings(BaseSettings):
    # Браузер и режим запуска
    browser: Browser = Browser.CHROME
    run_mode: RunMode = RunMode.LOCAL
    headless: bool = False

    # URLs
    base_url: str = "https://pizzeria.skillbox.cc/"
    selenoid_url: str = "http://localhost:4444/wd/hub"

    # Таймауты
    timeout: int = 10
    page_load_timeout: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Singleton — импортируй этот объект везде
settings = Settings()
