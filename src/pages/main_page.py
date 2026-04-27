import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage
from src.pages.components.slider_component import SliderComponent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MainPage(BasePage):
    PIZZA_SLIDER = (By.ID, "product1")

    @allure.step("Получить слайдер с пиццами")
    def pizza_slider(self) -> SliderComponent:
        return SliderComponent(self.driver, self.find(self.PIZZA_SLIDER))
