import pytest

from src.pages.cart_page import CartPage
from src.pages.main_page import MainPage


@pytest.fixture
def main_page(driver):
    return MainPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)
