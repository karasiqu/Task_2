import allure
from helpers import login_user


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Логин под существующим пользователем")
    def test_login_success(self, new_user):
        payload, _ = new_user
        response = login_user(payload)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Логин с неверным логином и паролем")
    def test_login_wrong_credentials(self, new_user):
        payload, _ = new_user
        wrong_payload = {
            "email": "wrong_" + payload["email"],
            "password": "wrong_password",
        }
        response = login_user(wrong_payload)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "email or password are incorrect"}
        