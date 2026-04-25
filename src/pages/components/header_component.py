import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HeaderComponent(BaseComponent):
    CART_CONTENTS = (By.CLASS_NAME, "cart-contents")

    @property
    def title(self) -> str:
        with allure.step("Получить текст корзины в хедере"):
            title = self.wait.until(
                lambda _: self.find(self.CART_CONTENTS).text.strip()
            )
            logger.info("Header cart text | %s", title)
            return title
