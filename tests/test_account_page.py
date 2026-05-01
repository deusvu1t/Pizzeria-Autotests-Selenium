from pages.account_page import AccountPage
from pages.main_page import MainPage


class TestAccountPage:
    def test_login(self, main_page: MainPage, account_page: AccountPage):
        main_page.open()
        main_page.header.go_to_login()
        account_page.set_username("test_username001")
        account_page.set_password("test123")
        account_page.login()
        assert account_page.is_authorized()
