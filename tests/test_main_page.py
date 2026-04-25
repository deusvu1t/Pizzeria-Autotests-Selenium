import allure

from src.pages.main_page import MainPage


@allure.feature("Главная страница")
class TestMainPage:
    @allure.story("Слайдер с пиццами")
    @allure.title("На главной странице отображается слайдер с пиццами")
    def test_pizza_slider_is_visible(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        with allure.step("Проверить видимость слайдера с пиццами"):
            slider = main_page.pizza_slider()
            assert slider.is_displayed()

    @allure.story("Слайдер с пиццами")
    @allure.title("У каждого слайда есть название и цена")
    def test_pizza_slide_has_title_and_price(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        slides = main_page.pizza_slider().slides()

        with allure.step("Проверить отображение названия и цены у каждого слайда"):
            for slide in slides:
                assert slide.title is not None or not ""
                assert slide.price is not None or not ""

    @allure.story("Слайдер с пиццами")
    @allure.title("На каждом слайде отображается кнопка 'В корзину'")
    def test_add_to_cart_btn_is_visible(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        slides = main_page.pizza_slider().slides()

        with allure.step("Проверить отображение кнопки 'В корзину' на каждом слайде'"):
            for slide in slides:
                assert slide.is_add_to_cart_button_visible()
