with open("tests/test_checkout_page.py", "r") as f:
    content = f.read()

content = content.replace('                assert math.isclose(checkout_page.order_total, cart_total, abs_tol=0.1)', '            assert math.isclose(checkout_page.order_total, cart_total, abs_tol=0.1)')

with open("tests/test_checkout_page.py", "w") as f:
    f.write(content)
