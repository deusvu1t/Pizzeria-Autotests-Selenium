import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.utils.helpers import parse_price
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HeaderComponent(BaseComponent):
    CART_CONTENTS = (By.CLASS_NAME, "cart-contents")

    @property
    def cart_total(self) -> float:
        total_text = self.find(self.CART_CONTENTS).text
        logger.info("Cart total in header: %s", total_text)
        return parse_price(total_text)

    @allure.step("Перейти в корзину через хедер")
    def go_to_cart(self):
        # click() внутри заново выполнит find(), что в сочетании с
        # динамическим header в BasePage уберет ошибку StaleElement
        self.click(self.CART_CONTENTS)
