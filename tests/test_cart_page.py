import allure

from pages.cart_page import CartPage
from pages.main_page import MainPage


class TestCartPage:
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
