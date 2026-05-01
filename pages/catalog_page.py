from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from components.catalog_item import CatalogItem
from pages.base_page import BasePage


class CatalogPage(BasePage):
    PRODUCTS = (By.CSS_SELECTOR, "ul.products li.product")
    PRICE_SLIDER_AMOUNT = (By.CSS_SELECTOR, ".price_slider_amount")
    PRICE_SLIDER = (By.CSS_SELECTOR, ".price_slider")
    MIN_PRICE_INPUT = (By.ID, "min_price")
    MAX_PRICE_INPUT = (By.ID, "max_price")
    APPLY_PRICE_FILTER = (By.CSS_SELECTOR, ".price_slider_amount button")

    @property
    def max_price(self) -> int:
        return int(
            self._find_hidden(self.MAX_PRICE_INPUT).get_attribute("value") or "0"
        )

    def get_products(self) -> list[CatalogItem]:
        elements = self.find_all(self.PRODUCTS)
        return [CatalogItem(el, self) for el in elements]

    def set_max_price_filter(self, max_price: int, apply: bool = True):
        self.logger.info(f"Установка максимальной цены: {max_price}")
        min_price_input = self._find_hidden(self.MIN_PRICE_INPUT)
        max_price_input = self._find_hidden(self.MAX_PRICE_INPUT)

        min_available = int(min_price_input.get_attribute("data-min") or "0")
        max_available = int(max_price_input.get_attribute("data-max") or "0")

        if not (min_available <= max_price <= max_available):
            raise ValueError(
                f"Цена должна быть в диапазоне "
                f"{min_available}–{max_available}, получено: {max_price}"
            )

        self.driver.execute_script(
            """
            var maxInput = document.getElementById('max_price');
            maxInput.value = arguments[0];

            var slider = jQuery(".price_slider");
            slider.slider("values", 1, arguments[0]);
            """,
            str(max_price),
        )

        if apply:
            self.wait.until(EC.element_to_be_clickable(self.APPLY_PRICE_FILTER)).click()

    def _find_hidden(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
