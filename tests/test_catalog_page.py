import allure

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.main_page import MainPage
from utils.helpers import normalize_text, parse_price


@allure.feature("Каталог")
class TestCatalogPage:
    @allure.story("Фильтр по цене")
    @allure.title("Фильтр по максимальной цене применяется корректно")
    def test_price_filter_applies_correctly(
        self, opened_main_page: MainPage, catalog_page: CatalogPage
    ):
        with allure.step("Перейти в раздел «Десерты»"):
            # go_to_desserts доступен на любой странице через header
            opened_main_page.header.go_to_desserts()

        with allure.step("Запомнить список товаров до фильтрации"):
            initial_data = [(p.name, p.price) for p in catalog_page.get_products()]

        with allure.step("Установить максимальную цену 135 ₽"):
            catalog_page.set_max_price_filter(135)

        with allure.step("Получить список товаров после фильтрации"):
            filtered_products = catalog_page.get_products()

        with allure.step("Проверить, что список товаров изменился"):
            filtered_data = [(p.name, p.price) for p in filtered_products]
            assert filtered_data != initial_data, "Список товаров не изменился"

        with allure.step("Проверить, что все цены не превышают 135 ₽"):
            for product in filtered_products:
                price = parse_price(product.price)
                assert price <= 135, (
                    f"Товар '{product.name}' имеет цену {price} ₽ > 135 ₽"
                )

    @allure.story("Добавление товара в корзину")
    @allure.title("Десерт из каталога добавляется в корзину с корректными данными")
    def test_add_dessert_to_cart(
        self,
        opened_main_page: MainPage,
        catalog_page: CatalogPage,
        cart_page: CartPage,
    ):
        with allure.step("Перейти в раздел «Десерты»"):
            opened_main_page.header.go_to_desserts()

        with allure.step("Проверить, что каталог не пуст"):
            products = catalog_page.get_products()
            assert products, "Список десертов пуст"

        with allure.step("Запомнить данные первого десерта"):
            product = products[0]
            product_name = product.name
            product_price = product.price

        with allure.step(f"Добавить десерт '{product_name}' в корзину"):
            product.add_to_cart()

        with allure.step("Перейти в корзину"):
            catalog_page.header.go_to_cart()

        with allure.step(f"Проверить '{product_name}' в корзине"):
            item = cart_page.find_item(product_name)
            assert item is not None, f"Десерт '{product_name}' не найден в корзине"
            assert normalize_text(item.name) == normalize_text(product_name), (
                f"Название: ожидалось '{product_name}', получено '{item.name}'"
            )
            assert normalize_text(item.price) == normalize_text(product_price), (
                f"Цена: ожидалась '{product_price}', получена '{item.price}'"
            )
