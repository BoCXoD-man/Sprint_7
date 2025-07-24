import allure
import pytest
from helpers.generator import generate_order_payload
from api.order_api import OrderApi


@allure.epic("Создание заказов")
class TestOrderCreate:

    @allure.title("Создание заказа с разными вариантами цвета. Цвета: {color}")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_various_colors(self, color):
        """
        Проверяет создание заказа с указанными цветами или без них.
        Args:
            order_api (OrderApi): API клиент.
            color (list): Список цветов в заказе.
        """
        order_api = OrderApi()
        payload = generate_order_payload(color)
        response = order_api.create_order(payload)

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
