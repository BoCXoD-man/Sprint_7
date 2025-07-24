import requests
import allure
from data.urls import BASE_URL


class OrderApi:
    def __init__(self):
        self.session = requests.Session()

    @allure.step("Создание заказа с телом: {payload}")
    def create_order(self, payload: dict):
        """
        Отправляет запрос на создание заказа.
        Args:
            payload (dict): Тело запроса для создания заказа.
        Returns:
            Response: Объект ответа от сервера.
        """
        return self.session.post(f"{BASE_URL}/api/v1/orders", json=payload)

    
    @allure.step("Получение списка заказов")
    def get_orders_list(self):
        """
        Отправляет запрос на получение списка заказов.
        Returns:
            Response: Объект ответа от сервера.
        """
        return self.session.get(f"{BASE_URL}/api/v1/orders")
    

    @allure.step("Принятие заказа {order_id} курьером с ID {courier_id}")
    def accept_order(self, order_id: int, courier_id: int):
        """
        Отправляет запрос на принятие заказа курьером.
        Args:
            order_id (int): ID заказа.
            courier_id (int): ID курьера.
        Returns:
            Response: Объект ответа от сервера.
        """
        return self.session.put(
            f"{BASE_URL}/api/v1/orders/accept/{order_id}",
            params={"courierId": courier_id})
    
    @allure.step("Получение заказа по трек-номеру {track}")
    def get_order_by_track(self, track: int) -> requests.Response:
        """
        Получает заказ по трек-номеру.

        Args:
            track (int): Трек-номер заказа.

        Returns:
            Response: Ответ от сервера.
        """
        url = f"{BASE_URL}/api/v1/orders/track"
        return self.session.get(url, params={"t": track})
    
    @allure.step("Отмена заказа по трек-номеру {track}")
    def cancel_order(self, track):
        """
        Отменяет заказ по его трек-номеру.
        Args:
            track (int): трек заказа
        Returns:
            Response: ответ API
        """
        url = f"{BASE_URL}/api/v1/orders/cancel"
        return self.session.put(url, json={"track": track})
