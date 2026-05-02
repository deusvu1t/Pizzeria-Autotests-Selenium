import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.logger import get_logger

logger = get_logger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Browser to run tests on: chrome (default) or firefox",
    )


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser").lower()


def _make_chrome_options(is_ci: bool) -> ChromeOptions:
    options = ChromeOptions()
    if is_ci:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return options


def _make_firefox_options(is_ci: bool) -> FirefoxOptions:
    options = FirefoxOptions()
    if is_ci:
        options.add_argument("--headless")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    return options


@pytest.fixture
def driver(browser_name):
    is_ci = os.getenv("CI", "false").lower() == "true"
    logger.info(f"Starting browser: {browser_name} | headless: {is_ci}")

    if browser_name == "chrome":
        drv = webdriver.Chrome(options=_make_chrome_options(is_ci))
    elif browser_name == "firefox":
        drv = webdriver.Firefox(options=_make_firefox_options(is_ci))
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    logger.info("Browser started successfully")
    yield drv
    logger.info("Closing browser")
    drv.quit()
