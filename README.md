# api_yamdb

## Описание

Проект ***YaMDb*** - это платформа для сбора отзывов пользователей на произведения.

## Информация о проекте

Стек технологий: **Python** 3.9.13, **Django**, **Django REST Framework**, **Simple JWT**;

Спецификация API: Доступна в файле `api_yamdb\api_yamdb\static\redoc.yaml`;

Над проектом работали: [scsluway](https://github.com/scsluway), [colddecember](https://github.com/colddecember), [NikitDeveloper](https://github.com/NikitDeveloper).

## Инструкция к установке

Клонировать репозиторий и перейти в него в командной строке:

```shell
git clone git@github.com:yandex-praktikum/api_final_yatube.git
```

Перейти в корень проекта API_Final_Yatube:

```shell
cd api_final_yatube/
```

Cоздать и активировать виртуальное окружение:

```shell
python3 -m venv venv
```

Активировать виртуальное окружение:

```shell
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```shell
python3 -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

Перейти в рабочую директорию проекта, в которой лежит файл *manage.py*:

```shell
cd yatube_api/
```

Выполнить миграции:

```shell
python3 manage.py migrate
```

Запустить проект:

```shell
python3 manage.py runserver
```

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

### Управление произведениями, категориями, жанрами, отзывами и комментариями

### Произведения

Эндпоинт: `/api/v1/titles/`  
Метод: `GET`

Пример ответа:
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```

Метод: `POST`

Пример запроса:
```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ],
  "category": {
    "name": "string",
    "slug": "^-$"
  }
}
```
Эндпоинт: `/api/v1/titles/{titles_id}/`

Метод: `GET`

Пример ответа:
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ],
  "category": {
    "name": "string",
    "slug": "^-$"
  }
}
```

Метод: `PATCH`

Пример запроса:
```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ],
  "category": {
    "name": "string",
    "slug": "^-$"
  }
}
```


Эндпоинт: `/api/v1/titles/{titles_id}/`

Метод: `DELETE`

### Категории

Эндпоинт: `/api/v1/categories/`  

Метод: `GET`

Пример ответа:
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ]
}
```

Метод: `POST`

Пример запроса:
```json
{
  "name": "string",
  "slug": "^-$"
}
```
Пример ответа:
```json
{
  "name": "string",
  "slug": "string"
}
```


Эндпоинт: `/api/v1/categories/{slug}`  

Метод: `DELETE`

### Жанры 

Эндпоинт: `/api/v1/genres/`  

Метод: `GET`

Пример ответа:
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ]
}
```

Метод: `POST`

Пример запроса:
```json
{
  "name": "string",
  "slug": "^-$"
}
```
Пример ответа:
```json
{
  "name": "string",
  "slug": "string"
}
```


Эндпоинт: `/api/v1/genres/{slug}`

Метод: `DELETE`


## Тестирование проекта через Postman

Для упрощения тестирования в проекте предусмотрен режим фиксированного кода подтверждения. 
Когда `USE_FIXED_CONFIRMATION_CODE = True` в настройках, всем пользователям будет отдаваться код '12345'.
Не забудьте установить `USE_FIXED_CONFIRMATION_CODE = False` перед развертыванием в продакшене!
