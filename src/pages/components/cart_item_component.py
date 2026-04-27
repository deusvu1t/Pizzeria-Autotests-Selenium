import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.utils.helpers import normalize_text, parse_price
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CartItemComponent(BaseComponent):
    REMOVE_BTN = (By.CSS_SELECTOR, "a .remove")
    NAME = (By.CSS_SELECTOR, ".product-name a")
    VARIATION = (By.CSS_SELECTOR, ".variation p")
    PRICE = (By.CSS_SELECTOR, ".product-price bdi")
    QUANTITY = (By.CLASS_NAME, "qty")
    SUBTOTAL = (By.CSS_SELECTOR, ".product-subtotal bdi")

    @property
    def name(self) -> str:
        self.wait.until(lambda _: self.find(self.NAME).text.strip() != "")
        return normalize_text(self.find(self.NAME).text)
    @property
    def variation(self):
        text = self.find(self.VARIATION).text
        return text


    @property
    def price(self) -> float:
        return parse_price(self.find(self.PRICE).text)

    @property
    def quantity(self) -> int:
        val = self.find(self.QUANTITY).get_attribute("value")
        return int(val) if val else 0

    @allure.step("Удалить товар из корзины")
    def remove(self):
        logger.info("Removing item: %s", self.name)
        self.click(self.REMOVE_BTN)
