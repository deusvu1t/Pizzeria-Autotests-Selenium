from datetime import date, timedelta

import allure

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage, DeliveryData
from pages.main_page import MainPage


@allure.feature("Оформление заказа")
class TestCheckoutPage:
    @allure.story("Требование авторизации")
    @allure.title(
        "Неавторизованный пользователь видит предложение войти при оформлении"
    )
    def test_requires_login_when_proceeding_to_checkout(
        self,
        opened_main_page: MainPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
    ):
        with allure.step("Добавить первую пиццу из слайдера в корзину"):
            opened_main_page.pizza_slider.get_slide(1).add_to_cart()

        with allure.step("Перейти в корзину"):
            opened_main_page.header.go_to_cart()

        with allure.step("Нажать «Оформить заказ»"):
            cart_page.checkout()

        with allure.step("Проверить, что отображается предложение войти"):
            assert checkout_page.is_login_required(), (
                "Блок авторизации не отображается на странице оформления заказа"
            )

    @allure.story("Оформление заказа")
    @allure.title("Авторизованный пользователь успешно оформляет заказ с доставкой")
    def test_place_order_as_authorized_user(
        self,
        authorized_account_page,
        opened_main_page: MainPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
    ):
        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        delivery = DeliveryData(
            first_name="Андрей",
            last_name="Тестов",
            address="ул. Пушкина, д. 1",
            city="Москва",
            state="Московская область",  # Поле «Область»
            postcode="101000",
            phone="+79001234567",
            email="test_001@mail.test",
            delivery_date=tomorrow,
        )

        with allure.step("Добавить первую пиццу из слайдера в корзину"):
            pizza = opened_main_page.pizza_slider.get_slide(1)
            pizza_name = pizza.name
            pizza.add_to_cart()

        with allure.step("Перейти в корзину"):
            opened_main_page.header.go_to_cart()

        with allure.step("Запомнить содержимое корзины"):
            cart_item = cart_page.find_item(pizza_name)
            assert cart_item is not None, f"Пицца '{pizza_name}' не найдена в корзине"

        with allure.step("Перейти к оформлению заказа"):
            cart_page.checkout()

        with allure.step("Заполнить форму доставки"):
            checkout_page.fill_delivery_form(delivery)

        with allure.step("Выбрать оплату при доставке"):
            checkout_page.select_payment_cod()

        with allure.step("Принять условия соглашения"):
            checkout_page.accept_terms()

        with allure.step("Подтвердить заказ"):
            checkout_page.place_order()

        with allure.step("Проверить данные подтверждённого заказа"):
            summary = checkout_page.get_order_summary()

            assert summary.order_number, "Номер заказа не отображается"
            assert summary.first_name == delivery.first_name, (
                f"Имя: ожидалось '{delivery.first_name}', получено '{summary.first_name}'"
            )
            assert summary.last_name == delivery.last_name, (
                f"Фамилия: ожидалось '{delivery.last_name}', получено '{summary.last_name}'"
            )
            assert delivery.address in summary.address, (
                f"Адрес: ожидалось содержание '{delivery.address}', "
                f"получено '{summary.address}'"
            )
            assert summary.total, "Итоговая сумма заказа не отображается"
