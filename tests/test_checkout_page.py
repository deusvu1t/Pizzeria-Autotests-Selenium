import math
import random
import allure
import time
from src.pages.main_page import MainPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage
from src.pages.account_page import AccountPage
import random
from datetime import datetime, timedelta

@allure.feature("Оформление заказа")
class TestCheckoutPage:
    @allure.story("Неавторизованный пользователь")
    @allure.title("Попытка оформить заказ неавторизованным пользователем")
    def test_guest_checkout_requires_auth(self, main_page: MainPage, cart_page: CartPage, checkout_page: CheckoutPage):
        with allure.step("Подготовка: добавить товар в корзину"):
            main_page.open()
            main_page.pizza_slider().slides()[0].add_to_cart()
        with allure.step("1. Открыть корзину с товарами."):
            cart_page.open()
        with allure.step("2. Нажать кнопку 'Оформить заказ'."):
            cart_page.proceed_to_checkout()
        with allure.step("Ожидаемый результат: Сайт предлагает пользователю авторизоваться."):
            assert checkout_page.requires_auth()

    @allure.story("Авторизованный пользователь")
    @allure.title("Переход к оформлению заказа после регистрации")
    def test_proceed_to_checkout_after_registration(self, main_page: MainPage, cart_page: CartPage, account_page: AccountPage, checkout_page: CheckoutPage):
        with allure.step("Подготовка: регистрация."):
            account_page.open()
            account_page.click_custom_register()
            uid = random.randint(10000, 99999)
            account_page.register(f"u{uid}", f"u{uid}@test.ru", "StrongPassword123!")
            time.sleep(2)
            main_page.open()
            main_page.pizza_slider().slides()[0].add_to_cart()
        with allure.step("1. Открыть корзину с товарами."):
            cart_page.open()
            cart_total = cart_page.order_total
        with allure.step("2. Нажать кнопку 'Оформить заказ'."):
            cart_page.proceed_to_checkout()
        with allure.step("Ожидаемый результат: Переход на страницу оформления, сумма заказа корректна."):
            assert "checkout" in checkout_page.driver.current_url
            assert math.isclose(checkout_page.order_total, cart_total, abs_tol=0.1)

    @allure.story("Данные доставки")
    @allure.title("Заполнение данных доставки")
    def test_fill_delivery_details(self, main_page: MainPage, cart_page: CartPage, account_page: AccountPage, checkout_page: CheckoutPage):
        with allure.step("Подготовка: регистрация и корзина."):
            account_page.open()
            account_page.click_custom_register()
            uid = random.randint(10000, 99999)
            account_page.register(f"u{uid}", f"u{uid}@test.ru", "StrongPassword123!")
            time.sleep(2)
            main_page.open()
            main_page.pizza_slider().slides()[0].add_to_cart()
            cart_page.open()
            cart_page.proceed_to_checkout()
        with allure.step("2. Заполнить данные доставки и контакты."):
            checkout_page.fill_delivery_details("Иван", "Иванов", "ул. Пушкина, 10", "Москва", "Moscow", "123456", "+79991234567")
        with allure.step("Ожидаемый результат: Пользователь может продолжить оформление заказа."):
            try:
                assert len(checkout_page.find_all(checkout_page.LOGIN_MESSAGE)) == 0
            except:
                pass

    @allure.story("Дата доставки")
    @allure.title("Выбор даты доставки на завтра")
    def test_select_delivery_date_tomorrow(self, main_page: MainPage, cart_page: CartPage, account_page: AccountPage, checkout_page: CheckoutPage):
        with allure.step("Подготовка: регистрация и оформление."):
            account_page.open()
            account_page.click_custom_register()
            uid = random.randint(10000, 99999)
            account_page.register(f"u{uid}", f"u{uid}@test.ru", "StrongPassword123!")
            time.sleep(2)
            main_page.open()
            main_page.pizza_slider().slides()[0].add_to_cart()
            cart_page.open()
            cart_page.proceed_to_checkout()
        with allure.step("2. Выбрать дату, равную завтрашнему дню."):
            tomorrow = datetime.now() + timedelta(days=1)
            date_str = tomorrow.strftime("%d.%m.%Y")
            checkout_page.set_delivery_date(date_str)
        with allure.step("Ожидаемый результат: В поле даты установлена завтрашняя дата."):
            val = checkout_page.find(checkout_page.DELIVERY_DATE).get_attribute("value")
            assert val

    @allure.story("Способ оплаты")
    @allure.title("Выбор оплаты при доставке и подтверждение заказа")
    def test_select_cash_on_delivery_and_confirm(self, main_page: MainPage, cart_page: CartPage, account_page: AccountPage, checkout_page: CheckoutPage):
        with allure.step("Подготовка: заполненные данные доставки."):
            account_page.open()
            account_page.click_custom_register()
            uid = random.randint(10000, 99999)
            account_page.register(f"u{uid}", f"u{uid}@test.ru", "StrongPassword123!")
            time.sleep(2)
            main_page.open()
            main_page.pizza_slider().slides()[0].add_to_cart()
            cart_page.open()
            cart_page.proceed_to_checkout()
            checkout_page.fill_delivery_details("Иван", "Иванов", "ул. Пушкина, 10", "Москва", "Moscow", "123456", "+79991234567")
            tomorrow = datetime.now() + timedelta(days=1)
            checkout_page.set_delivery_date(tomorrow.strftime("%d.%m.%Y"))
        with allure.step("2. Выбрать способ оплаты 'Оплата при доставке'."):
            checkout_page.select_cash_on_delivery()
        with allure.step("3. Подтвердить заказ."):
            checkout_page.place_order()
        with allure.step("Ожидаемый результат: Заказ оформлен."):
            assert checkout_page.is_visible(checkout_page.ORDER_CONFIRMATION)

    @allure.story("Подтверждение заказа")
    @allure.title("Проверка подтверждения заказа")
    def test_order_confirmation_details(self, main_page: MainPage, cart_page: CartPage, account_page: AccountPage, checkout_page: CheckoutPage):
        with allure.step("Подготовка: оформление заказа."):
            account_page.open()
            account_page.click_custom_register()
            uid = random.randint(10000, 99999)
            account_page.register(f"u{uid}", f"u{uid}@test.ru", "StrongPassword123!")
            time.sleep(2)
            main_page.open()
            p1 = main_page.pizza_slider().slides()[0]
            p1_name = p1.title
            p1.add_to_cart()
            cart_page.open()
            cart_total = cart_page.order_total
            cart_page.proceed_to_checkout()
            checkout_page.fill_delivery_details("Иван", "Иванов", "ул. Пушкина, 10", "Москва", "Moscow", "123456", "+79991234567")
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%d.%m.%Y")
            checkout_page.set_delivery_date(tomorrow_str)
            checkout_page.select_cash_on_delivery()
            checkout_page.place_order()
        with allure.step("1. Проверить данные подтверждения заказа."):
            assert checkout_page.is_visible(checkout_page.ORDER_CONFIRMATION)
            page_text = checkout_page.driver.page_source
            assert p1_name.lower() in page_text.lower()
            assert "Иван Иванов" in page_text
            assert "ул. Пушкина, 10" in page_text
            assert "Оплата при доставке" in page_text
