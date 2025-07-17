import random
import string
from api.courier_api import CourierApi
import allure


def generate_random_string(length: int) -> str:
    """
    Генерирует строку из строчных латинских букв заданной длины.
    Args:
        length (int): Длина строки.
    Returns:
        str: Случайная строка.
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_order_payload(color=None):
    return {
        "firstName": "Хината",
        "lastName": "Хьюга",
        "address": "д. Коноха, дом Хокаге",
        "metroStation": 2,
        "phone": "+7 999 999 99 99",
        "rentTime": 5,
        "deliveryDate": "2025-07-20",
        "comment": "Naruto is the best =)",
        "color": color if color is not None else []
    }


def register_new_courier_and_return_credentials(api = CourierApi()) -> tuple[str, str, str, int]:
    """
    Регистрирует нового курьера и возвращает его данные.
    Args:
        api (CourierApi): API клиент.
    Returns:
        tuple[str, str, str, int]: login, password, first_name, courier_id
    """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # Создание курьера и проверка успешности
    response = api.create_courier(login, password, first_name)
    assert response.status_code == 201

    # Логин для проверки
    login_response = api.login_courier(login, password)
    assert login_response.status_code == 200

    courier_id = login_response.json().get("id")
    return login, password, first_name, courier_id
