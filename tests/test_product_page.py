import allure

from pages.cart_page import CartPage
from pages.main_page import MainPage
from pages.product_page import ProductPage
from utils.helpers import normalize_text


@allure.feature("Страница продукта")
class TestProductPage:
    @allure.story("Переход на страницу продукта")
    @allure.title("При клике на пиццу открывается страница выбранного продукта")
    def test_go_to_product_page(
        self, opened_main_page: MainPage, product_page: ProductPage
    ):
        with allure.step("Запомнить данные пиццы из первого слайда"):
            pizza = opened_main_page.pizza_slider.get_slide(1)
            pizza_name = pizza.name
            pizza_price = pizza.price

        with allure.step(f"Перейти на страницу пиццы '{pizza_name}'"):
            pizza.go_to_product_page()

        with allure.step("Проверить название и цену на странице продукта"):
            assert normalize_text(product_page.name) == normalize_text(pizza_name), (
                f"Название: ожидалось '{pizza_name}', получено '{product_page.name}'"
            )
            assert product_page.price == pizza_price, (
                f"Цена: ожидалась '{pizza_price}', получена '{product_page.price}'"
            )

    @allure.story("Выбор опции бортика")
    @allure.title("Выбор бортика изменяет выбранную опцию на странице продукта")
    def test_select_product_option_changes_state(
        self, opened_main_page: MainPage, product_page: ProductPage
    ):
        with allure.step("Перейти на страницу первой пиццы из слайдера"):
            opened_main_page.pizza_slider.get_slide(1).go_to_product_page()

        with allure.step("Получить текущую и доступные опции бортика"):
            initial_board = product_page.selected_board
            available_boards = [
                b for b in product_page.board_options if b != initial_board
            ]
            assert available_boards, "Нет доступных опций бортика для выбора"

        with allure.step(f"Выбрать бортик '{available_boards[0]}'"):
            product_page.select_board(available_boards[0])

        with allure.step("Проверить, что выбранная опция изменилась"):
            assert product_page.selected_board == available_boards[0], (
                f"Ожидалась опция '{available_boards[0]}', "
                f"получена '{product_page.selected_board}'"
            )

    @allure.story("Добавление пиццы с опцией в корзину")
    @allure.title("Пицца с выбранным бортиком добавляется в корзину")
    def test_add_pizza_with_option_to_cart(
        self,
        opened_main_page: MainPage,
        product_page: ProductPage,
        cart_page: CartPage,
    ):
        with allure.step("Перейти на страницу первой пиццы из слайдера"):
            opened_main_page.pizza_slider.get_slide(1).go_to_product_page()

        with allure.step("Запомнить название пиццы со страницы продукта"):
            pizza_name = product_page.name

        with allure.step("Выбрать доступный бортик"):
            initial_board = product_page.selected_board
            available_boards = [
                b for b in product_page.board_options if b != initial_board
            ]
            assert available_boards, "Нет доступных опций бортика для выбора"
            selected_board = available_boards[0]
            product_page.select_board(selected_board)

        with allure.step(f"Добавить '{pizza_name}' с бортиком '{selected_board}'"):
            product_page.add_to_cart()

        with allure.step("Перейти в корзину из сообщения об успехе"):
            product_page.go_to_cart_from_message()

        with allure.step("Проверить пиццу и вариант бортика в корзине"):
            item = cart_page.find_item(pizza_name)
            assert item is not None, f"Пицца '{pizza_name}' не найдена в корзине"
            assert normalize_text(item.name) == normalize_text(pizza_name), (
                f"Название: ожидалось '{pizza_name}', получено '{item.name}'"
            )
            expected_board = selected_board.split(" - ")[0]
            actual_variation = item.variation or ""
            assert normalize_text(expected_board) in normalize_text(actual_variation), (
                f"Бортик: ожидался '{expected_board}', вариация в корзине: '{actual_variation}'"
            )
