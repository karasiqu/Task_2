import pytest
from helpers import generate_user_data, register_user, login_user, delete_user


@pytest.fixture
def new_user():
    payload = generate_user_data()
    register_user(payload)
    
    login_response = login_user(payload)
    access_token = login_response.json()["accessToken"]
    
    yield payload, access_token
    
    delete_user(access_token)

@pytest.fixture
def created_user():
    payload = generate_user_data()
    response = register_user(payload)

    login_response = login_user(payload)
    access_token = login_response.json()["accessToken"]

    yield response

    delete_user(access_token)