from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage
from src.pages.components.slider_component import SliderComponent


class MainPage(BasePage):
    PIZZA_SLIDER = (By.ID, "product1")


    def pizza_slider(self) -> SliderComponent:
        return SliderComponent(self.driver, self.find(self.PIZZA_SLIDER))
