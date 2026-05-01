# import allure

# from pages.account_page import AccountPage
# from pages.main_page import MainPage
# from pages.register_page import RegisterPage


# @allure.feature("Аккаунт")
# class TestRegisterPage:
#     @allure.story("Регистрация")
#     @allure.title("Новый пользователь успешно регистрируется на сайте")
#     def test_register(
#         self,
#         opened_main_page: MainPage,
#         account_page: AccountPage,
#         register_page: RegisterPage,
#     ):
#         with allure.step("Перейти в аккаунт через навигацию"):
#             opened_main_page.header.go_to_account()

#         with allure.step("Нажать кнопку «Зарегистрироваться»"):
#             account_page.go_to_register()

#         with allure.step("Заполнить форму регистрации"):
#             register_page.set_name("test_username001")
#             register_page.set_email("test_001@mail.test")
#             register_page.set_password("test123")

#         with allure.step("Отправить форму регистрации"):
#             register_page.register()

#         with allure.step("Проверить, что регистрация прошла успешно"):
#             assert register_page.is_registered(), (
#                 "Регистрация не прошла: сообщение об успехе не найдено"
#             )
