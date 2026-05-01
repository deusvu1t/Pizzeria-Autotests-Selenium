import allure

from pages.cart_page import CartPage
from pages.main_page import MainPage
from pages.product_page import ProductPage
from utils.helpers import normalize_text


class TestProductPage:
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
