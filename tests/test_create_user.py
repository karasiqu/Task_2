import allure
import pytest
from data import MISSING_FIELDS
from helpers import generate_user_data, register_user


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.step("Создать пользователя и проверить ответ")
    def test_create_unique_user(self, created_user):
        response = created_user

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание уже зарегистрированного пользователя")
    @allure.step("Попытаться создать существующего пользователя")
    def test_create_existing_user(self, new_user):
        payload, _ = new_user

        response = register_user(payload)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": "User already exists"}

    @allure.title("Создание пользователя без поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", MISSING_FIELDS)
    @allure.step("Создать пользователя без обязательного поля")
    def test_create_user_without_field(self, missing_field):
        payload = generate_user_data()
        del payload[missing_field]
        
        response = register_user(payload)

        assert response.status_code == 403
        assert response.json() == {
            "success": False, 
            "message": "Email, password and name are required fields"
        }
        