import allure
from helpers.generator import register_new_courier_and_return_credentials


@allure.epic("Удаление курьера")
class TestCourierDelete:

    @allure.title("Успешное удаление курьера")
    def test_delete_existing_courier(self, courier_api):
        """
        Проверяет успешное удаление ранее зарегистрированного курьера.
        Args:
            courier_api (CourierApi): API клиент.
        Returns:
            None
        """
        login, password, _, _ = register_new_courier_and_return_credentials()
        login_response = courier_api.login_courier(login, password)
        courier_id = login_response.json()["id"]

        delete_response = courier_api.delete_courier(courier_id)

        assert delete_response.status_code == 200
        assert delete_response.json().get("ok") is True

    @allure.title("Ошибка при удалении без ID (ручка требует ID в пути)")
    def test_delete_without_id(self, courier_api):
        """
        Проверяет ошибку при попытке удалить курьера без указания ID.
        Args:
            courier_api (CourierApi): API клиент.
        Returns:
            None
        """
        response = courier_api.delete_courier("")
        assert response.status_code == 404

    @allure.title("Ошибка при удалении несуществующего ID")
    def test_delete_nonexistent_courier(self, courier_api):
        """
        Проверяет ошибку при удалении курьера с несуществующим ID.
        Args:
            courier_api (CourierApi): API клиент.
        Returns:
            None
        """
        nonexistent_id = 999999
        response = courier_api.delete_courier(nonexistent_id)

        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.text
