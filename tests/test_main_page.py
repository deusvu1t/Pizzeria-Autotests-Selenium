import allure

from pages.cart_page import CartPage
from pages.main_page import MainPage
from utils.helpers import normalize_text


@allure.feature("Главная страница")
class TestMainPage:
    @allure.story("Отображение слайдера пицц")
    @allure.title("Слайдер пицц отображается на главной странице")
    def test_pizza_slider_is_visible(self, opened_main_page: MainPage):
        with allure.step("Проверить, что слайдер пицц отображается"):
            assert opened_main_page.pizza_slider.is_visible(), (
                "Слайдер пицц не отображается"
            )

    @allure.story("Отображение слайдов пицц")
    @allure.title("Первые четыре слайда пицц отображаются в слайдере")
    def test_pizza_slides_is_visible(self, opened_main_page: MainPage):
        for index in range(1, 5):
            with allure.step(f"Проверить отображение слайда #{index}"):
                assert opened_main_page.pizza_slider.get_slide(index).is_visible(), (
                    f"Слайд #{index} не отображается"
                )

    @allure.story("Отображение кнопки добавления в корзину")
    @allure.title("Кнопка «В корзину» появляется при наведении на слайд")
    def test_button_add_to_cart_is_visible(self, opened_main_page: MainPage):
        for index in range(1, 5):
            with allure.step(f"Навести курсор на слайд #{index}"):
                slide = opened_main_page.pizza_slider.get_slide(index)
                slide.hover_self()

            with allure.step(f"Проверить кнопку добавления на слайде #{index}"):
                assert slide.is_visible(slide.ADD_BUTTON), (
                    f"Кнопка добавления в корзину не отображается на слайде #{index}"
                )

    @allure.story("Переключение слайдера пицц")
    @allure.title("Набор пицц в слайдере меняется при переключении вперёд и назад")
    def test_pizza_slider_switches_both_directions(self, opened_main_page: MainPage):
        def get_visible_names() -> list[str]:
            return [
                opened_main_page.pizza_slider.get_slide(i).name for i in range(1, 5)
            ]

        with allure.step("Запомнить исходный набор видимых пицц"):
            initial_pizzas = get_visible_names()

        with allure.step("Переключить слайдер вперёд"):
            opened_main_page.pizza_slider.next()

        with allure.step("Проверить, что набор пицц изменился"):
            next_pizzas = get_visible_names()
            assert next_pizzas != initial_pizzas, (
                "Набор пицц не изменился после переключения вперёд"
            )

        with allure.step("Переключить слайдер назад"):
            opened_main_page.pizza_slider.prev()

        with allure.step("Проверить, что слайдер вернулся к исходному набору"):
            assert get_visible_names() == initial_pizzas, (
                "Слайдер не вернулся к исходному набору пицц"
            )

    @allure.story("Добавление пиццы в корзину после прокрутки слайдера")
    @allure.title("Пицца из слайдера добавляется в корзину после переключения вперёд")
    def test_add_pizza_after_slider_scroll(
        self, opened_main_page: MainPage, cart_page: CartPage
    ):
        with allure.step("Запомнить исходный набор пицц"):
            initial_pizzas = [
                opened_main_page.pizza_slider.get_slide(i).name for i in range(1, 5)
            ]

        with allure.step("Переключить слайдер вперёд"):
            opened_main_page.pizza_slider.next()

        with allure.step("Выбрать пиццу из нового набора"):
            pizza = opened_main_page.pizza_slider.get_slide(4)
            pizza_name = pizza.name
            pizza_price = pizza.price
            assert pizza_name not in initial_pizzas, (
                f"Пицца '{pizza_name}' уже была в исходном наборе слайдов"
            )

        with allure.step(f"Добавить пиццу '{pizza_name}' в корзину"):
            opened_main_page.pizza_slider.get_slide(4).add_to_cart()

        with allure.step("Перейти в корзину"):
            opened_main_page.header.go_to_cart()

        with allure.step(f"Проверить '{pizza_name}' в корзине"):
            item = cart_page.find_item(pizza_name)
            assert item is not None, f"Пицца '{pizza_name}' не найдена в корзине"
            assert normalize_text(item.name) == normalize_text(pizza_name), (
                f"Название: ожидалось '{pizza_name}', получено '{item.name}'"
            )
            assert normalize_text(item.price) == normalize_text(pizza_price), (
                f"Цена: ожидалась '{pizza_price}', получена '{item.price}'"
            )

    @allure.story("Добавление нескольких пицц в корзину из слайдера")
    @allure.title("Две пиццы из слайдера добавляются в корзину с правильными данными")
    def test_add_pizzas_from_slider_to_cart(
        self, opened_main_page: MainPage, cart_page: CartPage
    ):
        pizzas = []
        for index in range(1, 3):
            with allure.step(f"Запомнить данные пиццы со слайда #{index}"):
                pizza = opened_main_page.pizza_slider.get_slide(index)
                pizzas.append(
                    {"index": index, "name": pizza.name, "price": pizza.price}
                )

        for pizza in pizzas:
            with allure.step(f"Добавить пиццу '{pizza['name']}' в корзину"):
                opened_main_page.pizza_slider.get_slide(pizza["index"]).add_to_cart()

        with allure.step("Перейти в корзину"):
            opened_main_page.header.go_to_cart()

        for pizza in pizzas:
            with allure.step(f"Проверить '{pizza['name']}' в корзине"):
                item = cart_page.find_item(pizza["name"])
                assert item is not None, f"Пицца '{pizza['name']}' не найдена в корзине"
                assert normalize_text(item.name) == normalize_text(pizza["name"]), (
                    f"Название: ожидалось '{pizza['name']}', получено '{item.name}'"
                )
                assert normalize_text(item.price) == normalize_text(pizza["price"]), (
                    f"Цена: ожидалась '{pizza['price']}', получена '{item.price}'"
                )
