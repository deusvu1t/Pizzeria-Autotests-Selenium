import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.utils.helpers import normalize_text, parse_price
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SlideComponent(BaseComponent):
    TITLE = (By.TAG_NAME, "h3")
    PRICE = (By.CLASS_NAME, "amount")
    ADD_BTN = (By.CLASS_NAME, "add_to_cart_button")
    ADDED_BTN = (By.CLASS_NAME, "added_to_cart")
    IMG = (By.TAG_NAME, "img")

    @property
    def title(self) -> str:
        self.wait.until(lambda _: self.find(self.TITLE).text.strip() != "")
        text = self.find(self.TITLE).text.strip()
        logger.info("Slide product title: %s", text)
        return normalize_text(text)

    @property
    def price(self) -> float:
        # Ждем появления цифр цены
        self.wait.until(lambda _: self.find(self.PRICE).text.strip() != "")
        text = self.find(self.PRICE).text.strip()
        logger.info("Slide product price: %s", text)
        return parse_price(text)

    def is_add_to_cart_button_visible(self) -> bool:
        self.hover()
        return self.is_visible(self.ADD_BTN)

    @allure.step("Добавить продукт в корзину со слайда")
    def add_to_cart(self):
        self.hover()
        self.click(self.ADD_BTN)
        self.wait.until(lambda _: self.is_visible(self.ADDED_BTN))

    @allure.step("Перейти в карточку товара")
    def go_to_details_page(self):
        self.click(self.IMG)
