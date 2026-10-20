import allure
import requests
from urls import BASE_URL, GET_USER_ORDERS, TIMEOUT


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized(self, new_user):
        _, token = new_user
        
        response = requests.get(
            BASE_URL + GET_USER_ORDERS,
            headers={"Authorization": token},
            timeout=TIMEOUT,
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized(self):
        response = requests.get(
            BASE_URL + GET_USER_ORDERS,
            timeout=TIMEOUT,
        )

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "You should be authorised"}
        