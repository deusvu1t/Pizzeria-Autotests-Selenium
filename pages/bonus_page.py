import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class BonusPage(BasePage):
    PATH = "/bonus/"
    USERNAME = (By.NAME, "username")
    PHONE = (By.NAME, "billing_phone")
    SUBMIT = (By.NAME, "bonus")
    VALIDATION_BLOCK = (By.ID, "bonus_content")
    SUCCESS_BLOCK = (By.ID, "bonus_main")
    SUCCESS_TEXT = "Ваша карта оформлена!"

    # ------------------------------------------------------------------

    @allure.step("Ввести имя: {name}")
    def set_name(self, name: str):
        self.input_text(self.USERNAME, name)

    @allure.step("Ввести телефон: {phone}")
    def set_phone(self, phone: str):
        self.input_text(self.PHONE, phone)

    @allure.step("Нажать «Оформить карту»")
    def submit(self):
        self.click(self.SUBMIT)

    @allure.step("Подтвердить всплывающее окно (alert)")
    def accept_alert(self):

        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        self.logger.info(f"Alert текст: {alert_text}")
        alert.accept()
        return alert_text

    @allure.step("Заполнить форму и оформить бонусную карту")
    def register_bonus_card(self, name: str, phone: str) -> str:

        self.set_name(name)
        self.set_phone(phone)
        self.submit()
        return self.accept_alert()

    def get_validation_text(self) -> str:

        return self.get_text(self.VALIDATION_BLOCK)

    def is_success(self) -> bool:

        try:
            self.wait.until(
                lambda _: (
                    self.SUCCESS_TEXT
                    in self.driver.find_element(*self.SUCCESS_BLOCK).text
                )
            )
            return True
        except Exception:
            return False
