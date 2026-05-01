from pages.account_page import AccountPage
from pages.main_page import MainPage
from tests.register_page import RegisterPage


class TestRegisterPage:
    def test_register(
        self,
        main_page: MainPage,
        account_page: AccountPage,
        register_page: RegisterPage,
    ):
        main_page.open()
        main_page.header.go_to_login()
        account_page.register()
        register_page.set_name("test_username001")
        register_page.set_email("test_001@mail.test")
        register_page.set_password("test123")
        register_page.register()
        assert register_page.is_registered()
