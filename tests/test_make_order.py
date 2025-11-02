import pytest
import requests
import allure
from data import ORDER_DATA, ORDER_COLORS
from urls import URLs


@allure.feature("Создание заказа")
class TestMakeOrder:

    @allure.title("Тест: можно создать заказ с разными цветами")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_different_colors(self, color):
        payload = ORDER_DATA.copy()
        payload["color"] = color
        
        with allure.step("Создать заказ с выбранным цветом"):
            response = requests.post(URLs.CREATE_ORDER, json=payload)
        
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Тест: заказ можно создать без указания цвета")
    def test_create_order_without_color(self):
        payload = ORDER_DATA.copy()
        payload.pop("color", None)
        
        with allure.step("Создать заказ без указания цвета"):
            response = requests.post(URLs.CREATE_ORDER, json=payload)
        
        assert response.status_code == 201
        assert "track" in response.json()
