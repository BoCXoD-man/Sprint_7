import pytest
from helpers.generator import (
    generate_order_payload, 
    generate_random_string
    )
from api.courier_api import CourierApi
from api.order_api import OrderApi


@pytest.fixture
def courier_with_cleanup():
    """
    Создаёт курьера, сразу получает ID через логин. Возвращает все данные.
    Удаляет курьера по ID даже при падении теста.
    """
    courier_api = CourierApi()
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    register_response = courier_api.create_courier(login, password, first_name)
    courier_id = None

    if register_response.status_code == 201:
        login_response = courier_api.login_courier(login, password)
        if login_response.status_code == 200 and "id" in login_response.json():
            courier_id = login_response.json()["id"]

    yield {
        "login": login,
        "password": password,
        "first_name": first_name,
        "register_response": register_response,
        "courier_id": courier_id
    }

    # Удаляем, если знаем ID
    if courier_id:
        courier_api.delete_courier(courier_id)
@pytest.fixture
def order_with_cleanup():
    """
    Создаёт заказ и удаляет его после теста.
    """
    order_api = OrderApi()
    payload = generate_order_payload()
    response = order_api.create_order(payload)
    track = response.json()["track"]
    yield payload, track, response
    order_api.cancel_order(track)
