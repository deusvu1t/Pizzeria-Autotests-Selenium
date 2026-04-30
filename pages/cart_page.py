from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from components.cart_item import CartItem
from pages.base_page import BasePage
from utils.helpers import normalize_text


class CartPage(BasePage):
    PATH = "/cart/"
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    UPDATE_CART = (By.CSS_SELECTOR, "button[name='update_cart']")
    CART_UPDATED_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-message")
    CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, ".cart-empty")

    def get_cart_items(self) -> list[CartItem]:
        return [CartItem(el, self) for el in self.find_all(self.CART_ITEM)]

    def find_item(
        self, name: str, variation: str | None = None
    ) -> CartItem | None:
        items = self.get_cart_items()
        return self._find_item_in_items(items, name, variation)

    def find_item_optional(
        self, name: str, variation: str | None = None
    ) -> CartItem | None:
        elements = self.driver.find_elements(*self.CART_ITEM)
        items = [CartItem(el, self) for el in elements if el.is_displayed()]
        return self._find_item_in_items(items, name, variation)

    def _find_item_in_items(
        self,
        items: list[CartItem],
        name: str,
        variation: str | None = None,
    ) -> CartItem | None:
        for item in items:
            name_match = normalize_text(item.name) == normalize_text(name)
            variation_match = variation is None or (
                item.variation is not None
                and normalize_text(variation) in normalize_text(item.variation)
            )
            if name_match and variation_match:
                return item
        return None

    def update_cart(self):
        self.logger.info("Обновление корзины")
        self.wait.until(EC.element_to_be_clickable(self.UPDATE_CART)).click()
        self.find(self.CART_UPDATED_MESSAGE)

    def wait_until_item_removed(self, name: str):
        self.wait.until(lambda _: self.find_item_optional(name) is None)
