import allure
import requests
import pytest
from data.data import TestData


class TestLoginUser:

    # Успешная авторизация пользователя
    @allure.title("Проверка успешной авторизации пользователя")
    def test_successful_login(self, authorized_user):
        payload = {
            "email": authorized_user["email"],
            "password": authorized_user["password"]
        }

        response = requests.post(TestData.LOGIN_USER_API_URL, json=payload)

        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is True, "Запрос неуспешен"

    # Неуспешная авторизация с неверными данными
    @pytest.mark.parametrize("payload", [
        {"email": TestData.WRONG_EMAIL, "password": TestData.PASSWORD},
        {"email": TestData.EMAIL, "password": TestData.WRONG_PASSWORD},
        {"email": TestData.EMAIL},
        {"password": TestData.PASSWORD}
    ])
    @allure.title("Проверка невозможности авторизации с неверными данными")
    def test_login_failure_invalid_data(self, payload):

        response = requests.post(TestData.LOGIN_USER_API_URL, json=payload)

        assert response.status_code == 401, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"].strip().lower() == TestData.TEXT_EMAIL_OR_PASSWORD_ARE_INCORRECT, "Неверное сообщение об ошибке"
