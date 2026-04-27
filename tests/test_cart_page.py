from src.pages.cart_page import CartPage
from src.pages.main_page import MainPage


class TestCartPage:
    def test_cart_content_after_adding_items(
        self, main_page: MainPage, cart_page: CartPage
    ):
        main_page.open()
        main_page.pizza_slider().slides()[0].add_to_cart
        main_page.pizza_slider().slides()[1].add_to_cart
        pass

    def test_increase_item_quantity_in_cart(self):
        pass

    def test_remove_item_with_extra_option_from_cart(self):
        pass
