import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class Slide(BaseComponent):
    ADD_BUTTON = (By.CLASS_NAME, "add_to_cart_button")
    ADDED_BUTTON = (By.CLASS_NAME, "added_to_cart")
    NAME = (By.CSS_SELECTOR, "h3")
    PRICE = (By.CSS_SELECTOR, ".price")
    IMG = (By.CLASS_NAME, "item-img")

    @property
    def name(self) -> str:
        return self.get_text(self.NAME)

    @property
    def price(self) -> str:
        return self.get_text(self.PRICE)

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self):
        self.hover_self()
        self.click(self.ADD_BUTTON)
        self.wait.until(lambda d: self.find_optional(self.ADDED_BUTTON) is not None)

    @allure.step("Перейти на страницу товара")
    def go_to_product_page(self):
        self.click(self.IMG)
