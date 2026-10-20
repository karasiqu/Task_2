import allure
import requests
from data import INGREDIENTS
from urls import BASE_URL, CREATE_ORDER, TIMEOUT


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized(self, new_user):
        _, token = new_user
        
        response = requests.post(
            BASE_URL + CREATE_ORDER,
            headers={"Authorization": token},
            json={"ingredients": INGREDIENTS},
            timeout=TIMEOUT,
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self):
        response = requests.post(
            BASE_URL + CREATE_ORDER,
            json={"ingredients": INGREDIENTS},
            timeout=TIMEOUT,
        )

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "You should be authorised"}

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, new_user):
        _, token = new_user
        
        response = requests.post(
            BASE_URL + CREATE_ORDER,
            headers={"Authorization": token},
            json={"ingredients": []},
            timeout=TIMEOUT,
        )

        assert response.status_code == 400
        assert response.json() == {"success": False, "message": "Ingredient ids must be provided"}

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_wrong_hash(self, new_user):
        _, token = new_user
        
        response = requests.post(
            BASE_URL + CREATE_ORDER,
            headers={"Authorization": token},
            json={"ingredients": ["invalid_hash_123"]},
            timeout=TIMEOUT,
        )

        assert response.status_code == 500
        