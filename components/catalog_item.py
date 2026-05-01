import allure
from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class CatalogItem(BaseComponent):
    NAME = (By.CSS_SELECTOR, "h3")
    PRICE = (By.CSS_SELECTOR, ".price bdi")
    ADD_BUTTON = (By.CSS_SELECTOR, ".add_to_cart_button")
    ADDED_BUTTON = (By.CLASS_NAME, "added_to_cart")

    @property
    def name(self) -> str:
        return self.get_text(self.NAME)

    @property
    def price(self) -> str:
        return self.get_text(self.PRICE)

    @allure.step("Добавить товар из каталога в корзину")
    def add_to_cart(self):
        self.click(self.ADD_BUTTON)
        self.wait.until(lambda _: self.find_optional(self.ADDED_BUTTON) is not None)
