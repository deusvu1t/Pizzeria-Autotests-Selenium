import time
import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AccountPage(BasePage):
    REG_USERNAME = (By.ID, "reg_username")
    REG_EMAIL = (By.ID, "reg_email")
    REG_PASSWORD = (By.ID, "reg_password")
    REGISTER_BTN = (By.NAME, "register")
    LOGOUT_LINK = (By.XPATH, "//a[contains(@href, 'customer-logout')]")
    REGISTER_FORM_WRAPPER = (By.CLASS_NAME, "u-column2")
    CUSTOM_REGISTER_BTN = (By.CLASS_NAME, "custom-register-button")

    @allure.step("Открыть страницу 'Мой аккаунт'")
    def open(self, path: str = "my-account/") -> None:
        return super().open(path)

    @allure.step("Нажать на кнопку 'Зарегистрироваться' (переход к форме)")
    def click_custom_register(self):
        try:
            self.click(self.CUSTOM_REGISTER_BTN)
        except Exception:
            pass

    @allure.step("Заполнить форму регистрации")
    def register(self, username, email, password):
        self.find(self.REG_USERNAME).send_keys(username)
        self.find(self.REG_EMAIL).send_keys(email)
        self.find(self.REG_PASSWORD).send_keys(password)
        self.click(self.REGISTER_BTN)
        time.sleep(2)

    @allure.step("Проверить, авторизован ли пользователь")
    def is_logged_in(self):
        try:
            self.wait.until(lambda _: self.is_visible((By.XPATH, "//*[contains(text(), 'Выйти') or contains(text(), 'Logout')]"), timeout=2) or self.is_visible((By.CLASS_NAME, 'woocommerce-MyAccount-content'), timeout=2))
            return True
        except:
            return False
