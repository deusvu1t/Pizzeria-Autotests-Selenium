from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent


class SlideComponent(BaseComponent):
    TITLE = (By.TAG_NAME, "h3")
    PRICE = (By.CLASS_NAME, "amount")
    ADD_BTN = (By.CLASS_NAME, "add_to_cart_button")
    ADDED_BTN = (By.CLASS_NAME, "added_to_cart")

    @property
    def title(self) -> str:
        return self.wait.until(lambda _: self.find(self.TITLE).text.strip())

    @property
    def price(self) -> str:
        return self.wait.until(lambda _: self.find(self.PRICE).text.strip())

    def add_to_cart(self):
        self.hover()
        self.click(self.ADD_BTN)
        self.wait.until(lambda _: self.find(self.ADDED_BTN))
