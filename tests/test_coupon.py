import math
import time
from datetime import date, timedelta

import allure
import pytest

from pages.account_page import AccountPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage, DeliveryData
from pages.main_page import MainPage
from pages.register_page import RegisterPage

VALID_COUPON = "GIVEMEHALYAVA"
INVALID_COUPON = "DC120"
DISCOUNT_RATE = 0.10


def _add_pizza_to_cart(main_page: MainPage):
    main_page.open()
    main_page.pizza_slider.get_slide(1).add_to_cart()
    main_page.header.go_to_cart()


def _delivery_data(email: str = "test_coupon@mail.test") -> DeliveryData:
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    return DeliveryData(
        first_name="Андрей",
        last_name="Тестов",
        address="ул. Пушкина, д. 1",
        city="Москва",
        state="Московская область",
        postcode="101000",
        phone="+79001234567",
        email=email,
        delivery_date=tomorrow,
    )


@allure.feature("Промокод")
class TestCoupon:
    @allure.story("Применение купона")
    @allure.title("Валидный купон GIVEMEHALYAVA снижает итоговую сумму на 10%")
    def test_valid_coupon_applies_10_percent_discount(
        self, main_page: MainPage, cart_page: CartPage
    ):
        with allure.step("Добавить пиццу в корзину и перейти в корзину"):
            _add_pizza_to_cart(main_page)

        with allure.step("Запомнить сумму до применения купона"):
            price_before = cart_page.get_total_price()

        with allure.step(f"Применить купон «{VALID_COUPON}»"):
            cart_page.apply_coupon(VALID_COUPON)
            assert cart_page.is_coupon_applied(), (
                "Сообщение об успешном применении купона не появилось"
            )

        with allure.step("Проверить, что итоговая сумма уменьшилась на 10%"):
            price_after = cart_page.get_total_price()
            expected_price = math.floor(price_before * (1 - DISCOUNT_RATE))
            assert price_after == expected_price, (
                f"Сумма после скидки: ожидалось {expected_price} ₽, "
                f"получено {price_after} ₽ (до скидки: {price_before} ₽)"
            )

    @allure.story("Применение купона")
    @allure.title("Несуществующий купон DC120 не применяется и сумма остаётся прежней")
    def test_invalid_coupon_does_not_change_total(
        self, main_page: MainPage, cart_page: CartPage
    ):
        with allure.step("Добавить пиццу в корзину и перейти в корзину"):
            _add_pizza_to_cart(main_page)

        with allure.step("Запомнить сумму до ввода купона"):
            price_before = cart_page.get_total_price()

        with allure.step(f"Применить несуществующий купон «{INVALID_COUPON}»"):
            cart_page.apply_coupon(INVALID_COUPON)

        with allure.step("Проверить, что появилось сообщение об ошибке"):
            assert cart_page.is_coupon_error_shown(), (
                "Сообщение об ошибке купона не появилось"
            )

        with allure.step("Проверить, что итоговая сумма не изменилась"):
            price_after = cart_page.get_total_price()
            assert price_after == price_before, (
                f"Сумма изменилась: до {price_before} ₽, после {price_after} ₽"
            )

    @allure.story("Применение купона")
    @allure.title(
        "Купон не применяется и сумма не меняется при недоступности сервера (500)"
    )
    @pytest.mark.skipif(
        condition=pytest.importorskip("selenium", minversion="4.0.0") is None,
        reason="Требуется Selenium 4+ и Chrome",
    )
    def test_coupon_server_returns_500(self, main_page: MainPage, cart_page: CartPage):
        driver = cart_page.driver

        with allure.step("Добавить пиццу в корзину и перейти в корзину"):
            _add_pizza_to_cart(main_page)

        with allure.step("Запомнить сумму до ввода купона"):
            price_before = cart_page.get_total_price()

        with allure.step("Включить CDP Network и заблокировать запросы купона"):
            driver.execute_cdp_cmd("Network.enable", {})
            driver.execute_cdp_cmd(
                "Network.setBlockedURLs",
                {
                    "urls": [
                        "*wc-ajax=apply_coupon*",
                        "*wc-ajax=get_refreshed_fragments*",
                    ]
                },
            )

        try:
            with allure.step(f"Попытаться применить купон «{VALID_COUPON}»"):
                cart_page.input_text(cart_page.COUPON_INPUT, VALID_COUPON)
                cart_page.click(cart_page.COUPON_APPLY_BUTTON)

            with allure.step("Проверить, что купон не применился"):
                assert not cart_page.is_coupon_applied(), (
                    "Купон применился, хотя запрос к серверу был заблокирован"
                )

            with allure.step("Проверить, что итоговая сумма не изменилась"):
                price_after = cart_page.get_total_price()
                assert price_after == price_before, (
                    f"Сумма изменилась: до {price_before} ₽, после {price_after} ₽"
                )
        finally:
            with allure.step("Снять блокировку и отключить CDP Network"):
                driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": []})
                driver.execute_cdp_cmd("Network.disable", {})

    @allure.story("Ограничение купона")
    @allure.title(
        "Купон GIVEMEHALYAVA не применяется повторно для того же пользователя"
    )
    def test_coupon_cannot_be_used_twice(
        self,
        main_page: MainPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        account_page: AccountPage,
        register_page: RegisterPage,
    ):
        ts = int(time.time())
        username = f"coupon_user_{ts}"
        email = f"coupon_{ts}@mail.test"
        password = "Test1234!"

        with allure.step(f"Зарегистрировать нового пользователя «{username}»"):
            main_page.open()
            main_page.header.go_to_account()
            account_page.go_to_register()
            register_page.set_name(username)
            register_page.set_email(email)
            register_page.set_password(password)
            register_page.register()
            assert register_page.is_registered(), "Регистрация не прошла"

        with allure.step("Добавить пиццу и применить купон в первый раз"):
            main_page.open()
            main_page.pizza_slider.get_slide(1).add_to_cart()
            main_page.header.go_to_cart()
            cart_page.apply_coupon(VALID_COUPON)
            assert cart_page.is_coupon_applied(), (
                "Купон не применился при первом использовании"
            )

        with allure.step("Оформить первый заказ"):
            cart_page.checkout()
            checkout_page.fill_delivery_form(_delivery_data(email=email))
            checkout_page.select_payment_cod()
            checkout_page.accept_terms()
            checkout_page.place_order()
            summary = checkout_page.get_order_summary()
            assert summary.order_number, "Первый заказ не оформлен"

        with allure.step("Добавить пиццу для второго заказа"):
            main_page.open()
            main_page.pizza_slider.get_slide(1).add_to_cart()
            main_page.header.go_to_cart()

        with allure.step("Запомнить сумму до ввода купона"):
            price_before = cart_page.get_total_price()

        with allure.step(f"Попытаться применить купон «{VALID_COUPON}» повторно"):
            cart_page.apply_coupon(VALID_COUPON)

        with allure.step("Проверить, что купон не применился повторно"):
            assert cart_page.is_coupon_error_shown(), (
                "Ожидалось сообщение об ошибке при повторном применении купона"
            )
            price_after = cart_page.get_total_price()
            assert price_after == price_before, (
                f"Сумма изменилась при повторном применении купона: "
                f"до {price_before} ₽, после {price_after} ₽"
            )
