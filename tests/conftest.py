from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from core.config.settings import Settings, settings
from core.driver.factory import create_driver


def pytest_addoption(parser):
    """Позволяет переопределять настройки через CLI."""
    parser.addoption("--browser", default=None)
    parser.addoption("--run-mode", default=None)
    parser.addoption("--headless", action="store_true", default=None)


@pytest.fixture(scope="session")
def app_settings(request) -> Settings:
    """Настройки с возможностью переопределить через CLI."""
    overrides = {}
    if browser := request.config.getoption("--browser"):
        overrides["browser"] = browser
    if run_mode := request.config.getoption("--run-mode"):
        overrides["run_mode"] = run_mode
    if request.config.getoption("--headless"):
        overrides["headless"] = True

    return settings.model_copy(update=overrides)


@pytest.fixture(scope="function")
def driver(app_settings: Settings) -> Generator[WebDriver, None, None]:
    """Каждый тест получает свежий драйвер."""
    driver = create_driver(app_settings)
    driver.implicitly_wait(app_settings.timeout)
    driver.set_page_load_timeout(app_settings.page_load_timeout)
    yield driver
    driver.quit()
