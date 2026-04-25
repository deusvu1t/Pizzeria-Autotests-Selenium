from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout=Settings.timeout)

    def open(self, path: str = "") -> None:
        url = f"{Settings.base_url}{path}"
        logger.info("Opening page | url=%s", url)
        self._driver.get(url)
