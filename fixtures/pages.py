import pytest

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.main_page import MainPage
from pages.product_page import ProductPage


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver=driver)


@pytest.fixture()
def product_page(driver):
    return ProductPage(driver=driver)


@pytest.fixture()
def catalog_page(driver):
    return CatalogPage(driver=driver)
