from src.pages.cart_page import CartPage
from src.pages.main_page import MainPage


def test_example(main_page: MainPage, cart_page: CartPage):
    main_page.open()
    slider = main_page.get_pizza_slider()
    pass
