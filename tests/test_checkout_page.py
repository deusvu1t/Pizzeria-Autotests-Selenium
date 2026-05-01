# from pages.cart_page import CartPage
# from pages.checkout_page import CheckoutPage
# from pages.main_page import MainPage


# class TestCheckoutPage:
#     def test_requires_login_when_proceeding_to_checkout(
#         self, main_page: MainPage, cart_page: CartPage, checkout_page: CheckoutPage
#     ):
#         main_page.open()
#         main_page.pizza_slider.get_slide(1).add_to_cart()
#         main_page.header.go_to_cart()
#         cart_page.checkout()
#         assert checkout_page.is_login_requires()
