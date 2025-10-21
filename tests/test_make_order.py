import pytest
import requests
import allure
import random
import string
from data import ORDER_DATA, ORDER_COLORS
from urls import URLs


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@allure.feature("Создание заказа")
class TestMakeOrder:

    @pytest.mark.parametrize("color", ORDER_COLORS)
    @allure.title("Создание заказа с цветом: {color}")
    def test_create_order_with_different_colors(self, color):
        order_data = ORDER_DATA.copy()
        order_data["color"] = color
        order_data["firstName"] = generate_random_string(8)
        order_data["lastName"] = generate_random_string(8)

        response = requests.post(URLs.CREATE_ORDER, json=order_data)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без поля color")
    def test_create_order_without_color_field(self):
        order_data = ORDER_DATA.copy()
        order_data.pop("color", None)
        order_data["firstName"] = generate_random_string(8)
        order_data["lastName"] = generate_random_string(8)

        response = requests.post(URLs.CREATE_ORDER, json=order_data)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа с данными из data.py")
    def test_create_order_with_data_from_data_py(self):
        response = requests.post(URLs.CREATE_ORDER, json=ORDER_DATA)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа с минимальными данными")
    def test_create_order_with_minimal_data(self):
        order_data = {
            "firstName": "Тестовый",
            "lastName": "Пользователь",
            "address": "Москва, ул. Тестовая, 123",
            "metroStation": 5,
            "phone": "+7 900 123 45 67",
            "rentTime": 3,
            "deliveryDate": "2024-12-25"
        }

        response = requests.post(URLs.CREATE_ORDER, json=order_data)
        assert response.status_code == 201
        assert "track" in response.json()
