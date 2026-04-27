from src.pages.product_page import ProductPage


class TestProductPage:
    def test_can_select_product_extra_option(self, product_page: ProductPage):
        product_page.open("пицца-4-в-1")

        product_page.board_pack("Сырный")
        assert product_page.active_board_pack_value == "55.00"

        product_page.board_pack("Колбасный")
        assert product_page.active_board_pack_value == "65.00"

        product_page.board_pack("Обычный")
        assert product_page.active_board_pack_value == ""
