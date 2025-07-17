import allure


@allure.epic("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, order_api):
        """
        Проверяет, что возвращается список заказов.
        """
        response = order_api.get_orders_list()

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        try:
            json_data = response.json()
        except ValueError:
            raise AssertionError(f"Ответ не является JSON: {response.text}")

        assert "orders" in json_data, f"'orders' отсутствует в ответе: {json_data}"
        assert isinstance(json_data["orders"], list), "'orders' должен быть списком"
        assert len(json_data["orders"]) > 0, "Список заказов пуст"
