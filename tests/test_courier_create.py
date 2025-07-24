import allure
import pytest

from helpers.generator import generate_random_string
from api.courier_api import CourierApi
from data.data import (
    TEXT_LOGIN_ALREADY_EXISTS, TEXT_NOT_ENOUGH_DATA
    )


@allure.epic("Регистрация курьера")
class TestCourierCreate:
    """
    Тесты для регистрации курьера через API.
    Args:
        courier_api (CourierApi): API клиент.
    """

    @allure.title("Успешное создание курьера")
    def test_create_courier_successfully(self, courier_with_cleanup):
        """
        Проверяет, что курьер успешно создаётся при корректных данных.
        После теста курьер удаляется.
        Args:
            register_and_cleanup_courier : Фикстура: регистрирует нового курьера и удаляет его после теста.
        """
        register_response = courier_with_cleanup['register_response']
        
        assert register_response.status_code == 201
        assert register_response.json() == {"ok":True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier_with_cleanup):
        """
        Проверяет, что нельзя создать курьера с тем же логином.
        После теста курьер удаляется.
        Args:
            courier_api (CourierApi): API клиент.
        """
        courier_api = CourierApi()

        # first
        login =  courier_with_cleanup['login']
        password = courier_with_cleanup['password']
        first_name = courier_with_cleanup['first_name']

        # Если второй создастся и баг с дублем логина пройдет, то курьер тоже будет удален.
        second = courier_api.create_wrong_courier(login, password, first_name)

        assert second.status_code == 409
        assert TEXT_LOGIN_ALREADY_EXISTS in second.text

    @allure.title("Ошибка при создании курьера с отсутствующим логином или паролем")
    @pytest.mark.parametrize("login, password, expected_message", [
        ("", generate_random_string(10), "Недостаточно данных"),
        (generate_random_string(10), "", "Недостаточно данных"),
    ])
    def test_create_courier_missing_login_or_password(self,  login, password, expected_message):
        """
        Проверяет ошибки при создании курьера без логина или пароля.
        Args:
            courier_api (CourierApi): API клиент.
            login (str): Логин (может быть пустым).
            password (str): Пароль (может быть пустым).
            expected_message (str): Ожидаемое сообщение об ошибке.
        """
        courier_api = CourierApi()
        first_name = generate_random_string(10)

        # Если баг с невалидными данными, пройдет, то курьер тоже будет удален.
        response = courier_api.create_wrong_courier(login, password, first_name)

        assert response.status_code == 400
        assert expected_message in response.text

    @allure.title("Ошибка при создании курьера без имени")
    def test_create_courier_without_first_name(self):
        """
        Проверяет ошибку при создании курьера без имени.
        Args:
            courier_api (CourierApi): API клиент.
        """
        courier_api = CourierApi()
        login = generate_random_string(10)
        password = generate_random_string(10)

        # Если баг с невалидными данными, пройдет, то курьер тоже будет удален. 
        response = courier_api.create_wrong_courier(login, password, "") # тут особенно актуально

        assert response.status_code == 400
        assert TEXT_NOT_ENOUGH_DATA in response.text
