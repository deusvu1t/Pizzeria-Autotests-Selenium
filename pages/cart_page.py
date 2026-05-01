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
    CHECKOUT_BUTTON = (By.CLASS_NAME, "checkout-button")

    def get_cart_items(self, wait: bool = True) -> list[CartItem]:
        if wait:
            elements = self.find_all(self.CART_ITEM)
        else:
            elements = [
                el
                for el in self.driver.find_elements(*self.CART_ITEM)
                if el.is_displayed()
            ]
        return [CartItem(el, self) for el in elements]

    def find_item(
        self, name: str, variation: str | None = None, wait: bool = True
    ) -> CartItem | None:
        for item in self.get_cart_items(wait=wait):
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
        self.wait.until(lambda _: self.find_item(name, wait=False) is None)

    def is_cart_empty(self) -> bool:
        return self.is_visible(self.CART_EMPTY_MESSAGE)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
