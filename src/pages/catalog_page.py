import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from src.pages.base_page import BasePage
from src.pages.components.slide_component import SlideComponent
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CatalogPage(BasePage):
    PRODUCTS = (By.CSS_SELECTOR, "ul.products li.product")
    MIN_PRICE = (By.ID, "min_price")
    MAX_PRICE = (By.ID, "max_price")
    FILTER_BTN = (By.CSS_SELECTOR, ".price_slider_amount button")
    SLIDER_MIN = (By.CSS_SELECTOR, ".ui-slider-handle:nth-of-type(1)")
    SLIDER_MAX = (By.CSS_SELECTOR, ".ui-slider-handle:nth-of-type(2)")

    @allure.step("Открыть каталог: {path}")
    def open(self, path: str = "product-category/menu/") -> None:
        return super().open(path)

    @allure.step("Получить список товаров на странице")
    def products(self) -> list[SlideComponent]:
        elements = self.find_all(self.PRODUCTS)
        return [SlideComponent(self.driver, el) for el in elements]

    @allure.step("Установить максимальную цену: {price}")
    def set_max_price(self, price: int):
        # We might need to manipulate the DOM or slider directly since it's a UI slider
        # Or execute script
        self.driver.execute_script(f"document.getElementById('max_price').value = '{price}';")
        self.driver.execute_script("document.body.click();") # Trigger update if necessary

        # WooCommerce slider usually triggers an update
        self.click(self.FILTER_BTN)

        # Wait for products to refresh
        self.wait.until(lambda _: "overlay" not in self.find((By.CSS_SELECTOR, "ul.products")).get_attribute("class"))
