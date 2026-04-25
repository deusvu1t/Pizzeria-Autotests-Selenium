from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.browser.options import (
    get_chrome_options,
    get_firefox_options,
)
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_driver(settings: Settings) -> WebDriver:
    if settings.run_mode == "selenoid":
        return _create_remote(settings)
    return _create_local(settings)


def _create_local(settings: Settings):
    if settings.browser == "chrome":
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=get_chrome_options(settings),
        )
    elif settings.browser == "firefox":
        return webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=get_firefox_options(settings),
        )
    else:
        raise ValueError(f"Unsupported browser: {settings.browser}")


def _create_remote(settings: Settings) -> WebDriver:
    if settings.browser == "chrome":
        options = get_chrome_options(settings)
    elif settings.browser == "firefox":
        options = get_firefox_options(settings)
    else:
        raise ValueError(f"Unsupported browser: {settings.browser}")

    options.set_capability(
        "selenoid:options",
        {
            "enableVNC": True,
            "enableVideo": False,
        },
    )

    return webdriver.Remote(
        command_executor=settings.selenoid_url,
        options=options,
    )
