import allure
import requests
import pytest
from faker import Faker
from data.data import TestData

fake = Faker()


class TestUpdateUserData:

    # Изменение данных авторизованного пользователя
    @allure.title("Проверка изменения данных авторизованного пользователя")
    @pytest.mark.parametrize("update_payload", [
        {"email": f"{fake.random_int()}_newemail@yandex.ru", "expected_key": "email"},  # Генерация уникального email
        {"name": "Updated Name", "expected_key": "name"}  # Изменение имени
    ])
    def test_update_user_with_authorization(self, authorized_user, update_payload):
        # Проверка начального состояния пользователя
        response = requests.get(TestData.USER_API_URL, headers={"Authorization": authorized_user["accessToken"]})
        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is True, "Запрос неуспешен"

        # Обновление данных пользователя
        headers = {"Authorization": authorized_user["accessToken"]}
        response = requests.patch(TestData.USER_API_URL, json=update_payload, headers=headers)

        assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}: {response.text}"
        data = response.json()
        assert data["success"] is True, "Запрос неуспешен"

        # Проверка данных после обновления
        response = requests.get(TestData.USER_API_URL, headers=headers)
        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()
        assert data["user"].get(update_payload.get("expected_key")) != authorized_user.get(
            update_payload.get("expected_key")), "Поле не обновлено"

    # изменение данных без авторизации
    @pytest.mark.parametrize("update_payload", [
        {"email": "unauthemail@yandex.ru"},
        {"name": "Unauthorized Name"},
        {"password": "unauthpassword69"}
    ])
    @allure.title("Проверка невозможности изменения данных без авторизации")
    def test_update_user_without_authorization(self, update_payload):
        response = requests.patch(TestData.USER_API_URL, json=update_payload)

        assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code}: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"] == TestData.TEXT_YOU_SHOULD_BE_AUTHORIZED, "Неверное сообщение об ошибке"

    # Изменение email на уже существующий
    @pytest.mark.parametrize("update_payload", [
        {"email": "existing_user@yandex.ru"}  # Уже существующий email
    ])
    @allure.title("Проверка невозможности обновления email на уже существующий")
    def test_update_user_to_existing_email(self, authorized_user, update_payload):
        headers = {"Authorization": authorized_user["accessToken"]}
        response = requests.patch(TestData.USER_API_URL, json=update_payload, headers=headers)

        assert response.status_code == 403, f"Ожидался 403, но получен {response.status_code}: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"] == TestData.TEXT_USER_WITH_SUCH_EMAIL_ALREADY_EXISTS, "Неверное сообщение об ошибке"
