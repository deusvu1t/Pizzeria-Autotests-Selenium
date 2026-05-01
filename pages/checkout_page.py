from dataclasses import dataclass

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


@dataclass
class DeliveryData:
    """Данные для заполнения формы доставки."""

    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    postcode: str
    phone: str
    email: str
    delivery_date: str = ""
    payment_method: str = "При доставке"


@dataclass
class OrderSummary:
    order_number: str
    total: str
    payment_method: str
    first_name: str
    last_name: str
    address: str
    email: str


class CheckoutPage(BasePage):
    PATH = "/checkout/"
    LOGIN_NOTICE = (By.CLASS_NAME, "showlogin")
    FIRST_NAME = (By.ID, "billing_first_name")
    LAST_NAME = (By.ID, "billing_last_name")
    ADDRESS = (By.ID, "billing_address_1")
    CITY = (By.ID, "billing_city")
    STATE = (By.ID, "billing_state")  # Поле «Область»
    POSTCODE = (By.ID, "billing_postcode")
    PHONE = (By.ID, "billing_phone")
    EMAIL = (By.ID, "billing_email")
    DELIVERY_DATE = (By.ID, "order_date")
    PAYMENT_COD = (By.ID, "payment_method_cod")  # «При доставке»
    TERMS_CHECKBOX = (By.ID, "terms")
    PLACE_ORDER = (By.ID, "place_order")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".woocommerce-order-overview__order strong")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".woocommerce-order-overview__total strong")
    ORDER_PAYMENT = (
        By.CSS_SELECTOR,
        ".woocommerce-order-overview__payment-method strong",
    )
    CONFIRM_NAME = (By.CSS_SELECTOR, ".woocommerce-customer-details address")

    def is_login_required(self) -> bool:
        return self.is_visible(self.LOGIN_NOTICE)

    @allure.step("Заполнить форму доставки")
    def fill_delivery_form(self, data: DeliveryData):
        self.input_text(self.FIRST_NAME, data.first_name)
        self.input_text(self.LAST_NAME, data.last_name)
        self.input_text(self.ADDRESS, data.address)
        self.input_text(self.CITY, data.city)
        self.input_text(self.STATE, data.state)
        self.input_text(self.POSTCODE, data.postcode)
        self.input_text(self.PHONE, data.phone)
        self.input_text(self.EMAIL, data.email)
        if data.delivery_date:
            self._set_delivery_date(data.delivery_date)

    @allure.step("Выбрать дату доставки: {date}")
    def _set_delivery_date(self, date: str):
        self.input_text(self.DELIVERY_DATE, date)

    @allure.step("Выбрать оплату при доставке")
    def select_payment_cod(self):
        self.click(self.PAYMENT_COD)

    @allure.step("Принять условия соглашения")
    def accept_terms(self):
        self.click(self.TERMS_CHECKBOX)

    @allure.step("Подтвердить заказ")
    def place_order(self):
        self.click(self.PLACE_ORDER)

    @allure.step("Получить данные подтверждённого заказа")
    def get_order_summary(self) -> OrderSummary:
        address_block = self.get_text(self.CONFIRM_NAME)
        lines = [line.strip() for line in address_block.splitlines() if line.strip()]
        first_name, last_name = (lines[0].split(" ", 1) + [""])[:2]
        return OrderSummary(
            order_number=self.get_text(self.ORDER_NUMBER),
            total=self.get_text(self.ORDER_TOTAL),
            payment_method=self.get_text(self.ORDER_PAYMENT),
            first_name=first_name,
            last_name=last_name,
            address=lines[1] if len(lines) > 1 else "",
            email="",
        )
