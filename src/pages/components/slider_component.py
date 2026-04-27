import allure
from selenium.webdriver.common.by import By

from src.pages.components.base_component import BaseComponent
from src.pages.components.slide_component import SlideComponent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SliderComponent(BaseComponent):
    SLIDES = (By.CSS_SELECTOR, "li[aria-hidden='false']")
    TRACK = (By.CLASS_NAME, "slick-track")
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

    def slide_titles(self) -> list[str]:
        return [slide.title for slide in self.slides()]

    def _wait_until_animation_finished(self):
        self.wait.until(
            lambda _: (
                "slick-animating" not in self.find(self.TRACK).get_attribute("class")
            )
        )

    # def next(self):
    #     before = self.slide_titles()

    #     with allure.step("Переключить слайдер вправо"):
    #         self._wait_until_animation_finished()
    #         self.slides()[-1].hover()
    #         self.wait.until(lambda _: self.find(self.NEXT).is_displayed())
    #         self.click(self.NEXT)
    #         self.wait.until(lambda _: self.slide_titles() != before)
    #         self._wait_until_animation_finished()

    # def prev(self):
    #     before = self.slide_titles()

    #     with allure.step("Переключить слайдер влево"):
    #         self._wait_until_animation_finished()
    #         self.slides()[0].hover()
    #         self.wait.until(lambda _: self.find(self.PREV).is_displayed())
    #         self.click(self.PREV)
    #         self.wait.until(lambda _: self.slide_titles() != before)
    #         self._wait_until_animation_finished()
    def _click_via_js(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def next(self):
        self._wait_until_animation_finished()
        before = self.slide_titles()

        with allure.step("Переключить слайдер вправо"):
            # Наводим для активации кнопок
            self.slides()[-1].hover()
            # Ждем именно видимости кнопки
            self.wait.until(lambda _: self.find(self.NEXT).is_displayed())

            # Используем JS клик, чтобы анимация или потеря ховера не мешали
            self._click_via_js(self.NEXT)

            # Ждем изменения контента
            self.wait.until(lambda _: self.slide_titles() != before)
            self._wait_until_animation_finished()

    def prev(self):
        self._wait_until_animation_finished()
        before = self.slide_titles()

        with allure.step("Переключить слайдер влево"):
            # Наводим на первый видимый слайд
            self.slides()[0].hover()
            self.wait.until(lambda _: self.find(self.PREV).is_displayed())

            self._click_via_js(self.PREV)

            self.wait.until(lambda _: self.slide_titles() != before)
            self._wait_until_animation_finished()
