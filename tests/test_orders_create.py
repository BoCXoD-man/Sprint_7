# import allure
# import pytest


# @allure.epic("Создание заказов")
# class TestOrderCreate:

#     @allure.title("Создание заказа с разными вариантами цвета. Цвета: {color}")
#     @pytest.mark.parametrize("color", [
#         ["BLACK"],
#         ["GREY"],
#         ["BLACK", "GREY"],
#         []
#     ])
#     def test_create_order_with_various_colors(self, order_api, color):
#         """
#         Проверяет создание заказа с указанными цветами или без них.
#         Args:
#             order_api (OrderApi): API клиент.
#             color (list): Список цветов в заказе.
#         """
#         payload = {
#             "firstName": "Хината",
#             "lastName": "Хьюга",
#             "address": "д. Коноха, дом Хокаге",
#             "metroStation": 2,
#             "phone": "+7 999 999 99 99",
#             "rentTime": 5,
#             "deliveryDate": "2025-07-20",
#             "comment": "Naruto is the best =)",
#             "color": color
#         }

#         response = order_api.create_order(payload)

#         assert response.status_code == 201
#         assert "track" in response.json()
#         assert isinstance(response.json()["track"], int)

import allure
import pytest
from helpers.generator import generate_order_payload


@allure.epic("Создание заказов")
class TestOrderCreate:

    @allure.title("Создание заказа с разными вариантами цвета. Цвета: {color}")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_various_colors(self, order_api, color):
        """
        Проверяет создание заказа с указанными цветами или без них.
        Args:
            order_api (OrderApi): API клиент.
            color (list): Список цветов в заказе.
        """
        payload = generate_order_payload(color=color)
        response = order_api.create_order(payload)

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)

        # Очистка заказа
        track = response.json()["track"]
        order_api.cancel_order(track)
