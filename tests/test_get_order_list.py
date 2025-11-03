import pytest
import requests
import allure
from urls import URLs


@allure.feature("Получение списка заказов")
class TestGetOrderList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        with allure.step("Отправить запрос на получение списка заказов"):
            response = requests.get(URLs.GET_ORDERS_LIST)
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
