import pytest

from pages.main_page import MainPage


@pytest.fixture
def main_page(driver):
    return MainPage(driver)
