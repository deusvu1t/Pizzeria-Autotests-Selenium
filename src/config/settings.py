from dataclasses import dataclass


@dataclass
class Settings:
    browser: str = "chrome"
    headless: bool = False

    base_url: str = "https://pizzeria.skillbox.cc/"
