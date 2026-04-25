from typing import Generator

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.browser.factory import create_driver
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    settings = Settings(
        browser=request.config.getoption("--browser"),
        headless=request.config.getoption("--headless"),
    )

    test_name = request.node.nodeid

    logger.info(
        "START TEST | %s | browser=%s | headless=%s",
        test_name,
        settings.browser,
        settings.headless,
    )

    allure.dynamic.parameter("browser", settings.browser)
    allure.dynamic.parameter("headless", settings.headless)

    with allure.step(
        f"Запустить браузер {settings.browser} | headless={settings.headless}"
    ):
        driver = create_driver(settings)

    try:
        yield driver
    finally:
        logger.info(
            "END TEST | %s | session_id=%s",
            test_name,
            driver.session_id,
        )

        with allure.step("Закрыть браузер"):
            driver.quit()
