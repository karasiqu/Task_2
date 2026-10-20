import allure
import pytest
import requests
from data import UPDATE_FIELDS
from urls import BASE_URL, USER_INFO, TIMEOUT


@allure.feature("Изменение данных пользователя")
class TestUpdateUser:

    @allure.title("Изменение поля {field} с авторизацией")
    @pytest.mark.parametrize("field", UPDATE_FIELDS)
    def test_update_user_authorized(self, new_user, field):
        _, token = new_user
        new_value = "updated_" + field
        
        response = requests.patch(
            BASE_URL + USER_INFO,
            headers={"Authorization": token},
            json={field: new_value},
            timeout=TIMEOUT,
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        
        if field != "password":
            assert response.json()["user"][field] == new_value

    @allure.title("Изменение поля {field} без авторизации")
    @pytest.mark.parametrize("field", UPDATE_FIELDS)
    def test_update_user_unauthorized(self, field):
        response = requests.patch(
            BASE_URL + USER_INFO,
            json={field: "updated_value"},
            timeout=TIMEOUT,
        )

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "You should be authorised"}
