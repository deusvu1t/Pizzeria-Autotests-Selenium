from pages.cart_page import CartPage
from pages.main_page import MainPage


class TestExample:
    def test_example(self, main_page: MainPage, cart_page: CartPage):
        main_page.open()
        cart_page.open()
