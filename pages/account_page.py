import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AccountPage(BasePage):
    PATH = "/my-account/"
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.NAME, "login")
    REGISTER_BUTTON = (By.CLASS_NAME, "custom-register-button")
    HELLO_MESSAGE = (By.XPATH, "//p[contains(text(), 'Привет ')]")

    @allure.step("Ввести логин")
    def set_username(self, username: str):
        self.input_text(self.USERNAME, username)

    @allure.step("Ввести пароль")
    def set_password(self, password: str):
        self.input_text(self.PASSWORD, password)

    @allure.step("Нажать кнопку «Войти»")
    def submit_login(self):
        self.click(self.LOGIN_BUTTON)

    @allure.step("Войти в аккаунт: {username}")
    def login(self, username: str, password: str):
        self.set_username(username)
        self.set_password(password)
        self.submit_login()

    def is_authorized(self) -> bool:
        return bool(self.find_all(self.HELLO_MESSAGE))

    @allure.step("Нажать кнопку «Зарегистрироваться»")
    def go_to_register(self):
        self.click(self.REGISTER_BUTTON)
