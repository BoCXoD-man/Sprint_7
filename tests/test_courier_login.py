import allure
import pytest
from helpers.generator import generate_random_string
from api.courier_api import CourierApi
from data.data import TEXT_ACCOUNT_NOT_FOUND, TEXT_NOT_ENOUGH_DATA


@allure.epic("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    def test_login_successful(self, courier_with_cleanup):
        """
        Проверяет, что курьер может авторизоваться при корректных данных.
        После теста удаляет созданного курьера.
        Args:
            courier_api (CourierApi): API клиент.
            courier_with_cleanup (tuple): Кортеж с данными курьера.
        """
        courier_api = CourierApi()
        login, password= courier_with_cleanup['login'], courier_with_cleanup['password']
        response = courier_api.login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Ошибка при неверном логине")
    def test_login_with_invalid_login(self, courier_with_cleanup):
        """
        Проверяет, что авторизация с неверным логином вызывает ошибку.
        После теста удаляет созданного курьера.
        """
        courier_api = CourierApi()
        password= courier_with_cleanup['password']
        response = courier_api.login_courier("wronglogin", password)

        assert response.status_code == 404
        assert TEXT_ACCOUNT_NOT_FOUND in response.text

    @allure.title("Ошибка при неверном пароле")
    def test_login_with_invalid_password(self, courier_with_cleanup):
        """
        Проверяет, что авторизация с неверным паролем вызывает ошибку.
        После теста удаляет созданного курьера.
        Args:
            courier_api (CourierApi): API клиент.
            courier_with_cleanup (tuple): Кортеж с данными курьера.
        """
        courier_api = CourierApi()
        login= courier_with_cleanup['login']
        response = courier_api.login_courier(login, "wrongpassword")

        assert response.status_code == 404
        assert TEXT_ACCOUNT_NOT_FOUND in response.text

    @allure.title("Ошибка при авторизации с некорректными данными")
    @pytest.mark.parametrize(
        "login_mod, password_mod, expected_message",
        [
            ("wrong", "correct", TEXT_ACCOUNT_NOT_FOUND),
            ("correct", "wrong", TEXT_ACCOUNT_NOT_FOUND),
        ]
    )
    def test_login_with_invalid_credentials(self, courier_with_cleanup, login_mod, password_mod, expected_message):
        """
        Проверяет, что авторизация с неправильным логином или паролем вызывает ошибку 404.
        После теста курьер удаляется через фикстуру.
        """
        courier_api = CourierApi()
        login, password= courier_with_cleanup['login'], courier_with_cleanup['password']


        if login_mod == "wrong":
            login = "wronglogin"
        if password_mod == "wrong":
            password = "wrongpassword"

        response = courier_api.login_courier(login, password)

        assert response.status_code == 404
        assert expected_message in response.text

    @allure.title("Ошибка при отсутствии логина или пароля")
    @pytest.mark.parametrize("login,password", [
        ("", generate_random_string(10)),  # отсутствует логин
        (generate_random_string(10), ""),  # отсутствует пароль
    ])
    def test_login_with_missing_credentials(self, login, password):
        """
        Проверяет, что при отсутствии логина или пароля возвращается ошибка 400.
        """
        courier_api = CourierApi()
        response = courier_api.login_courier(login, password)

        assert response.status_code == 400
        assert TEXT_NOT_ENOUGH_DATA in response.text
