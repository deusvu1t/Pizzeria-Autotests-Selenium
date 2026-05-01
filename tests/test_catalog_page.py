import allure

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.main_page import MainPage
from utils.helpers import normalize_text, parse_price


@allure.feature("Каталог")
class TestCatalogPage:
    @allure.story("Фильтр по цене")
    def test_price_filter_applies_correctly(
        self, main_page: MainPage, catalog_page: CatalogPage
    ):
        with allure.step("Открыть страницу десертов"):
            main_page.open()
            catalog_page.header.go_to_deserts()

        with allure.step("Получить список товаров до фильтрации"):
            initial_products = catalog_page.get_products()
            initial_data = [(p.name, p.price) for p in initial_products]

        with allure.step("Установить максимальную цену 135"):
            catalog_page.set_max_price_filter(135)

        with allure.step("Получить список товаров после фильтрации"):
            filtered_products = catalog_page.get_products()
            filtered_data = [(p.name, p.price) for p in filtered_products]

        with allure.step("Проверить, что список изменился"):
            assert filtered_data != initial_data, "Список товаров не изменился"

        with allure.step("Проверить, что все цены <= 135"):
            for name, price in filtered_data:
                numeric_price = parse_price(price)
                assert numeric_price <= 135, (
                    f"Товар '{name}' имеет цену {numeric_price} > 135"
                )

    @allure.feature("Каталог")
    @allure.story("Добавление товара в корзину")
    @allure.title("Десерт из каталога добавляется в корзину с корректными данными")
    def test_add_dessert_to_cart(
        self, main_page: MainPage, catalog_page: CatalogPage, cart_page: CartPage
    ):
        with allure.step("Открыть страницу и перейти в раздел десертов"):
            main_page.open()
            main_page.header.go_to_deserts()

        with allure.step("Получить список десертов"):
            products = catalog_page.get_products()
            assert products, "Список десертов пуст"

        with allure.step("Выбрать первый десерт"):
            product = products[0]
            product_name = product.name
            product_price = product.price

        with allure.step(f"Добавить десерт '{product_name}' в корзину"):
            product.add_to_cart()

        with allure.step("Перейти в корзину"):
            catalog_page.header.go_to_cart()

        with allure.step("Найти добавленный десерт в корзине"):
            item = cart_page.find_item(product_name)
            assert item is not None, f"Десерт '{product_name}' не найден в корзине"

        with allure.step("Проверить название"):
            assert normalize_text(item.name) == normalize_text(product_name), (
                f"Название: ожидалось '{product_name}', получено '{item.name}'"
            )

        with allure.step("Проверить цену"):
            assert normalize_text(item.price) == normalize_text(product_price), (
                f"Цена: ожидалась '{product_price}', получена '{item.price}'"
            )
