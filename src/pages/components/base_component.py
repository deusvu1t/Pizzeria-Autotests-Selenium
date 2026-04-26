import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseComponent:
    def __init__(self, driver, root, timeout=10):
        self.driver = driver
        self.root = root
        self.wait = WebDriverWait(driver, timeout)

    def _find_raw(self, locator):
        return self.root.find_element(*locator)

    def _find_all_raw(self, locator):
        return self.root.find_elements(*locator)

    def find(self, locator):
        logger.debug("Find element inside component | locator=%s", locator)
        with allure.step(f"Найти элемент внутри компонента: {locator}"):
            return self.wait.until(lambda _: self._find_raw(locator))

    def find_all(self, locator):
        logger.debug("Find elements inside component | locator=%s", locator)
        with allure.step(f"Найти элементы внутри компонента: {locator}"):
            return self.wait.until(lambda _: self._find_all_raw(locator))

    def click(self, locator: tuple[str, str]):
        logger.info("Click component element | locator=%s", locator)
        with allure.step(f"Кликнуть по элементу внутри компонента: {locator}"):
            element = self.wait.until(lambda _: self._find_raw(locator))
            self.wait.until(EC.element_to_be_clickable(element)).click()

    def hover(self):
        logger.info("Hover component | %s", self.__class__.__name__)
        with allure.step(f"Навести курсор на компонент: {self.__class__.__name__}"):
            self.wait.until(lambda _: self.root.is_displayed())
            ActionChains(self.driver).move_to_element(self.root).perform()

    def is_displayed(self, timeout: int = 10) -> bool:
        logger.debug("Check component visibility | %s", self.__class__.__name__)
        with allure.step(f"Проверить видимость компонента: {self.__class__.__name__}"):
            return self._is_displayed(timeout)

    def _is_displayed(self, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda _: self.root.is_displayed()
            )
            return True
        except TimeoutException:
            return False

    def is_visible(self, locator: tuple[str, str], timeout: int = 10) -> bool:
        logger.debug("Check component element visibility | locator=%s", locator)
        with allure.step(f"Проверить видимость элемента внутри компонента: {locator}"):
            return self._is_visible(locator, timeout)

    def _is_visible(self, locator: tuple[str, str], timeout: int = 10) -> bool:
        try:
            self.wait.until(lambda _: self.find(locator).is_displayed())
            return True
        except TimeoutException:
            return False
