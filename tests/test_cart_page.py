import time
import allure
import math
from src.pages.cart_page import CartPage
from src.pages.main_page import MainPage
from src.pages.product_page import ProductPage

@allure.feature("Страница корзины")
class TestCartPage:
    @allure.story("Состав корзины")
    @allure.title("Проверка состава корзины после добавления пицц")
    def test_cart_content_after_adding_items(self, main_page: MainPage, product_page: ProductPage, cart_page: CartPage):
        with allure.step("1. Добавить в корзину несколько пицц из слайдера."):
            main_page.open()
            slider = main_page.pizza_slider()
            p1 = slider.slides()[0]
            p1_name = p1.title
            p1.add_to_cart()
            p2 = slider.slides()[1]
            p2_name = p2.title
            p2.add_to_cart()
        with allure.step("2. Добавить в корзину пиццу с дополнительной опцией со страницы подробностей."):
            product_page.open("пицца-4-в-1")
            product_page.board_pack("Сырный")
            p3_name = 'пицца "4 в 1"'
            product_page.add_to_cart()
        with allure.step("3. Открыть корзину."):
            cart_page.open()
        with allure.step("Ожидаемый результат: все добавленные пиццы отображаются в корзине."):
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
                    if item.variation: assert "сыр" in item.variation.lower()
            total_items_price = sum(item.price * item.quantity for item in cart_page.items())
            assert math.isclose(cart_page.order_total, total_items_price, abs_tol=0.1)

    @allure.story("Количество товара")
    @allure.title("Увеличение количества пиццы в корзине")
    def test_increase_item_quantity_in_cart(self, main_page: MainPage, cart_page: CartPage):
        with allure.step("Подготовка: добавить несколько товаров в корзину."):
            main_page.open()
            slider = main_page.pizza_slider()
            slider.slides()[0].add_to_cart()
            slider.slides()[1].add_to_cart()
        with allure.step("1. Открыть корзину с несколькими товарами."):
            cart_page.open()
            initial_total = cart_page.order_total
        with allure.step("2. Выбрать одну позицию с пиццей."):
            items = cart_page.items()
            target_item = items[0]
            initial_quantity = target_item.quantity
            initial_price = target_item.price
        with allure.step("3. Увеличить количество этой позиции."):
            new_quantity = initial_quantity + 1
            target_item.set_quantity(new_quantity)
        with allure.step("4. Нажать кнопку 'Обновить корзину'."):
            cart_page.update_cart()
        with allure.step("Ожидаемый результат: количество обновлено, стоимость пересчитана."):
            items_after = cart_page.items()
            updated_item = items_after[0]
            assert updated_item.quantity == new_quantity
            expected_total = initial_total + initial_price
            assert math.isclose(cart_page.order_total, expected_total, abs_tol=0.1)

    @allure.story("Удаление товара")
    @allure.title("Удаление пиццы с дополнительной опцией из корзины")
    def test_remove_item_with_extra_option_from_cart(self, main_page: MainPage, product_page: ProductPage, cart_page: CartPage):
        with allure.step("Подготовка: добавить товары в корзину."):
            main_page.open()
            main_page.pizza_slider().slides()[0].add_to_cart()
            product_page.open("пицца-4-в-1")
            product_page.board_pack("Сырный")
            p_extra_name = 'пицца "4 в 1"'
            product_page.add_to_cart()
        with allure.step("1. Открыть корзину, в которой есть пицца с дополнительной опцией."):
            cart_page.open()
            items_before = cart_page.items()
            assert len(items_before) >= 2
        with allure.step("2. Найти позицию с дополнительной опцией."):
            target_item = next(item for item in cart_page.items() if item.variation and "сыр" in item.variation.lower())
        with allure.step("3. Удалить эту позицию из корзины."):
            target_item.remove()
            time.sleep(2); cart_page.wait.until(lambda _: len(cart_page.items()) == len(items_before) - 1)
        with allure.step("Ожидаемый результат: позиция удалена, сумма пересчитана."):
            items_after = cart_page.items()
            assert len(items_after) == len(items_before) - 1
            for item in items_after:
                if item.variation:
                    assert "сыр" not in item.variation.lower()
