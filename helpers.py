import random
import string
import requests
from urls import BASE_URL, CREATE_USER, LOGIN_USER, USER_INFO, TIMEOUT


def generate_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_user_data():
    email = f"{generate_random_string(10)}@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(10)
    return {"email": email, "password": password, "name": name}


def register_user(payload):
    return requests.post(BASE_URL + CREATE_USER, json=payload, timeout=TIMEOUT)


def login_user(payload):
    return requests.post(BASE_URL + LOGIN_USER, json=payload, timeout=TIMEOUT)


def delete_user(access_token):
    return requests.delete(
        BASE_URL + USER_INFO,
        headers={"Authorization": access_token},
        timeout=TIMEOUT,
    )
