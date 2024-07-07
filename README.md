# api_yamdb
api_yamdb

## Аутентификация и управление пользователями

### Регистрация нового пользователя

Эндпоинт: `/api/v1/auth/signup/`  
Метод: `POST`

Пример запроса:
```json
{
    "email": "user@example.com",
    "username": "example_user"
}
```
Пример ответа:
```json
{
    "email": "user@example.com",
    "username": "example_user"
}
```
### Получение JWT-токена
Эндпоинт: `/api/v1/auth/token/`    
Метод: `POST`

Пример запроса:
```json
{
    "username": "example_user",
    "confirmation_code": "12345"
}
```
Пример ответа:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2NTM2OTAxLCJqdGkiOiI3ZjU5OGM5MzM4Njk0ZDAwYjhkMWZkNTU2MzQ1MjJiOSIsInVzZXJfaWQiOjF9.UymM_Rl2BjP1UW-rZpUXMhW-7PabDj9j8v8fCxIKPcs"
}
```

## Тестирование проекта через Postman

Для упрощения тестирования в проекте предусмотрен режим фиксированного кода подтверждения. 
Когда `USE_FIXED_CONFIRMATION_CODE = True` в настройках, всем пользователям будет отдаваться код '12345'.
Не забудьте установить `USE_FIXED_CONFIRMATION_CODE = False` перед развертыванием в продакшене!
