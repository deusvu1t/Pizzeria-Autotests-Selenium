import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage
from src.pages.components.cart_item_component import CartItemComponent
from src.utils.helpers import parse_price
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_SUBTOTAL = (By.CSS_SELECTOR, ".cart-subtotal bdi")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".order-total bdi")
    UPDATE_CART_BTN = (By.NAME, "update_cart")
    CHECKOUT_BTN = (By.CLASS_NAME, "checkout-button")

    @allure.step("Открыть страницу корзины")
    def open(self, path: str = "cart/") -> None:
        return super().open(path)

    @allure.step("Получить список товаров в корзине")
    def items(self) -> list[CartItemComponent]:
        # Если корзина пуста, find_all может упасть, поэтому лучше обрабатывать это тихо
        try:
            elements = self.find_all(self.CART_ITEM)
            return [CartItemComponent(self.driver, el) for el in elements]
        except Exception:
            logger.info("Cart is empty")
            return []

    @property
    def order_total(self) -> float:
        text = self.find(self.ORDER_TOTAL).text
        return parse_price(text)

    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BTN)
