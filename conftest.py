from pathlib import Path

import allure
import pytest

from src.config.settings import Settings
from src.utils.logger import get_logger, setup_logging
from src.utils.logger import LOG_FILE

logger = get_logger(__name__)


def pytest_configure(config):
    setup_logging()
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    allure_dir = Path(config.option.allure_report_dir or "reports/allure-results")
    allure_dir.mkdir(parents=True, exist_ok=True)

    browser = config.getoption("--browser")
    headless = config.getoption("--headless")
    environment = {
        "base_url": Settings.base_url,
        "browser": browser,
        "headless": str(headless),
    }
    content = "\n".join(f"{key}={value}" for key, value in environment.items())
    (allure_dir / "environment.properties").write_text(
        content,
        encoding="utf-8",
    )


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if not report.failed:
        return

    logger.error("TEST FAILED | %s | phase=%s", item.nodeid, report.when)

    driver = item.funcargs.get("driver")
    if driver is not None:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                driver.page_source,
                name="failure_page_source",
                attachment_type=allure.attachment_type.HTML,
            )
        except Exception:
            logger.exception("Failed to attach browser state to Allure")

    if LOG_FILE.exists():
        allure.attach.file(
            str(LOG_FILE),
            name="test_run_log",
            attachment_type=allure.attachment_type.TEXT,
        )


pytest_plugins: list[str] = [
    "src.fixtures.driver",
    "src.fixtures.pages",
]
