import allure
import pytest
import requests
from data import UPDATE_FIELDS
from urls import BASE_URL, USER_INFO, TIMEOUT


@allure.feature("Изменение данных пользователя")
class TestUpdateUser:

    @allure.title("Изменение email с авторизацией")
    @allure.step("Изменить email авторизованного пользователя")
    def test_update_user_authorized(self, new_user):
        _, token = new_user
        new_email = "updated_email@yandex.ru"
        
        response = requests.patch(
            BASE_URL + USER_INFO,
            headers={"Authorization": token},
            json={"email": new_email},
            timeout=TIMEOUT,
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == new_email

    @allure.title("Изменение пароля с авторизацией")
    @allure.step("Изменить пароль авторизованного пользователя")
    def test_update_password_authorized(self, new_user):
        payload, token = new_user
        new_password = "updated_password123"

        response = requests.patch(
            BASE_URL + USER_INFO,
            headers={"Authorization": token},
            json={"password": new_password},
            timeout=TIMEOUT,
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Изменение поля {field} без авторизации")
    @pytest.mark.parametrize("field", UPDATE_FIELDS)
    @allure.step("Попытаться изменить данные без авторизации")
    def test_update_user_unauthorized(self, field):
        response = requests.patch(
            BASE_URL + USER_INFO,
            json={field: "updated_value"},
            timeout=TIMEOUT,
        )

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "You should be authorised"}
