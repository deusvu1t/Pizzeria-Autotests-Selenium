from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.browser.factory import create_driver
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    test_name = request.node.nodeid
    logger.info("Test started | %s", test_name)

    settings = Settings()  # просто создаём

    driver = create_driver(settings)
    driver.implicitly_wait(settings.timeout)
    driver.set_page_load_timeout(settings.page_load_timeout)

    yield driver

    logger.info(
        "Closing browser | session_id=%s | test=%s",
        driver.session_id,
        test_name,
    )
    driver.quit()
    logger.info("Browser closed | %s", test_name)
