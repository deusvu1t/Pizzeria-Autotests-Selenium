with open("tests/test_cart_page.py", "r") as f:
    content = f.read()

content = content.replace("time.sleep(2) cart_page.wait.until", "time.sleep(2); cart_page.wait.until")
with open("tests/test_cart_page.py", "w") as f:
    f.write(content)

with open("tests/test_checkout_page.py", "r") as f:
    content = f.read()

content = content.replace("            assert math.isclose(checkout_page.order_total, cart_total, abs_tol=0.1)", "            assert math.isclose(checkout_page.order_total, cart_total, abs_tol=0.1)")

# wait, unexpected indent? Let's check lines 40-50
lines = content.split('\n')
for i, line in enumerate(lines[35:50]):
    print(f"{i+35}: {repr(line)}")
