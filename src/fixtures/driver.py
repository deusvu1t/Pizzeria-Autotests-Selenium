from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.browser.factory import create_driver
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    settings = Settings()

    settings.browser = request.config.getoption("--browser")
    settings.run_mode = request.config.getoption("--run-mode")
    settings.headless = request.config.getoption("--headless")

    driver = create_driver(settings)
    driver.implicitly_wait(settings.timeout)
    driver.set_page_load_timeout(settings.page_load_timeout)

    yield driver
    driver.quit()
