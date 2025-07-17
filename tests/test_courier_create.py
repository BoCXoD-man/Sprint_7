import allure
import pytest
from helpers.generator import generate_random_string


@allure.epic("Регистрация курьера")
class TestCourierCreate:
    """
    Тесты для регистрации курьера через API.
    Args:
        courier_api (CourierApi): API клиент.
    """

    @allure.title("Успешное создание курьера")
    def test_create_courier_successfully(self, courier_api):
        """
        Проверяет, что курьер успешно создаётся при корректных данных.
        После теста курьер удаляется.
        Args:
            courier_api (CourierApi): API клиент.
        """
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = courier_api.create_courier(login, password, first_name)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Удаление после теста
        login_response = courier_api.login_courier(login, password)
        assert login_response.status_code == 200
        courier_id = login_response.json()["id"]
        courier_api.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier_api):
        """
        Проверяет, что нельзя создать курьера с тем же логином.
        После теста курьер удаляется.
        Args:
            courier_api (CourierApi): API клиент.
        """
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        first = courier_api.create_courier(login, password, first_name)
        second = courier_api.create_courier(login, password, first_name)

        assert first.status_code == 201
        assert second.status_code == 409
        assert "Этот логин уже используется" in second.text

        # Удаление курьера
        login_response = courier_api.login_courier(login, password)
        assert login_response.status_code == 200
        courier_id = login_response.json()["id"]
        courier_api.delete_courier(courier_id)

    @allure.title("Ошибка при создании курьера с отсутствующим логином или паролем")
    @pytest.mark.parametrize("login, password, expected_message", [
        ("", generate_random_string(10), "Недостаточно данных"),
        (generate_random_string(10), "", "Недостаточно данных"),
    ])
    def test_create_courier_missing_login_or_password(self, courier_api, login, password, expected_message):
        """
        Проверяет ошибки при создании курьера без логина или пароля.
        Args:
            courier_api (CourierApi): API клиент.
            login (str): Логин (может быть пустым).
            password (str): Пароль (может быть пустым).
            expected_message (str): Ожидаемое сообщение об ошибке.
        """
        first_name = generate_random_string(10)

        response = courier_api.create_courier(login, password, first_name)

        assert response.status_code == 400
        assert expected_message in response.text

    @allure.title("Ошибка при создании курьера без имени")
    def test_create_courier_without_first_name(self, courier_api):
        """
        Проверяет ошибку при создании курьера без имени.
        Args:
            courier_api (CourierApi): API клиент.
        """
        login = generate_random_string(10)
        password = generate_random_string(10)

        response = courier_api.create_courier(login, password, "")

        assert response.status_code == 400
        assert "Недостаточно данных" in response.text
