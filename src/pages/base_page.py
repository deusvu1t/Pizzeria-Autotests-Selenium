import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config.settings import Settings
from src.pages.components.header_component import HeaderComponent
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    URL = Settings.base_url
    HEADER = (By.CLASS_NAME, "site-header")

    def __init__(self, driver: WebDriver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @property
    def header(self) -> HeaderComponent:
        header_element = self.find(self.HEADER)
        return HeaderComponent(self.driver, header_element)

    @allure.step("Открыть страницу: {part}")
    def open(self, part=""):
        url = self.URL + part
        logger.info("Opening page | url=%s", url)
        self.driver.get(url)

    def find(self, locator: tuple[str, str]) -> WebElement:
        logger.debug("Find visible element on page | locator=%s", locator)
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: tuple[str, str]) -> list[WebElement]:
        logger.debug("Find visible elements on page | locator=%s", locator)
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple[str, str]):
        logger.info("Click page element | locator=%s", locator)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def is_visible(self, locator: tuple[str, str], timeout: int = 10) -> bool:
        logger.debug("Check page element visibility | locator=%s", locator)
        return self._is_visible(locator, timeout)

    def _is_visible(self, locator: tuple[str, str], timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
