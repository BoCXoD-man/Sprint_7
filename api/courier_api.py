import requests
import allure
from data.urls import BASE_URL


class CourierApi:
    def __init__(self):
        self.session = requests.Session()

    @allure.step("Создание нового курьера с логином: {login}")
    def create_courier(self, login: str, password: str, first_name: str):
        """
        Создаёт нового курьера.
        Args:
            login (str): Логин курьера.
            password (str): Пароль курьера.
            first_name (str): Имя курьера.
        Returns:
            Response: Объект ответа от сервера.
        """
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return self.session.post(f"{BASE_URL}/api/v1/courier", data=payload)
    
    @allure.step("Создание нового курьера с невалидными данными, логин: {login}")
    def create_wrong_courier(self, login: str, password: str, first_name: str):
        """
        Создаёт нового курьера c невалидными данными.
        Удаляется курьер после создания.
        Args:
            login (str): Логин курьера.
            password (str): Пароль курьера.
            first_name (str): Имя курьера.
        Returns:
            Response: Объект ответа от сервера.
        """
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = self.session.post(f"{BASE_URL}/api/v1/courier", data=payload)

        if response.status_code == 201:
            login_response = self.login_courier(login, password)
            if login_response.status_code == 200 and "id" in login_response.json():
                courier_id = login_response.json()["id"]
                self.delete_courier(courier_id)
        return response

    @allure.step("Авторизация курьера с логином: {login}")
    def login_courier(self, login: str, password: str):
        """
        Авторизует курьера в системе.
        Args:
            login (str): Логин курьера.
            password (str): Пароль курьера.
        Returns:
            Response: Объект ответа от сервера.
        """
        payload = {
            "login": login,
            "password": password
        }
        return self.session.post(f"{BASE_URL}/api/v1/courier/login", data=payload)
    

    @allure.step("Удаление курьера с ID: {courier_id}")
    def delete_courier(self, courier_id: int):
        """
        Удаляет курьера по ID.
        Args:
            courier_id (int): Идентификатор курьера.
        Returns:
            Response: Объект ответа от сервера.
        """
        return self.session.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")
