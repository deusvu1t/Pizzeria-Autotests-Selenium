import pytest

from pages.account_page import AccountPage
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.register_page import RegisterPage


@pytest.fixture
def main_page(driver) -> MainPage:
    return MainPage(driver=driver)


@pytest.fixture
def cart_page(driver) -> CartPage:
    return CartPage(driver=driver)


@pytest.fixture
def product_page(driver) -> ProductPage:
    return ProductPage(driver=driver)


@pytest.fixture
def catalog_page(driver) -> CatalogPage:
    return CatalogPage(driver=driver)


@pytest.fixture
def checkout_page(driver) -> CheckoutPage:
    return CheckoutPage(driver=driver)


@pytest.fixture
def account_page(driver) -> AccountPage:
    return AccountPage(driver=driver)


@pytest.fixture
def register_page(driver) -> RegisterPage:
    return RegisterPage(driver=driver)


@pytest.fixture
def opened_main_page(main_page: MainPage) -> MainPage:
    main_page.open()
    return main_page


@pytest.fixture
def opened_cart_page(cart_page: CartPage) -> CartPage:
    cart_page.open()
    return cart_page


@pytest.fixture
def opened_account_page(account_page: AccountPage) -> AccountPage:
    account_page.open()
    return account_page


@pytest.fixture
def opened_catalog_page(catalog_page: CatalogPage) -> CatalogPage:
    catalog_page.open()
    return catalog_page


@pytest.fixture
def opened_checkout_page(checkout_page: CheckoutPage) -> CheckoutPage:
    checkout_page.open()
    return checkout_page


@pytest.fixture
def authorized_account_page(
    opened_account_page: AccountPage, test_user: dict
) -> AccountPage:
    opened_account_page.login(
        username=test_user["username"],
        password=test_user["password"],
    )
    return opened_account_page
