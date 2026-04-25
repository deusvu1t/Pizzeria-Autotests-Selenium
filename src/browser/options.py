from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.config.settings import Settings


def get_chrome_options(settings: Settings) -> ChromeOptions:
    options = ChromeOptions()

    if settings.headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    return options


def get_firefox_options(settings: Settings) -> FirefoxOptions:
    options = FirefoxOptions()
    if settings.headless:
        options.add_argument("--headless")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    return options
