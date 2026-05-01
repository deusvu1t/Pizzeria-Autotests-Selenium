from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    PATH = "/register/"
    USERNAME = (By.NAME, "username")
    EMAIL = (By.NAME, "email")
    PASSWORD = (By.NAME, "password")
    REGISTER = (By.NAME, "register")
    SUCCESSFULLY = (By.XPATH, "//*[contains(text(), 'Регистрация завершена')]")

    def set_name(self, name: str):
        self.input_text(self.USERNAME, name)

    def set_email(self, email: str):
        self.input_text(self.EMAIL, email)

    def set_password(self, password: str):
        self.input_text(self.PASSWORD, password)

    def register(self):
        self.click(self.REGISTER)

    def is_registered(self):
        return True if self.find_all(self.SUCCESSFULLY) else False
