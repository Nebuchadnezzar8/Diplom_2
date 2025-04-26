import allure
import requests
from data.data import TestData


class TestCreateOrder:

    # Создание заказа с авторизацией
    @allure.title("Проверка создания заказа авторизованным пользователем с ингредиентами")
    def test_create_order_with_authorization(self, authorized_user, get_ingredients):
        headers = {"Authorization": authorized_user['accessToken']}
        payload = {"ingredients": get_ingredients[:2]}
        response = requests.post(TestData.ORDERS_API_URL, json=payload, headers=headers)

        assert response.status_code == 200, f"Ошибка при создании заказа: {response.text}"
        assert response.json()["success"] is True, "Система вернула неуспешный результат"
        assert "order" in response.json(), "Ответ не содержит данных о заказе"

    # Создание заказа без авторизации
    @allure.title("Проверка создания заказа без авторизации")
    def test_create_order_without_auth(self, get_ingredients):
        payload = {"ingredients": get_ingredients[:2]}
        response = requests.post(TestData.ORDERS_API_URL, json=payload)

        assert response.status_code == 200, f"Ошибка при создании заказа без авторизации: {response.text}"
        assert response.json()["success"] is True, "Система вернула неуспешный результат"
        assert "order" in response.json(), "Ответ не содержит данных о заказе"

    # Создание заказа без ингредиентов
    @allure.title("Проверка создания заказа с пустым списком ингредиентов")
    def test_create_order_with_empty_ingredients(self, authorized_user):
        headers = {"Authorization": authorized_user['accessToken']}
        payload = {"ingredients": []}
        response = requests.post(TestData.ORDERS_API_URL, json=payload, headers=headers)

        assert response.status_code == 400, f"Ожидался 400, но получен {response.status_code}: {response.text}"
        assert response.json()["success"] is False, "Система вернула успешный результат, хотя ожидалась ошибка"
        assert response.json()["message"] == TestData.TEXT_INGREDIENT_IDS_MUST_BE_PROVIDED, "Неверное сообщение об ошибке"

    # Создание заказа с неверным хешем ингредиентов
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, authorized_user):
        headers = {"Authorization": authorized_user['accessToken']}
        payload = {"ingredients": ["invalid_hash_123"]}
        response = requests.post(TestData.ORDERS_API_URL, json=payload, headers=headers)

        assert response.status_code == 500, f"Ожидался 500, но получен {response.status_code}: {response.text}"

