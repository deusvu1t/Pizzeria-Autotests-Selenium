import allure

from src.pages.cart_page import CartPage
from src.pages.product_page import ProductPage


@allure.feature("Страница продукта")
class TestProductPage:
    @allure.story("Выбор опций")
    @allure.title("Изменение типа борта пиццы")
    def test_can_select_product_extra_option(self, product_page: ProductPage):
        product_page.open("пицца-4-в-1")

        product_page.board_pack("Сырный")
        assert product_page.active_board_pack_value == "55.00"

        product_page.board_pack("Колбасный")
        assert product_page.active_board_pack_value == "65.00"

        product_page.board_pack("Обычный")
        assert product_page.active_board_pack_value == ""

    def test_can_add_pizza_with_extra_option_to_cart(
        self, product_page: ProductPage, cart_page: CartPage
    ):
        pizza_variation = "Сырный"
        product_page.open("пицца-4-в-1")
        product_page.board_pack(pizza_variation)
        pizza_price = product_page.price
        product_page.add_to_cart()
        product_page.header.go_to_cart()
        item = cart_page.items()[0]
        assert pizza_price == item.price
        assert pizza_variation in item.variation
