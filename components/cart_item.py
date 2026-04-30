from selenium.webdriver.common.by import By

from components.base_component import BaseComponent


class CartItem(BaseComponent):
    NAME = (By.CSS_SELECTOR, ".product-name a")
    VARIATION = (By.CSS_SELECTOR, ".variation")
    PRICE = (By.CSS_SELECTOR, ".product-price .amount")
    QUANTITY = (By.CSS_SELECTOR, "input.qty")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".remove")

    @property
    def name(self) -> str:
        return self.get_text(self.NAME)

    @property
    def variation(self) -> str | None:
        element = self.find_optional(self.VARIATION)
        return element.text if element else None

    @property
    def price(self) -> str:
        return self.get_text(self.PRICE)

    @property
    def quantity(self) -> str:
        value = self.find(self.QUANTITY).get_attribute("value") or ""
        self.logger.debug(f"Получено количество: {value}")
        return value

    def remove(self):
        self.click(self.REMOVE_BUTTON)
