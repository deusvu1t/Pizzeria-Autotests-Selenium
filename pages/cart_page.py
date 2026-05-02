import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from components.cart_item import CartItem
from pages.base_page import BasePage
from utils.helpers import normalize_text, parse_price


class CartPage(BasePage):
    PATH = "/cart/"
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    UPDATE_CART = (By.CSS_SELECTOR, "button[name='update_cart']")
    CART_UPDATED_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-message")
    CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, ".cart-empty")
    CHECKOUT_BUTTON = (By.CLASS_NAME, "checkout-button")
    COUPON_INPUT = (By.NAME, "coupon_code")
    COUPON_APPLY_BUTTON = (By.NAME, "apply_coupon")
    COUPON_SUCCESS = (By.CSS_SELECTOR, ".woocommerce-message")
    COUPON_ERROR = (By.CSS_SELECTOR, ".woocommerce-error")
    CART_TOTAL = (By.CSS_SELECTOR, ".order-total .amount")
    DISCOUNT_ROW = (By.CSS_SELECTOR, ".cart-discount .amount")

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

    @allure.step("Обновить корзину")
    def update_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.UPDATE_CART)).click()
        self.find(self.CART_UPDATED_MESSAGE)

    def wait_until_item_removed(self, name: str):
        self.wait.until(lambda _: self.find_item(name, wait=False) is None)

    def is_cart_empty(self) -> bool:
        return self.is_visible(self.CART_EMPTY_MESSAGE)

    @allure.step("Перейти к оформлению заказа")
    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    @allure.step("Применить купон: {code}")
    def apply_coupon(self, code: str):
        self.input_text(self.COUPON_INPUT, code)
        self.click(self.COUPON_APPLY_BUTTON)
        self._wait_for_totals_update()

    def is_coupon_applied(self) -> bool:
        return self.is_visible(self.COUPON_SUCCESS, timeout=5)

    def is_coupon_error_shown(self) -> bool:
        return self.is_visible(self.COUPON_ERROR, timeout=5)

    def get_total_price(self) -> int:
        return parse_price(self.get_text(self.CART_TOTAL))

    def get_discount_amount(self) -> int:
        if not self.is_visible(self.DISCOUNT_ROW, timeout=3):
            return 0
        return parse_price(self.get_text(self.DISCOUNT_ROW))

    def _wait_for_totals_update(self):
        BLOCK_OVERLAY = (By.CSS_SELECTOR, ".cart_totals .blockOverlay")

        try:
            from selenium.webdriver.support.ui import WebDriverWait

            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(BLOCK_OVERLAY)
            )
        except Exception:
            pass

        self.wait.until(EC.invisibility_of_element_located(BLOCK_OVERLAY))
