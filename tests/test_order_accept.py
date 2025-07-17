import allure
import pytest
from helpers.generator import register_new_courier_and_return_credentials, generate_order_payload


@allure.epic("Принятие заказа")
class TestOrderAccept:

    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, courier_api, order_api):
        """
        Проверяет успешное принятие заказа курьером.
        Args:
            courier_api (CourierApi): API клиент.
            order_api (OrderApi): API клиент.
        """
        # создать курьера
        login, password, _ , _= register_new_courier_and_return_credentials()
        courier_id = courier_api.login_courier(login, password).json()["id"]

        # создать заказ
        payload = generate_order_payload(["BLACK"])
        order_response = order_api.create_order(payload)
        track = order_response.json()["track"]

        try:
            # получить order_id по треку
            order_id = order_api.get_order_by_track(track).json()["order"]["id"]

            # принять заказ
            accept_response = order_api.accept_order(order_id, courier_id)

            assert accept_response.status_code == 200
            assert accept_response.json().get("ok") is True
        finally:
            # удалить заказ и курьера
            order_api.cancel_order(track)
            courier_api.delete_courier(courier_id)

    @allure.title("Ошибка при некорректном ID курьера")
    @pytest.mark.parametrize(
        "order_id, courier_id, expected_status",
        [
            (1, None, 400),       # не передан courierId
            (1, 999999, 404),     # несуществующий courierId
        ]
    )
    def test_accept_order_invalid_courier_id(self, order_api, order_id, courier_id, expected_status):
        """
        Проверяет ошибки при некорректном ID курьера (отсутствующий или несуществующий).
        Args:
            order_api (OrderApi): API клиент.
            order_id (int): ID заказа.
            courier_id (int | None): ID курьера.
            expected_status (int): Ожидаемый HTTP-код.
        Returns:
            None
        """
        response = order_api.accept_order(order_id, courier_id)
        assert response.status_code == expected_status

    @allure.title("Ошибка при некорректном ID заказа")
    @pytest.mark.parametrize(
        "order_id, courier_id, expected_status",
        [
            (None, 1, 404),       # заказ не передан в URL
            (999999, 1, 404),     # несуществующий заказ
        ])
    def test_accept_order_invalid_order_id(self, order_api, order_id, courier_id, expected_status):
        """
        Проверяет ошибки при некорректном ID заказа (отсутствующий или несуществующий).
        """
        response = order_api.accept_order(order_id, courier_id)
        assert response.status_code == expected_status
