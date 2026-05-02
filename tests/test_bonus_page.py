import allure
import pytest

from pages.bonus_page import BonusPage

VALID_NAME = "Андрей"
VALID_PHONE = "79001234567"


@allure.feature("Бонусная программа")
class TestBonusPage:
    @allure.story("Оформление бонусной карты")
    @allure.title("Бонусная карта успешно оформляется при вводе корректных данных")
    def test_bonus_card_registration_success(self, opened_bonus_page: BonusPage):
        with allure.step(
            f"Заполнить форму: имя «{VALID_NAME}», телефон «{VALID_PHONE}»"
        ):
            alert_text = opened_bonus_page.register_bonus_card(VALID_NAME, VALID_PHONE)

        with allure.step("Проверить текст alert — заявка отправлена"):
            assert "заявка отправлена" in alert_text.lower(), (
                f"Неожиданный текст alert: «{alert_text}»"
            )

        with allure.step("Проверить, что страница показывает «Ваша карта оформлена!»"):
            assert opened_bonus_page.is_success(), (
                "Сообщение «Ваша карта оформлена!» не появилось после подтверждения"
            )

    @allure.story("Валидация формы")
    @allure.title("При отправке пустой формы отображаются ошибки для обоих полей")
    def test_empty_fields_show_validation_errors(self, opened_bonus_page: BonusPage):
        with allure.step("Отправить форму без заполнения полей"):
            opened_bonus_page.submit()

        with allure.step("Проверить наличие ошибок для обоих полей"):
            validation_text = opened_bonus_page.get_validation_text()
            assert 'Поле "Имя" обязательно для заполнения' in validation_text, (
                f"Ошибка для поля «Имя» не найдена. Текст блока: «{validation_text}»"
            )
            assert 'Поле "Телефон" обязательно для заполнения' in validation_text, (
                f"Ошибка для поля «Телефон» не найдена. Текст блока: «{validation_text}»"
            )

    @allure.story("Валидация формы")
    @allure.title("При пустом поле «Имя» отображается соответствующая ошибка")
    def test_empty_name_shows_validation_error(self, opened_bonus_page: BonusPage):
        with allure.step(
            f"Заполнить только телефон «{VALID_PHONE}», имя оставить пустым"
        ):
            opened_bonus_page.set_phone(VALID_PHONE)
            opened_bonus_page.submit()

        with allure.step("Проверить ошибку для поля «Имя»"):
            validation_text = opened_bonus_page.get_validation_text()
            assert 'Поле "Имя" обязательно для заполнения' in validation_text, (
                f"Ошибка для поля «Имя» не найдена. Текст блока: «{validation_text}»"
            )

        with allure.step("Убедиться, что ошибка телефона не показывается"):
            assert 'Поле "Телефон" обязательно для заполнения' not in validation_text, (
                "Неожиданно показана ошибка для поля «Телефон»"
            )

    @allure.story("Валидация формы")
    @allure.title("При пустом поле «Телефон» отображается соответствующая ошибка")
    def test_empty_phone_shows_validation_error(self, opened_bonus_page: BonusPage):
        with allure.step(
            f"Заполнить только имя «{VALID_NAME}», телефон оставить пустым"
        ):
            opened_bonus_page.set_name(VALID_NAME)
            opened_bonus_page.submit()

        with allure.step("Проверить ошибку для поля «Телефон»"):
            validation_text = opened_bonus_page.get_validation_text()
            assert 'Поле "Телефон" обязательно для заполнения' in validation_text, (
                f"Ошибка для поля «Телефон» не найдена. Текст блока: «{validation_text}»"
            )

        with allure.step("Убедиться, что ошибка имени не показывается"):
            assert 'Поле "Имя" обязательно для заполнения' not in validation_text, (
                "Неожиданно показана ошибка для поля «Имя»"
            )

    @allure.story("Валидация формы")
    @allure.title("При вводе телефона в неверном формате отображается ошибка формата")
    @pytest.mark.parametrize(
        "invalid_phone",
        [
            "77777",
            "abc",
            "+7900123456",
        ],
    )
    def test_invalid_phone_format_shows_error(
        self, opened_bonus_page: BonusPage, invalid_phone: str
    ):
        with allure.step(f"Ввести имя «{VALID_NAME}» и телефон «{invalid_phone}»"):
            opened_bonus_page.set_name(VALID_NAME)
            opened_bonus_page.set_phone(invalid_phone)
            opened_bonus_page.submit()

        with allure.step("Проверить ошибку формата телефона"):
            validation_text = opened_bonus_page.get_validation_text()
            assert "неверный формат телефона" in validation_text.lower(), (
                f"Ошибка формата телефона не найдена для «{invalid_phone}». "
                f"Текст блока: «{validation_text}»"
            )
