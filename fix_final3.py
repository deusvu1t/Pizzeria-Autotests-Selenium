import re
with open("tests/test_catalog_page.py", "r") as f:
    content = f.read()

# Revert my revert of deserty -> deserts in test_catalog_page
content = content.replace('            main_page.wait.until(lambda _: "deserty" in main_page.driver.current_url)\n            assert "deserty" in main_page.driver.current_url', '            main_page.wait.until(lambda _: "deserts" in main_page.driver.current_url)\n            assert "deserts" in main_page.driver.current_url')

with open("tests/test_catalog_page.py", "w") as f:
    f.write(content)
