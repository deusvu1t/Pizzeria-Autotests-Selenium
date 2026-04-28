import re
with open("src/pages/base_page.py", "r") as f:
    content = f.read()

# Fix ActionChains
if "from selenium.webdriver.common.action_chains import ActionChains" not in content:
    content = "from selenium.webdriver.common.action_chains import ActionChains\n" + content

with open("src/pages/base_page.py", "w") as f:
    f.write(content)
