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
        with allure.step("Получить текст корзины в хедере"):
            total = self.find(self.CART_CONTENTS).text
            logger.info("Header cart total | %s", total)
            return parse_price(total)
