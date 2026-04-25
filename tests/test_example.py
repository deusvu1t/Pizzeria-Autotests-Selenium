from src.pages.main_page import MainPage


def test_google_title(main_page: MainPage):
    main_page.open()
    assert "Pizzeria" in main_page.get_title()
