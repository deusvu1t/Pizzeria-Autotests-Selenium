from src.pages.main_page import MainPage


class TestMainPage:
    def test_is_pizza_slider_visible(self, main_page: MainPage):
        main_page.open()
        assert main_page.title == "Pizzeria — Пиццерия"
        slider = main_page.pizza_slider()
        assert slider.is_displayed()
        slides = slider.slides()
        assert len(slides) == 4
        for slide in slides:
            assert slide.is_displayed()
            assert slide.title is not None or not ""
            assert slide.price is not None or not ""
