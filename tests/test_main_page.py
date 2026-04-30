import allure

from pages.cart_page import CartPage
from pages.main_page import MainPage
from utils.helpers import normalize_text


@allure.feature("Главная страница")
class TestMainPage:
    @allure.story("Добавление пиццы в корзину из слайдера")
    @allure.title(
        "Пицца из слайдера добавляется в корзину с правильным названием и ценой"
    )
    def test_add_pizza_from_slider_to_cart(
        self, main_page: MainPage, cart_page: CartPage
    ):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Получить данные первой пиццы из слайдера"):
            pizza = main_page.pizza_slider.get_slide(1)
            pizza_name = pizza.name
            pizza_price = pizza.price

        pizza.add_to_cart()

        with allure.step("Перейти в корзину"):
            main_page.header.go_to_cart()

        with allure.step("Найти пиццу в корзине и проверить данные"):
            item = cart_page.find_item(pizza_name)

            assert item is not None, f"Пицца '{pizza_name}' не найдена в корзине"
            assert normalize_text(item.name) == normalize_text(pizza_name), (
                f"Название: ожидалось '{pizza_name}', получено '{item.name}'"
            )
            assert normalize_text(item.price) == normalize_text(pizza_price), (
                f"Цена: ожидалась '{pizza_price}', получена '{item.price}'"
            )
