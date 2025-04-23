import allure
import requests
import pytest
from data.data import TestData


# Проверка создания пользователя
class TestCreateUser:

    # Создание нового пользователя
    @allure.title("Проверка успешного создания нового пользователя")
    def test_create_new_user_successfully(self, created_user):
        assert created_user is not None, "Созданный пользователь отсутствует"

        response = created_user["response"]
        assert response.status_code == 200, f"Ошибка при создании пользователя: {response.text}"

        data = response.json()
        assert data.get("success"), "Неуспешное создание пользователя"

    # Создание уже существующего пользователя
    @pytest.mark.parametrize("payload, expected_status_code, expected_success, expected_message", [
        (
            {"email": TestData.EXISTING_EMAIL, "password": TestData.PASSWORD, "name": TestData.NAME},
            403,
            False,
            "User already exists"
        ),
    ])
    @allure.title('Проверка невозможности создания пользователя с существующим email')
    def test_create_existing_user(self, created_user, payload, expected_status_code, expected_success, expected_message):

        response = requests.post(TestData.REGISTER_USER_API_URL, json={
            "email": created_user["email"],
            "password": created_user["password"],
            "name": created_user["name"]
        })

        assert response.status_code == expected_status_code, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] == expected_success, "Ожидалась ошибка, но запрос прошел успешно"
        assert data["message"] == expected_message, f"Ожидалось сообщение '{expected_message}', но получено '{data['message']}'"

    # Создание пользователя с незаполненным обязательным полем
    @pytest.mark.parametrize("payload", [
        {"email": TestData.EMAIL, "password": TestData.PASSWORD},
        {"password": TestData.PASSWORD, "name": TestData.NAME},
        {"email": TestData.EMAIL, "name": TestData.NAME}
    ])
    @allure.title('Проверка невозможности создания пользователя с пропущенным обязательным полем')
    def test_create_user_with_missing_field(self, payload):

        response = requests.post(TestData.REGISTER_USER_API_URL, json=payload)

        assert response.status_code == 403, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"] == TestData.TEXT_EMAIL_PASSWORD_AND_NAME_ARE_REQUIRED_FIELDS, "Неверное сообщение об ошибке"





