from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from core.config.settings import Browser, RunMode, Settings
from core.driver.options import (
    get_chrome_options,
    get_firefox_options,
)


def create_driver(settings: Settings) -> WebDriver:
    if settings.run_mode == RunMode.SELENOID:
        return _create_remote(settings)
    return _create_local(settings)


def _create_local(settings: Settings) -> WebDriver:
    match settings.browser:
        case Browser.CHROME:
            return webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=get_chrome_options(settings),
            )
        case Browser.FIREFOX:
            return webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=get_firefox_options(settings),
            )
        case _:
            raise ValueError(f"Unsupported browser: {settings.browser}")


def _create_remote(settings: Settings) -> WebDriver:
    """Selenoid и GitHub CI — оба используют Remote."""
    options_map = {
        Browser.CHROME: get_chrome_options(settings),
        Browser.FIREFOX: get_firefox_options(settings),
    }
    options = options_map.get(settings.browser)
    if not options:
        raise ValueError(f"Unsupported browser: {settings.browser}")

    # Selenoid capabilities
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
