import allure

from src.pages.cart_page import CartPage
from src.pages.main_page import MainPage
from src.pages.product_page import ProductPage


@allure.feature("Страница корзины")
class TestCartPage:
    def test_cart_content_after_adding_items(
        self, main_page: MainPage, product_page: ProductPage, cart_page: CartPage
    ):
        with allure.step("1. Добавить в корзину несколько пицц из слайдера."):
            main_page.open()
            slider = main_page.pizza_slider()
            total = 0
            p1 = slider.slides()[0]
            p1_name = p1.title
            total += p1.price
            p1.add_to_cart()
            p2 = slider.slides()[1]
            p2_name = p2.title
            total += p2.price
            p2.add_to_cart()
        with allure.step(
            "2. Добавить в корзину пиццу с дополнительной опцией со страницы подробностей."
        ):
            product_page.open("пицца-4-в-1")
            product_page.board_pack("Сырный")
            p3_name = 'пицца "4 в 1"'
            total += product_page.price
            product_page.add_to_cart()
        with allure.step("3. Открыть корзину."):
            cart_page.open()
        with allure.step(
            "Ожидаемый результат: все добавленные пиццы отображаются в корзине."
        ):
            cart_page.wait.until(lambda _: len(cart_page.items()) >= 3)
            items = cart_page.items()
            assert len(items) >= 3
            item_names = [item.name for item in items]
            assert p1_name in item_names
            assert p2_name in item_names
            assert p3_name in item_names
            for item in items:
                assert item.quantity >= 1
                if item.name == p3_name:
                    if item.variation:
                        assert "сыр" in item.variation.lower()
            assert total == cart_page.order_total

    def test_increase_item_quantity_in_cart(self):
        pass

    def test_remove_item_with_extra_option_from_cart(self):
        pass
