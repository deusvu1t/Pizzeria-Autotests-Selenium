import pytest

from src.pages.cart_page import CartPage
from src.pages.main_page import MainPage
from src.pages.product_page import ProductPage
from src.pages.account_page import AccountPage
from src.pages.catalog_page import CatalogPage
from src.pages.checkout_page import CheckoutPage

@pytest.fixture
def main_page(driver):
    return MainPage(driver)

@pytest.fixture
def cart_page(driver):
    return CartPage(driver)

@pytest.fixture
def product_page(driver):
    return ProductPage(driver)

@pytest.fixture
def account_page(driver):
    return AccountPage(driver)

@pytest.fixture
def catalog_page(driver):
    return CatalogPage(driver)

@pytest.fixture
def checkout_page(driver):
    return CheckoutPage(driver)
