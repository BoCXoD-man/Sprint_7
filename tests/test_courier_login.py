import allure
import pytest
from helpers.generator import generate_random_string


@allure.epic("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    def test_login_successful(self, courier_with_cleanup, courier_api):
        """
        Проверяет, что курьер может авторизоваться при корректных данных.
        После теста удаляет созданного курьера.
        Args:
            courier_api (CourierApi): API клиент.
            courier_with_cleanup (tuple): Кортеж с данными курьера.
        """
        login, password, _, _ = courier_with_cleanup
        response = courier_api.login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Ошибка при неверном логине")
    def test_login_with_invalid_login(self, courier_with_cleanup, courier_api):
        """
        Проверяет, что авторизация с неверным логином вызывает ошибку.
        После теста удаляет созданного курьера.
        """
        _, password, _, _ = courier_with_cleanup
        response = courier_api.login_courier("wronglogin", password)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.title("Ошибка при неверном пароле")
    def test_login_with_invalid_password(self, courier_with_cleanup, courier_api):
        """
        Проверяет, что авторизация с неверным паролем вызывает ошибку.
        После теста удаляет созданного курьера.
        Args:
            courier_api (CourierApi): API клиент.
            courier_with_cleanup (tuple): Кортеж с данными курьера.
        """
        login, _, _, _ = courier_with_cleanup
        response = courier_api.login_courier(login, "wrongpassword")

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.title("Ошибка при отсутствии логина или пароля")
    @pytest.mark.parametrize("login,password", [
        ("", generate_random_string(10)),  # отсутствует логин
        (generate_random_string(10), ""),  # отсутствует пароль
    ])
    def test_login_with_missing_credentials(self, courier_api, login, password):
        """
        Проверяет, что при отсутствии логина или пароля возвращается ошибка 400.
        """
        response = courier_api.login_courier(login, password)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.text
