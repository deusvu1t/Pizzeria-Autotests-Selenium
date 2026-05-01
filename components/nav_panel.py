import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from components.base_component import BaseComponent


class NavPanel(BaseComponent):
    MENU_LINK = (By.CSS_SELECTOR, "a[href*='/product-category/menu/']")
    DESSERTS_LINK = (By.CSS_SELECTOR, "a[href*='/product-category/menu/deserts/']")
    CART_ICON = (By.CSS_SELECTOR, "a.cart-contents")
    CART_TOTAL = (By.CSS_SELECTOR, ".amount")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='my-account']")

    @property
    def cart_total(self) -> str:
        return self.get_text(self.CART_TOTAL)

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        self.click(self.CART_ICON)

    @allure.step("Перейти в аккаунт")
    def go_to_account(self):
        self.click(self.LOGIN_LINK)

    @allure.step("Перейти в раздел «Десерты»")
    def go_to_desserts(self):
        menu_link = self.find(self.MENU_LINK)
        self.hover(menu_link)
        self.wait.until(EC.visibility_of_element_located(self.DESSERTS_LINK))
        self.click(self.DESSERTS_LINK)
