import allure
import math
from src.pages.main_page import MainPage
from src.pages.catalog_page import CatalogPage
from src.pages.cart_page import CartPage

@allure.feature("Страница каталога")
class TestCatalogPage:
    @allure.story("Навигация")
    @allure.title("Переход в раздел десертов через меню")
    def test_navigate_to_desserts_via_menu(self, main_page: MainPage, catalog_page: CatalogPage):
        with allure.step("1. Находясь не на главной странице, открыть вкладку Меню -> Десерты."):
            main_page.open("cart/")
            main_page.hover_menu()
            main_page.click_submenu("Десерты")
        with allure.step("Ожидаемый результат: Открыт раздел Десерты."):
            main_page.wait.until(lambda _: "deserts" in main_page.driver.current_url)
            assert "deserts" in main_page.driver.current_url

    @allure.story("Фильтрация")
    @allure.title("Фильтрация десертов по бюджету 135 рублей")
    def test_filter_desserts_by_price(self, catalog_page: CatalogPage):
        with allure.step("1. Открыть раздел Десерты."):
            catalog_page.open("product-category/menu/deserts/")
        with allure.step("2. Применить ограничение цены до 135 рублей."):
            catalog_page.set_max_price(135)
        with allure.step("Ожидаемый результат: В списке отображаются десерты не дороже 135 рублей."):
            products = catalog_page.products()
            assert len(products) > 0
            for p in products:
                assert p.price <= 135.0

    @allure.story("Покупка")
    @allure.title("Добавление десерта в корзину после фильтрации")
    def test_add_filtered_dessert_to_cart(self, catalog_page: CatalogPage, cart_page: CartPage):
        with allure.step("1. Открыть раздел Десерты, отфильтровать до 135."):
            catalog_page.open("product-category/menu/deserts/")
            catalog_page.set_max_price(135)
        with allure.step("2. Выбрать десерт и добавить в корзину."):
            products = catalog_page.products()
            assert len(products) > 0
            target = products[0]
            target_name = target.title
            target.add_to_cart()
        with allure.step("3. Открыть корзину."):
            cart_page.open()
        with allure.step("Ожидаемый результат: Выбранный десерт в корзине, цена не превышает 135."):
            items = cart_page.items()
            assert len(items) >= 1
            found = False
            for item in items:
                if target_name.lower() in item.name.lower():
                    found = True
                    assert item.price <= 135.0
                    break
            assert found, f"{target_name} not found in cart items"
