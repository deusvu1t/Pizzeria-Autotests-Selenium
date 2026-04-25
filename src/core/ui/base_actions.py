from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseActions:
    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(driver, Settings.timeout)

    def find(self, locator: tuple) -> WebElement:
        logger.debug("Find element | locator=%s", locator)
        return self._wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: tuple) -> list[WebElement]:
        logger.debug("Find elements | locator=%s", locator)
        return self._wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple) -> None:
        logger.debug("Click | locator=%s", locator)
        element = self.find(locator)
        element.click()

    def type_text(self, locator: tuple, text: str) -> None:
        logger.debug("Type text | locator=%s | text=<hidden>", locator)
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        text = self.find(locator).text
        logger.debug("Get text | locator=%s | text=%s", locator, text)
        return text

    def hover(self, locator: tuple) -> None:
        element = self.find(locator)
        ActionChains(self._driver).move_to_element(element).perform()
