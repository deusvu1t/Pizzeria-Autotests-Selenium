from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from core.config.settings import Settings, settings
from core.driver.factory import create_driver
from core.utils.logger import get_logger, setup_logging

logger = get_logger(__name__)


def pytest_configure(config):
    setup_logging()


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
def driver(
    app_settings: Settings, request: pytest.FixtureRequest
) -> Generator[WebDriver, None, None]:
    """Каждый тест получает свежий драйвер."""
    test_name = request.node.nodeid
    logger.info("Test started | %s", test_name)

    driver = create_driver(app_settings)
    driver.implicitly_wait(app_settings.timeout)
    driver.set_page_load_timeout(app_settings.page_load_timeout)

    yield driver
    logger.info(
        "Closing browser | session_id=%s | test=%s", driver.session_id, test_name
    )
    driver.quit()
    logger.info("Browser closed | %s", test_name)
