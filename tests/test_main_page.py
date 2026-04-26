import allure

from src.pages.main_page import MainPage


@allure.feature("Главная страница")
class TestMainPage:
    EXPECTED_VISIBLE_SLIDES_COUNT = 4

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
                assert slide.name
                assert slide.price > 0

    @allure.story("Слайдер с пиццами")
    @allure.title("На каждом слайде отображается кнопка 'В корзину'")
    def test_add_to_cart_btn_is_visible(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        slides = main_page.pizza_slider().slides()

        with allure.step("Проверить отображение кнопки 'В корзину' на каждом слайде"):
            for slide in slides:
                assert slide.is_add_to_cart_button_visible()

    @allure.story("Слайдер с пиццами")
    @allure.title("Добавление одной пиццы из слайдера в корзину")
    def test_can_add_one_pizza_from_slider_to_cart(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        pizza = main_page.pizza_slider().slides()[0]
        pizza_price = pizza.price

        with allure.step("Добавить пиццу в корзину"):
            pizza.add_to_cart()

        with allure.step("Сравнить цену товаров в корзине с ценой пиццы"):
            assert main_page.header.cart_total == pizza_price

    @allure.story("Слайдер с пиццами")
    @allure.title("Добавление нескольких пицц из слайдера в корзину")
    def test_can_add_several_pizzas_from_slider_to_cart(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        total = 0

        slides = main_page.pizza_slider().slides()

        for slide in slides:
            total += slide.price
            slide.add_to_cart()

        with allure.step("Проверить сумму корзины"):
            assert main_page.header.cart_total == total

    @allure.story("Слайдер с пиццами")
    @allure.title("Слайдер переключается вправо и влево")
    def test_can_switch_pizza_slider(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        slider = main_page.pizza_slider()
        first_names = slider.slide_names()

        with allure.step("Переключить слайдер вправо"):
            slider.next()
            second_names = slider.slide_names()
            assert first_names != second_names

        with allure.step("Переключить слайдер влево"):
            slider.prev()
            third_names = slider.slide_names()
            assert second_names != third_names

    @allure.story("Слайдер с пиццами")
    @allure.title("Можно добавить пиццу после переключения слайдера")
    def test_can_add_pizza_after_slider_switch(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        slider = main_page.pizza_slider()
        slider.next()
        pizza = slider.slides()[-1]
        pizza_price = pizza.price

        with allure.step("Добавить пиццу после переключения слайдера"):
            pizza.add_to_cart()

        with allure.step("Проверить сумму корзины"):
            assert main_page.header.cart_total == pizza_price

    @allure.story("Слайдер с пиццами")
    @allure.title("Можно открыть страницу подробностей выбранной пиццы")
    def test_can_open_pizza_details_page(self, main_page: MainPage):
        with allure.step("Открыть главную страницу"):
            main_page.open()

        slider = main_page.pizza_slider()
        slides = slider.slides()
        assert len(slides) == self.EXPECTED_VISIBLE_SLIDES_COUNT
        slide = slides[-1]
        pizza_name = slide.name

        slide.go_to_details_page()

        with allure.step("Проверить, что открылась страница выбранной пиццы"):
            assert pizza_name in main_page.title.lower()

    def test_test(self, main_page: MainPage):
        main_page.open()
        slider = main_page.pizza_slider()
        slider.next()
        slider.prev()
        pass
