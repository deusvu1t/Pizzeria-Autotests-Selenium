import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.pages.base_page import BasePage
from src.utils.helpers import parse_price
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CheckoutPage(BasePage):
    LOGIN_MESSAGE = (By.CLASS_NAME, "woocommerce-error")
    SHOW_LOGIN_LINK = (By.CLASS_NAME, "showlogin")

    FIRST_NAME = (By.ID, "billing_first_name")
    LAST_NAME = (By.ID, "billing_last_name")
    ADDRESS = (By.ID, "billing_address_1")
    CITY = (By.ID, "billing_city")
    STATE = (By.ID, "billing_state")
    POSTCODE = (By.ID, "billing_postcode")
    PHONE = (By.ID, "billing_phone")
    EMAIL = (By.ID, "billing_email")
    DELIVERY_DATE = (By.ID, "order_date")

    PAYMENT_METHOD_COD = (By.ID, "payment_method_cod")
    PLACE_ORDER_BTN = (By.ID, "place_order")

    ORDER_CONFIRMATION = (By.CLASS_NAME, "woocommerce-order-overview__order")
    ORDER_TOTAL = (By.CSS_SELECTOR, "tr.order-total .amount")

    @allure.step("Открыть оформление заказа")
    def open(self, path: str = "checkout/") -> None:
        return super().open(path)

    def requires_auth(self) -> bool:
        return self.is_visible(self.SHOW_LOGIN_LINK)

    @allure.step("Заполнить данные доставки")
    def fill_delivery_details(self, first_name, last_name, address, city, state, postcode, phone):
        self.wait.until(lambda _: self.find(self.FIRST_NAME).is_displayed())
        time.sleep(2) # Give it a bit to load blocks
        try:
            self.find(self.EMAIL).clear()
            self.find(self.EMAIL).send_keys("test@test.com")
        except:
            pass
        self.find(self.FIRST_NAME).clear()
        self.find(self.FIRST_NAME).send_keys(first_name)
        self.find(self.LAST_NAME).clear()
        self.find(self.LAST_NAME).send_keys(last_name)
        self.find(self.ADDRESS).clear()
        self.find(self.ADDRESS).send_keys(address)
        self.find(self.CITY).clear()
        self.find(self.CITY).send_keys(city)
        try:
            self.find(self.STATE).clear()
            self.find(self.STATE).send_keys(state)
        except:
            pass
        self.find(self.POSTCODE).clear()
        self.find(self.POSTCODE).send_keys(postcode)
        self.find(self.PHONE).clear()
        self.find(self.PHONE).send_keys(phone)
        time.sleep(2)

    @allure.step("Выбрать дату доставки")
    def set_delivery_date(self, date_str: str):
        el = self.find(self.DELIVERY_DATE)
        try:
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", el)
            el.clear()
            el.send_keys(date_str)
        except:
            self.driver.execute_script(f"arguments[0].value = '{date_str}';", el)
        time.sleep(1)

    @allure.step("Выбрать оплату при доставке")
    def select_cash_on_delivery(self):
        el = self.find(self.PAYMENT_METHOD_COD)
        if not el.is_selected():
            self.driver.execute_script("arguments[0].click();", el)

    @allure.step("Подтвердить заказ")
    def place_order(self):
        time.sleep(2)
        try:
            terms = self.driver.find_element(By.ID, "terms")
            self.driver.execute_script("arguments[0].click();", terms)
        except:
            pass
        self.wait.until(lambda _: self.find(self.PLACE_ORDER_BTN).is_enabled())
        self.driver.execute_script("arguments[0].click();", self.find(self.PLACE_ORDER_BTN))
        try:
            self.wait.until(lambda _: self.is_visible(self.ORDER_CONFIRMATION, timeout=10))
        except:
            print("Checkout errors: ", [el.text for el in self.find_all(self.LOGIN_MESSAGE)])
            raise

    @property
    def order_total(self) -> float:
        time.sleep(1)
        text = self.find(self.ORDER_TOTAL).text
        return parse_price(text)
