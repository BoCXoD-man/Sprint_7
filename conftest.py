import pytest
from api.courier_api import CourierApi
from api.order_api import OrderApi
from helpers.generator import register_new_courier_and_return_credentials, generate_order_payload


@pytest.fixture
def courier_api():
    """
    Создаёт клиент для работы с API курьера.
    Args:
        None
    Returns:
        CourierApi: Экземпляр API-клиента.
    """
    return CourierApi()

@pytest.fixture
def order_api():
    """
    Возвращает экземпляр API клиента заказов.
    Returns:
        OrderApi: API клиент.
    """
    return OrderApi()

@pytest.fixture
def courier_with_cleanup(courier_api):
    """
    Создаёт нового курьера и возвращает его данные.
    После теста удаляет созданного курьера. ё
    Args:
        courier_api (CourierApi): API клиент.
    Returns:
        tuple[str, str, str, int]: login, password, first_name, courier_id
    """
    login, password, first_name, courier_id = register_new_courier_and_return_credentials(courier_api)
    yield login, password, first_name, courier_id
    courier_api.delete_courier(courier_id)

@pytest.fixture
def order_with_cleanup(order_api):
    """
    Создаёт заказ и удаляет его после теста.
    """
    payload = generate_order_payload()
    response = order_api.create_order(payload)
    track = response.json()["track"]
    yield payload, track
    order_api.cancel_order(track)
