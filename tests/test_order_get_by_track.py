import allure
import pytest
from api.order_api import OrderApi


@allure.epic("Заказы")
@allure.feature("Получение заказа по трек-номеру")
class TestGetOrderByTrack:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = OrderApi()

    @allure.title("Успешное получение заказа по трек-номеру")
    def test_get_order_success(self, order_with_cleanup):
        """
        Проверяет успешное получение заказа по валидному трек-номеру.
        """

        # Создание заказа
        _, track, response = order_with_cleanup
        assert response.status_code == 201, f"Create order failed: {response.text}"
        assert track is not None, f"Track not returned: {response.text}"

        # Получение заказа по треку
        order_response = self.api.get_order_by_track(track)
        assert order_response.status_code == 200, f"Expected 200, got {order_response.status_code}, body: {order_response.text}"

        json_data = order_response.json()
        assert "order" in json_data, f"'order' not in response: {json_data}"
        assert json_data["order"]["track"] == track

    @allure.title("Ошибка при неверном трек-номере: {track}")
    @pytest.mark.parametrize(
        "track, expected_status",
        [
            (None, 400),        # Отсутствует параметр track
            (999999, 404),      # Несуществующий track
        ]
    )
    def test_get_order_with_invalid_track(self, track, expected_status):
        """
        Проверяет, что запрос с отсутствующим или несуществующим трек-номером возвращает ошибку.
        Args:
            order_api (OrderApi): API клиент.
            track (int | None): Трек-номер.
            expected_status (int): Ожидаемый HTTP-статус.
        """
        order_api = OrderApi()
        response = order_api.get_order_by_track(track)
        assert response.status_code == expected_status
