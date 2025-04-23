import pytest
import requests
from faker import Faker
from data.data import TestData

fake = Faker()


@pytest.fixture
def created_user():
    email = f"{fake.random_int()}_{fake.email()}"
    password = fake.password()
    name = fake.name()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(TestData.REGISTER_USER_API_URL, json=payload)

    return {
        "email": email,
        "password": password,
        "name": name,
        "response": response
    }


@pytest.fixture
def logged_in_user(created_user):
    payload = {
        "email": created_user["email"],
        "password": created_user["password"]
    }

    response = requests.post(TestData.LOGIN_USER_API_URL, json=payload)

    data = response.json()

    return {
        "email": created_user["email"],
        "password": created_user["password"],
        "name": created_user["name"],
        "accessToken": data.get("accessToken"),
        "refreshToken": data.get("refreshToken"),
        "response": response
    }


@pytest.fixture
def get_ingredients():
    response = requests.get(TestData.INGREDIENTS_API_URL)

    data = response.json()
    return [ingredient["_id"] for ingredient in data["data"]]


@pytest.fixture
def authorized_user(logged_in_user):
    yield logged_in_user

    headers = {"Authorization": logged_in_user["accessToken"]}
    requests.delete(TestData.USER_API_URL, headers=headers)
