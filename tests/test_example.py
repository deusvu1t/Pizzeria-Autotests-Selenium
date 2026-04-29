class TestExample:
    def test_example(self, driver):
        driver.get("https://www.google.com")
        assert "Google" in driver.title
