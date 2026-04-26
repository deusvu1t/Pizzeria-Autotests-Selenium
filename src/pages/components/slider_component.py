import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.pages.components.slide_component import SlideComponent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SliderComponent(BaseComponent):
    SLIDES = (By.CSS_SELECTOR, "li[aria-hidden='false']")
    PREV = (By.CLASS_NAME, "slick-prev")
    NEXT = (By.CLASS_NAME, "slick-next")

    def slides(self) -> list[SlideComponent]:
        logger.info("Get visible slider slides")
        with allure.step("Получить видимые слайды"):
            slides = [
                SlideComponent(self.driver, slide)
                for slide in self.find_all(self.SLIDES)
            ]
            logger.info("Visible slider slides found | count=%s", len(slides))
            allure.attach(
                str(len(slides)),
                name="visible_slides_count",
                attachment_type=allure.attachment_type.TEXT,
            )
            return slides

    def prev(self):
        logger.info("Switch slider to previous slides")
        with allure.step("Переключить слайдер влево"):
            self.slides()[0].hover()
            self.click(self.PREV)

    def next(self):
        logger.info("Switch slider to next slides")
        with allure.step("Переключить слайдер вправо"):
            self.slides()[-1].hover()
            self.click(self.NEXT)
