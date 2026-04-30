import allure

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.main_page import MainPage
from pages.product_page import ProductPage
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

    @allure.story("Изменение количества товара в корзине")
    @allure.title("Количество пиццы в корзине изменяется после обновления")
    def test_change_product_quantity_in_cart(
        self, main_page: MainPage, cart_page: CartPage
    ):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Получить данные первой пиццы из слайдера"):
            pizza = main_page.pizza_slider.get_slide(1)
            pizza_name = pizza.name

        with allure.step(f"Добавить пиццу '{pizza_name}' в корзину"):
            pizza.add_to_cart()

        with allure.step("Перейти в корзину"):
            main_page.header.go_to_cart()

        with allure.step(f"Найти пиццу '{pizza_name}' в корзине"):
            item = cart_page.find_item(pizza_name)
            assert item is not None, f"Пицца '{pizza_name}' не найдена в корзине"

        with allure.step("Изменить количество товара на 2"):
            item.set_quantity(2)
            cart_page.update_cart()

        with allure.step("Проверить, что количество товара изменилось"):
            updated_item = cart_page.find_item(pizza_name)
            assert updated_item is not None, (
                f"Пицца '{pizza_name}' не найдена после обновления корзины"
            )
            assert updated_item.quantity == "2", (
                f"Количество: ожидалось '2', получено '{updated_item.quantity}'"
            )

    @allure.story("Удаление товара из корзины")
    @allure.title("Пицца удаляется из корзины")
    def test_remove_product_from_cart(self, main_page: MainPage, cart_page: CartPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Получить данные первой пиццы из слайдера"):
            pizza = main_page.pizza_slider.get_slide(1)
            pizza_name = pizza.name

        with allure.step(f"Добавить пиццу '{pizza_name}' в корзину"):
            pizza.add_to_cart()

        with allure.step("Перейти в корзину"):
            main_page.header.go_to_cart()

        with allure.step(f"Найти пиццу '{pizza_name}' в корзине"):
            item = cart_page.find_item(pizza_name)
            assert item is not None, f"Пицца '{pizza_name}' не найдена в корзине"

        with allure.step(f"Удалить пиццу '{pizza_name}' из корзины"):
            item.remove()
            cart_page.wait_until_item_removed(pizza_name)

        with allure.step("Проверить, что пицца удалена из корзины"):
            assert cart_page.is_cart_empty()

    @allure.story("Переход на страницу продукта")
    @allure.title("При клике на пиццу открывается страница выбранного продукта")
    def test_go_to_product_page(self, main_page: MainPage, product_page: ProductPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Получить данные пиццы из первого слайда"):
            pizza = main_page.pizza_slider.get_slide(1)
            pizza_name = pizza.name
            pizza_price = pizza.price

        with allure.step(f"Перейти на страницу пиццы '{pizza_name}'"):
            pizza.go_to_product_page()

        with allure.step("Проверить название и цену на странице продукта"):
            expected_name = normalize_text(pizza_name)
            actual_name = normalize_text(product_page.name)
            assert actual_name == expected_name, (
                f"Название: ожидалось '{pizza_name}', получено '{product_page.name}'"
            )
            assert product_page.price == pizza_price, (
                f"Цена: ожидалась '{pizza_price}', получена '{product_page.price}'"
            )

    @allure.story("Выбор опции на странице продукта")
    @allure.title("Выбор бортика меняет выбранную опцию на странице продукта")
    def test_select_product_option_changes_state(
        self, main_page: MainPage, product_page: ProductPage
    ):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Перейти на страницу первой пиццы из слайдера"):
            main_page.pizza_slider.get_slide(1).go_to_product_page()

        with allure.step("Получить текущую и доступные опции бортика"):
            initial_board = product_page.selected_board
            available_boards = [
                board for board in product_page.board_options if board != initial_board
            ]
            assert available_boards, "Нет доступных опций бортика для выбора"

        selected_board = available_boards[0]
        with allure.step(f"Выбрать опцию бортика '{selected_board}'"):
            product_page.select_board(selected_board)

        with allure.step("Проверить, что выбранная опция изменилась"):
            assert product_page.selected_board == selected_board, (
                f"Ожидалась выбранная опция '{selected_board}', "
                f"получена '{product_page.selected_board}'"
            )

    @allure.story("Добавление пиццы с опцией")
    @allure.title("Пицца с выбранным бортиком добавляется в корзину")
    def test_add_pizza_with_option_to_cart(
        self,
        main_page: MainPage,
        product_page: ProductPage,
        cart_page: CartPage,
    ):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Получить пиццу из первого слайда"):
            pizza = main_page.pizza_slider.get_slide(1)
            slider_pizza_name = pizza.name

        with allure.step(f"Перейти на страницу пиццы '{slider_pizza_name}'"):
            pizza.go_to_product_page()

        with allure.step("Получить название пиццы со страницы продукта"):
            pizza_name = product_page.name

        with allure.step("Выбрать доступную опцию бортика"):
            initial_board = product_page.selected_board
            available_boards = [
                board for board in product_page.board_options if board != initial_board
            ]
            assert available_boards, "Нет доступных опций бортика для выбора"

            selected_board = available_boards[0]
            product_page.select_board(selected_board)

        with allure.step(
            f"Добавить пиццу '{pizza_name}' с бортиком '{selected_board}'"
        ):
            product_page.add_to_cart()

        with allure.step("Перейти в корзину из сообщения о добавлении"):
            product_page.go_to_cart_from_message()

        with allure.step("Проверить пиццу с выбранной опцией в корзине"):
            item = cart_page.find_item(pizza_name)

            assert item is not None, f"Пицца '{pizza_name}' не найдена в корзине"

            expected_name = normalize_text(pizza_name)
            actual_name = normalize_text(item.name)
            assert actual_name == expected_name, (
                f"Название: ожидалось '{pizza_name}', получено '{item.name}'"
            )

            actual_variation = item.variation or ""
            expected_board_name = selected_board.split(" - ")[0]
            assert normalize_text(expected_board_name) in normalize_text(
                actual_variation
            ), f"Опция: ожидалась '{expected_board_name}', получено '{item.variation}'"
