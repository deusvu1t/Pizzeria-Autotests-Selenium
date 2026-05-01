import allure
import pytest
from allure_commons.types import AttachmentType

pytest_plugins = [
    "fixtures.driver",
    "fixtures.pages",
]


@pytest.fixture
def test_user():
    return {"username": "test_username001", "password": "test123"}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=AttachmentType.PNG,
            )
