import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.utils.helpers import parse_price
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HeaderComponent(BaseComponent):
    CART_CONTENTS = (By.CLASS_NAME, "cart-contents")

    def _cart_total(self) -> float:
        total = self._find_raw(self.CART_CONTENTS).text.strip()
        return parse_price(total)

    @property
    def cart_total(self) -> float:
        with allure.step("Получить текст корзины в хедере"):
            total = self.wait.until(lambda _: self._cart_total())
            logger.info("Header cart total | %s", total)
            return total

    def wait_until_cart_total(
        self,
        expected_total: float,
        tolerance: float = 0.01,
    ) -> float:
        logger.info("Wait header cart total | expected=%s", expected_total)
        with allure.step(f"Дождаться суммы корзины: {expected_total}"):

            def cart_total_is_expected(_):
                actual_total = self._cart_total()
                return (
                    actual_total
                    if abs(actual_total - expected_total) <= tolerance
                    else False
                )

            return self.wait.until(
                cart_total_is_expected
            )
