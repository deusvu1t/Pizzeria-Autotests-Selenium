from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class MainPage(BasePage):
    PIZZA_SLIDER = (By.CSS_SELECTOR, "#product1 .product-slider .ak-container")

    def get_pizza_slider(self):
        return self.find(self.PIZZA_SLIDER)
