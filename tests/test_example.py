from selenium.webdriver.remote.webdriver import WebDriver


def test_example(driver: WebDriver):
    driver.get("https://www.google.com/")
    assert "Google" in driver.title
