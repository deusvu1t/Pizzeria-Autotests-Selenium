import allure

from pages.account_page import AccountPage
from pages.main_page import MainPage


@allure.feature("Аккаунт")
class TestAccountPage:
    @allure.story("Авторизация")
    @allure.title("Пользователь успешно входит в аккаунт")
    def test_login(self, opened_main_page: MainPage, account_page: AccountPage):
        with allure.step("Перейти в аккаунт через навигацию"):
            opened_main_page.header.go_to_account()

        with allure.step("Войти под тестовым пользователем"):
            account_page.login("test_username001", "test123")

        with allure.step("Проверить, что пользователь авторизован"):
            assert account_page.is_authorized(), (
                "Пользователь не авторизован после входа"
            )
