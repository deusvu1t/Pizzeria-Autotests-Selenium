import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SlideComponent(BaseComponent):
    TITLE = (By.TAG_NAME, "h3")
    PRICE = (By.CLASS_NAME, "amount")
    ADD_BTN = (By.CLASS_NAME, "add_to_cart_button")
    ADDED_BTN = (By.CLASS_NAME, "added_to_cart")

    @property
    def title(self) -> str:
        with allure.step("Получить название пиццы на слайде"):
            title = self.wait.until(lambda _: self.find(self.TITLE).text.strip())
            logger.info("Slide title | %s", title)
            return title

    @property
    def price(self) -> str:
        with allure.step("Получить цену пиццы на слайде"):
            price = self.wait.until(lambda _: self.find(self.PRICE).text.strip())
            logger.info("Slide price | %s", price)
            return price

    def is_add_to_cart_button_visible(self) -> bool:
        self.hover()
        return self.is_visible(self.ADD_BTN)

    def add_to_cart(self):
        logger.info("Add slide product to cart")
        with allure.step("Добавить пиццу из слайда в корзину"):
            self.hover()
            self.click(self.ADD_BTN)
            self.wait.until(lambda _: self.find(self.ADDED_BTN))
