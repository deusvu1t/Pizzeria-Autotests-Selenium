import allure
import time
from src.pages.account_page import AccountPage
import random

@allure.feature("Личный кабинет")
class TestAccountPage:
    @allure.story("Регистрация")
    @allure.title("Регистрация нового пользователя через вкладку «Мой аккаунт»")
    def test_register_new_user(self, account_page: AccountPage):
        with allure.step("1. Открыть вкладку 'Мой аккаунт'"):
            account_page.open()
        with allure.step("2. Нажать кнопку 'Зарегистрироваться'"):
            account_page.click_custom_register()
        with allure.step("3. Ввести уникальный логин, email, пароль"):
            uid = random.randint(10000, 99999)
            username = f"usr{uid}"
            email = f"usr{uid}@test.ru"
            password = "StrongPassword123!"
        with allure.step("4. Подтвердить регистрацию"):
            account_page.register(username, email, password)
        with allure.step("Ожидаемый результат: Регистрация успешна, ошибок нет"):
            assert account_page.is_logged_in()

    @allure.story("Авторизация")
    @allure.title("Проверка авторизации после регистрации")
    def test_auth_status_after_registration(self, account_page: AccountPage):
        with allure.step("Подготовка: регистрация нового пользователя."):
            account_page.open()
            account_page.click_custom_register()
            uid = random.randint(10000, 99999)
            username = f"usr{uid}"
            email = f"usr{uid}@test.ru"
            password = "StrongPassword123!"
            account_page.register(username, email, password)
            assert account_page.is_logged_in()
        with allure.step("1. Открыть вкладку 'Мой аккаунт'"):
            account_page.open()
        with allure.step("Ожидаемый результат: Пользователь авторизован"):
            assert account_page.is_logged_in()
