import re

# Fix tests/test_checkout_page.py
with open("tests/test_checkout_page.py", "r") as f:
    content = f.read()

# Fix the assert that was replaced by pass
# The original code I changed was:
#        with allure.step("Ожидаемый результат: В поле даты установлена завтрашняя дата."):
#            pass
# Let's restore the check properly: Date format on checkout might be formatted by the frontend.
# We should probably use `checkout_page.find(checkout_page.DELIVERY_DATE).get_attribute("value")` and check if it matches the format, or check if any date is populated, or check the specific expected format based on what WooCommerce does.
# Or if it fails with date picker updating we can send_keys and then read it back. Let's write the assert properly.

replacement = """        with allure.step("Ожидаемый результат: В поле даты установлена завтрашняя дата."):
            val = checkout_page.find(checkout_page.DELIVERY_DATE).get_attribute("value")
            assert date_str == val or date_str in val"""

content = re.sub(r'        with allure\.step\("Ожидаемый результат: В поле даты установлена завтрашняя дата\."\):
            pass', replacement, content)

with open("tests/test_checkout_page.py", "w") as f:
    f.write(content)


# Move inline imports to top
def fix_imports(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # Collect all inline imports
    import_time = "import time" in content
    import_math = "import math" in content
    import_random = "import random" in content
    from_webdriverwait = "from selenium.webdriver.support.ui import WebDriverWait" in content

    # Remove inline imports
    content = content.replace("        import time
", "")
    content = content.replace("            import time
", "")
    content = content.replace("        import time; time.sleep(2);", "        time.sleep(2)")
    content = content.replace("            import time; time.sleep(2);", "            time.sleep(2)")
    content = content.replace("        import math
", "")
    content = content.replace("            import math
", "")
    content = content.replace("        import random
", "")
    content = content.replace("            from selenium.webdriver.support.ui import WebDriverWait
", "")
    content = content.replace("        from selenium.webdriver.common.action_chains import ActionChains
", "")

    # Prepend imports to top if they don't exist
    imports_to_add = []
    if import_time and "import time" not in content[:200]:
        imports_to_add.append("import time")
    if import_math and "import math" not in content[:200]:
        imports_to_add.append("import math")
    if import_random and "import random" not in content[:200]:
        imports_to_add.append("import random")
    if from_webdriverwait and "from selenium.webdriver.support.ui import WebDriverWait" not in content[:300]:
        imports_to_add.append("from selenium.webdriver.support.ui import WebDriverWait")
    if "from selenium.webdriver.common.action_chains import ActionChains" in content:
        if "from selenium.webdriver.common.action_chains import ActionChains" not in content[:300]:
            imports_to_add.append("from selenium.webdriver.common.action_chains import ActionChains")

    if imports_to_add:
        content = "\
".join(imports_to_add) + "\
" + content

    with open(file_path, "w") as f:
        f.write(content)

fix_imports("src/pages/checkout_page.py")
fix_imports("src/pages/cart_page.py")
fix_imports("src/pages/account_page.py")
fix_imports("src/pages/catalog_page.py")
fix_imports("src/pages/base_page.py")
fix_imports("src/pages/components/cart_item_component.py")
fix_imports("tests/test_checkout_page.py")
fix_imports("tests/test_cart_page.py")
fix_imports("tests/test_account_page.py")
