import requests
import pytest

def test_create_booking():
    url = "https://restful-booker.herokuapp.com/booking"
    data = {
        "firstname": "Ivan",
        "lastname": "Iuanov",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-03-23",
            "checkout": "2025-03-25"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200, "Failed to create booking"
    assert "bookingid" in response.json(), "No booking ID in response"

def test_get_booking():
    # Создаем бронь
    create_response = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json={"firstname": "Ivan",
              "lastname": "Iuanov",
              "totalprice": 111,
              "depositpaid": True,
              "bookingdates": {
                  "checkin": "2025-03-23",
                  "checkout": "2025-03-25"
              },
              "additionalneeds": "Breakfast"
              }
    )
    booking_id = create_response.json()["bookingid"]

    # Получаем бронь
    get_response = requests.get(f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert get_response.status_code == 200
    assert get_response.json()["firstname"] == "Ivan"

def test_update_booking():
    # Авторизуемся
    auth_response = requests.post(
        "https://restful-booker.herokuapp.com/auth",
        json={"username": "admin", "password": "password123"}
    )
    assert auth_response.status_code == 200, "Auth failed"
    token = auth_response.json()["token"]

    # Создаем бронирование
    create_response = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json={
            "firstname": "Ivan",
            "lastname": "Iuanov",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-03-23",
                "checkout": "2025-03-25"
            },
            "additionalneeds": "Breakfast"
        }
    )
    assert create_response.status_code == 200, "Booking creation failed"
    booking_id = create_response.json()["bookingid"]

    # Данные для обновления
    update_data = {
        "firstname": "Anatoly",
        "lastname": "Iuanov",
        "totalprice": 222,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-03-24",
            "checkout": "2025-03-26"
        },
        "additionalneeds": "Dinner"
    }

    # Отправляем обновление с авторизацией
    put_response = requests.put(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=update_data,
        headers={
            "Content-Type": "application/json",
            "Cookie": f"token={token}"  # Добавляем токен
        }
    )

    # Проверяем ответ
    assert put_response.status_code == 200, "Update failed"
    updated_data = put_response.json()

    # Проверяем обновленные поля
    assert updated_data["firstname"] == "Anatoly"
    assert updated_data["totalprice"] == 222
    assert updated_data["bookingdates"]["checkin"] == "2025-03-24"
    assert updated_data["additionalneeds"] == "Dinner"

    # Дополнительная проверка через GET
    get_response = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}"
    )
    assert get_response.json()["firstname"] == "Anatoly"

def test_update_booking():
    # Аутентификация
    auth_response = requests.post(
        "https://restful-booker.herokuapp.com/auth",
        json={"username": "admin", "password": "password123"}
    )
    assert auth_response.status_code == 200, "Auth failed"
    token = auth_response.json()["token"]

    # Создаем бронирование
    create_response = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json={
            "firstname": "Ivan",
            "lastname": "Iuanov",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-03-23",
                "checkout": "2025-03-25"
            },
            "additionalneeds": "Breakfast"
        }
    )
    assert create_response.status_code == 200, "Booking creation failed"
    booking_id = create_response.json()["bookingid"]

    # Данные для обновления
    update_data = {
        "firstname": "Anatoly",
        "lastname": "Iuanov",
        "totalprice": 222,  # Меняем цену для проверки
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-03-24",  # Меняем даты
            "checkout": "2025-03-26"
        },
        "additionalneeds": "Dinner"
    }

    # Отправляем обновление с авторизацией
    put_response = requests.put(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=update_data,
        headers={
            "Content-Type": "application/json",
            "Cookie": f"token={token}"  # Добавляем токен
        }
    )

    # Проверяем ответ
    assert put_response.status_code == 200, "Update failed"
    updated_data = put_response.json()

    # Проверяем обновленные поля
    assert updated_data["firstname"] == "Anatoly"
    assert updated_data["totalprice"] == 222
    assert updated_data["bookingdates"]["checkin"] == "2025-03-24"
    assert updated_data["additionalneeds"] == "Dinner"

    # Дополнительная проверка через GET
    get_response = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}"
    )
    assert get_response.json()["firstname"] == "Anatoly"

def test_delete_booking():
    auth_response = requests.post(
        "https://restful-booker.herokuapp.com/auth",
        json={"username": "admin", "password": "password123"}
    )
    assert auth_response.status_code == 200, "Auth failed"
    token = auth_response.json()["token"]
    # Создаем бронь
    create_response = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json={
            "firstname": "Ivan",
            "lastname": "Iuanov",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-03-23",
                "checkout": "2025-03-25"
            },
            "additionalneeds": "Breakfast"
        }
    )
    assert create_response.status_code == 200, "Booking creation failed"
    booking_id = create_response.json()["bookingid"]

    # Удаление брони с передачей токена
    delete_response = requests.delete(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        headers={"Cookie": f"token={token}"}  # Добавляем токен в заголовки
    )

    # Проверяем статус код
    assert delete_response.status_code == 201, "Delete failed"

    # Дополнительная проверка что бронь действительно удалена
    get_response = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}"
    )
    assert get_response.status_code == 404, "Booking still exists"

def test_get_bookings_by_name_filter():
    # Создаем тестовое бронирование для фильтрации
    create_response = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json={
            "firstname": "Ivan",
            "lastname": "Iuanov",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-03-23",
                "checkout": "2025-03-25"
            },
            "additionalneeds": "Breakfast"
        }
    )
    assert create_response.status_code == 200

    # Получаем бронирования по фильтру имени и фамилии
    get_response = requests.get(
        "https://restful-booker.herokuapp.com/booking",
        params={"firstname": "Ivan", "lastname": "Iuanov"}
    )

    assert get_response.status_code == 200
    bookings = get_response.json()
    assert len(bookings) > 0
    assert any(
        b["bookingid"] == create_response.json()["bookingid"]
        for b in bookings
    ), "Created booking not found in filtered results"

def test_auth_with_invalid_credentials():
    # Пытаемся аутентифицироваться с неверными данными
    invalid_auth_response = requests.post(
        "https://restful-booker.herokuapp.com/auth",
        json={
            "username": "admin",
            "password": "wrong_password"  # Неверный пароль
        }
    )

    # Проверяем ответ с ошибкой аутентификации
    assert invalid_auth_response.status_code == 200  # API возвращает 200 даже при ошибке
    assert "token" not in invalid_auth_response.json()
    assert "reason" in invalid_auth_response.json()
    assert invalid_auth_response.json()["reason"] == "Bad credentials"