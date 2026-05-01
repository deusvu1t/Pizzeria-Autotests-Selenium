import allure

from pages.cart_page import CartPage
from pages.main_page import MainPage
from utils.helpers import normalize_text


@allure.feature("Главная страница")
class TestMainPage:
    @allure.story("Отображение слайдера пицц")
    @allure.title("Слайдер пицц отображается на главной странице")
    def test_pizza_slider_is_visible(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Проверить, что слайдер пицц отображается"):
            assert main_page.pizza_slider.is_visible(), "Слайдер пицц не отображается"

    @allure.story("Отображение слайдов пицц")
    @allure.title("Первые четыре слайда пицц отображаются в слайдере")
    def test_pizza_slides_is_visible(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        for index in range(1, 5):
            with allure.step(f"Проверить отображение слайда #{index}"):
                assert main_page.pizza_slider.get_slide(index).is_visible(), (
                    f"Слайд #{index} не отображается"
                )

    @allure.story("Отображение кнопки добавления в корзину")
    @allure.title("Кнопка добавления в корзину отображается при наведении")
    def test_button_add_to_cart_is_visible(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        for index in range(1, 5):
            with allure.step(f"Навести курсор на слайд #{index}"):
                slide = main_page.pizza_slider.get_slide(index)
                slide.hover_self()

            with allure.step(
                f"Проверить отображение кнопки добавления на слайде #{index}"
            ):
                assert slide.is_visible(slide.ADD_BUTTON), (
                    f"Кнопка добавления в корзину не отображается на слайде #{index}"
                )

    @allure.story("Переключение слайдера пицц")
    @allure.title("Набор пицц в слайдере меняется при переключении")
    def test_pizza_slider_switches_both_directions(self, main_page: MainPage):
        def get_visible_pizza_names():
            return [
                main_page.pizza_slider.get_slide(index).name for index in range(1, 5)
            ]

        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Получить исходный набор видимых пицц"):
            initial_pizzas = get_visible_pizza_names()

        with allure.step("Переключить слайдер вперёд"):
            main_page.pizza_slider.next()

        with allure.step("Проверить, что набор пицц изменился"):
            next_pizzas = get_visible_pizza_names()
            assert next_pizzas != initial_pizzas, (
                "Набор пицц не изменился после переключения вперёд"
            )

        with allure.step("Переключить слайдер назад"):
            main_page.pizza_slider.prev()

        with allure.step("Проверить, что слайдер вернулся к исходному набору"):
            previous_pizzas = get_visible_pizza_names()
            assert previous_pizzas == initial_pizzas, (
                "Слайдер не вернулся к исходному набору пицц"
            )

    @allure.story("Добавление пиццы в корзину после прокрутки слайдера")
    @allure.title("Пицца из слайдера добавляется в корзину после переключения вперёд")
    def test_add_pizza_after_slider_scroll(
        self, main_page: MainPage, cart_page: CartPage
    ):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Получить исходный набор видимых пицц"):
            initial_pizzas = [
                main_page.pizza_slider.get_slide(index).name for index in range(1, 5)
            ]

        with allure.step("Переключить слайдер вперёд"):
            main_page.pizza_slider.next()

        with allure.step("Выбрать пиццу из нового набора слайдов"):
            pizza = main_page.pizza_slider.get_slide(4)
            pizza_name = pizza.name
            pizza_price = pizza.price

            assert pizza_name not in initial_pizzas, (
                f"Пицца '{pizza_name}' уже была в исходном наборе слайдов"
            )

        with allure.step(f"Добавить пиццу '{pizza_name}' в корзину"):
            main_page.pizza_slider.get_slide(4).add_to_cart()

        with allure.step("Перейти в корзину"):
            main_page.header.go_to_cart()

        with allure.step(f"Найти пиццу '{pizza_name}' и проверить данные"):
            item = cart_page.find_item(pizza_name)

            assert item is not None, f"Пицца '{pizza_name}' не найдена в корзине"

            expected_name = normalize_text(pizza_name)
            actual_name = normalize_text(item.name)
            assert actual_name == expected_name, (
                f"Название: ожидалось '{pizza_name}', получено '{item.name}'"
            )

            expected_price = normalize_text(pizza_price)
            actual_price = normalize_text(item.price)
            assert actual_price == expected_price, (
                f"Цена: ожидалась '{pizza_price}', получена '{item.price}'"
            )

    @allure.story("Добавление пицц в корзину из слайдера")
    @allure.title(
        "Две пиццы из слайдера добавляются в корзину с правильными названиями и ценами"
    )
    def test_add_pizzas_from_slider_to_cart(
        self, main_page: MainPage, cart_page: CartPage
    ):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        pizzas = []
        for index in range(1, 3):
            with allure.step(f"Получить данные пиццы со слайда #{index}"):
                pizza = main_page.pizza_slider.get_slide(index)
                pizzas.append(
                    {
                        "index": index,
                        "name": pizza.name,
                        "price": pizza.price,
                    }
                )

        for pizza in pizzas:
            with allure.step(
                f"Добавить пиццу '{pizza['name']}' из слайда "
                f"#{pizza['index']} в корзину"
            ):
                main_page.pizza_slider.get_slide(pizza["index"]).add_to_cart()

        with allure.step("Перейти в корзину"):
            main_page.header.go_to_cart()

        for pizza in pizzas:
            with allure.step(
                f"Найти пиццу '{pizza['name']}' в корзине и проверить данные"
            ):
                item = cart_page.find_item(pizza["name"])

                assert item is not None, f"Пицца '{pizza['name']}' не найдена в корзине"
                expected_name = normalize_text(pizza["name"])
                actual_name = normalize_text(item.name)
                assert actual_name == expected_name, (
                    f"Название: ожидалось '{pizza['name']}', получено '{item.name}'"
                )

                expected_price = normalize_text(pizza["price"])
                actual_price = normalize_text(item.price)
                assert actual_price == expected_price, (
                    f"Цена: ожидалась '{pizza['price']}', получена '{item.price}'"
                )
