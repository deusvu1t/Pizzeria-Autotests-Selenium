from selenium.webdriver.common.by import By

from src.core.ui.base_page import BasePage


class MainPage(BasePage):
    PIZZA_SLIDER = (By.CSS_SELECTOR, "#product1 .product-slider .ak-container")
