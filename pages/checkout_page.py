from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    PATH = "/checkout/"
    LOGIN = (By.CLASS_NAME, "showlogin")

    def is_login_requires(self):
        return True if self.is_visible(self.LOGIN) else False
