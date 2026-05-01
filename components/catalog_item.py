from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class CatalogItem(BaseComponent):
    NAME = (By.CSS_SELECTOR, "h3")
    PRICE = (By.CSS_SELECTOR, ".price bdi")
    ADD_BUTTON = (By.CSS_SELECTOR, ".add_to_cart_button")

    @property
    def name(self) -> str:
        return self.get_text(self.NAME)

    @property
    def price(self) -> str:
        return self.get_text(self.PRICE)

    def add_to_cart(self):
        self.click(self.ADD_BUTTON)
