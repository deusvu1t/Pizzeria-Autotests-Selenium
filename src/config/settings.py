from dataclasses import dataclass


@dataclass
class Settings:
    browser: str = "chrome"
    run_mode: str = "local"
    headless: bool = False

    base_url: str = "https://pizzeria.skillbox.cc/"
    selenoid_url: str = "http://localhost:4444/wd/hub"

    timeout: int = 10
    page_load_timeout: int = 30
