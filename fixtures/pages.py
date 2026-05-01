import pytest

from pages.account_page import AccountPage
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.main_page import MainPage
from pages.product_page import ProductPage
from tests.register_page import RegisterPage


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver=driver)


@pytest.fixture
def product_page(driver):
    return ProductPage(driver=driver)


@pytest.fixture
def catalog_page(driver):
    return CatalogPage(driver=driver)


@pytest.fixture
def checkout_page(driver):
    return CheckoutPage(driver=driver)


@pytest.fixture
def account_page(driver):
    return AccountPage(driver=driver)


@pytest.fixture
def register_page(driver):
    return RegisterPage(driver=driver)
