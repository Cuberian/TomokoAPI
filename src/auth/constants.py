class ErrorCode:
    AUTHENTICATION_REQUIRED = "Необходима аутентификация."
    AUTHORIZATION_FAILED = "Авторизация провалена. У пользователя нет доступа."
    INVALID_TOKEN = "Невалидный токен."
    INVALID_CREDENTIALS = "Некорректные данные пользователя."
    EMAIL_TAKEN = "Почта уже существует."
    REFRESH_TOKEN_NOT_VALID = "Токен обновления не валиден."
    REFRESH_TOKEN_REQUIRED = "Токен обновления требуется либо в теле, либо в cookie."
