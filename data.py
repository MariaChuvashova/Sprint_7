# Данные для создания заказа
ORDER_DATA = {
    "firstName": "Тестовый",
    "lastName": "Пользователь",
    "address": "Москва, ул. Тестовая, 123",
    "metroStation": 5,
    "phone": "+7 900 123 45 67",
    "rentTime": 3,
    "deliveryDate": "2025-07-22",
    "comment": "Тестовый заказ для проверки API",
    "color": ["BLACK"]
}

# Базовые данные для создания курьера
COURIER_DATA = {
    "login": "test_courier_001",
    "password": "password123",
    "firstName": "ТестовыйКурьер"
}

# Данные для авторизации курьера
LOGIN_DATA = {
    "login": "test_user_001", 
    "password": "password123"
}

# Цвета для параметризации тестов заказов
ORDER_COLORS = [
    ["BLACK"],
    ["GREY"], 
    ["BLACK", "GREY"],
    []
]

# Данные для тестирования создания курьера
COURIER_TEST_DATA = {
    "valid": {
        "login": "valid_courier",
        "password": "valid_password",
        "firstName": "ВалидныйКурьер"
    },
    "missing_login": {
        "password": "test_password",
        "firstName": "КурьерБезЛогина"
    },
    "missing_password": {
        "login": "courier_no_pass",
        "firstName": "КурьерБезПароля"
    },
    "missing_first_name": {
        "login": "courier_no_name",
        "password": "password123"
    }
}

# Ожидаемые сообщения об ошибках
ERROR_MESSAGES = {
    "missing_data": "Недостаточно данных для создания учетной записи",
    "missing_login_data": "Недостаточно данных для входа", 
    "login_exists": "Этот логин уже используется",
    "account_not_found": "Учетная запись не найдена"
}

# Коды статусов HTTP
STATUS_CODES = {
    "created": 201,
    "success": 200,
    "bad_request": 400,
    "not_found": 404,
    "conflict": 409
}
