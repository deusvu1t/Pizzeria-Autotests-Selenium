from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AccountPage(BasePage):
    PATH = "/my-account/"
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN = (By.NAME, "login")
    REGISTER = (By.CLASS_NAME, "custom-register-button")
    HELLO_MESSAGE = (By.XPATH, "//p[contains(text(), 'Привет ')]")

    def set_username(self, username):
        self.input_text(self.USERNAME, username)

    def set_password(self, password):
        self.input_text(self.PASSWORD, password)

    def login(self):
        self.click(self.LOGIN)

    def is_authorized(self):
        return True if self.find_all(self.HELLO_MESSAGE) else False

    def register(self):
        self.click(self.REGISTER)
