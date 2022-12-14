![example workflow](https://github.com/aakozlov85gmail/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Описание учебного проекта YaMDb

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Хранение логинов, паролей и иных секретных данных

- Все данные должны быть перенесены в .env файл, а так же этот файл необходимо
  отметить в файле .gitignore, что бы вышеупомянутые данные не попадали в общий
  доступ.
- Для заполнения .env файла используйте следующий шаблон:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных>
POSTGRES_USER=<пользователь базы данных>
POSTGRES_PASSWORD=<пароль пользователя>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<ключ шифрования данных Django>
```
## Запуск проекта

Для работы с проектом у вас должен быть установлен git, docker, docker-compose

### Процедура
- Склонируйте репозиторий к себе на компьютер.
- В консоли перейдите в папку проекта с файлом docker-compose.yaml и создайте в ней .env файл с логинами и паролями.
- Наберите команду `docker-compose up` и запускайте.
- Откройте второе окно консоли и дождитесь запуска проекта в первой.
- Наберите команду `docker-compose exec web python manage.py migrate` для запуска миграций.
- Наберите команду `docker-compose exec web python manage.py createsuperuser` и
  создайте суперпользователя.
- Наберите команду для копирования
  статики `docker-compose exec web python manage.py collectstatic --no-input`.

## Остановка проекта и удаление проекта

Для остановки проекта выполните команду:
`docker-compose stop`
Для остановки и удаления контейнеров выполните команду:
`docker-compose down -v`

## Доступ к административной консоли

- http://localhost/admin
- Выполните вход под ранее созданной учетной записью суперпользователя.

## Примеры работы с API для всех пользователей
Данный проект предоставляет возможность использования REST API для доступа к элементам базы данных. Документация с описанием возможных методов и доступных эндпойнтов представлена по адресу http://localhost/redoc и доступа после установки проекта. 

## Пользовательские роли

- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

- **Аутентифицированный пользователь** _(user)_ — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.

- **Модератор** _(moderator)_ — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.

- **Администратор** _(admin)_ — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

- **Суперюзер** Django должен всегда обладать правами администратора, пользователя с правами _admin_. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

## Самостоятельная регистрация новых пользователей

Пользователь отправляет POST-запрос с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.

Сервис YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на указанный адрес email.

Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).

### Примеры работы с API для авторизованных пользователей
Добавление категории:
```
POST http://localhost/api/v1/categories/
```
Удаление категории:
```
DELETE http://localhost/api/v1/categories/{slug}/
```
Добавление жанра:
```
POST http://localhost/api/v1/genres/
```
Удаление жанра:
```
DELETE http://localhost/api/v1/genres/{slug}/
```
Добавление произведения:
```
POST http://localhost/api/v1/titles/
```
Получение списка всех отзывов
```
GET http://localhost/api/v1/titles/{title_id}/reviews/
```
Добавление нового отзыва
```
POST http://localhost/api/v1/titles/{title_id}/reviews/
```
Полуение отзыва по id
```
GET/POST http://localhost/api/v1/titles/{title_id}/reviews/{review_id}/
```
Частичное обновление отзыва по id
```
PATCH http://localhost/api/v1/titles/{title_id}/reviews/{review_id}/
```
Удаление отзыва по id
```
DELETE http://localhost/api/v1/titles/{title_id}/reviews/{review_id}/
```

## Примеры API запросов и ответов

Запрос категорий:
```
GET http://localhost/api/v1/categories/
```
Пример ответа в JSON формате:
```
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "Фильмы",
            "slug": "films"
        },
        {
            "name": "Разное",
            "slug": "other"
        },
        {
            "name": "Мультфильмы",
            "slug": "multfilms"
        }
    ]
}
```
Запрос произведений:
```
GET http://localhost/api/v1/titles/
```
Пример ответа в JSON формате:
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Спасти рядового Райана",
            "year": 1998,
            "rating": null,
            "description": "Вторая мировая. Капитан Джон Миллер получает тяжелое задание. Вместе с отрядом из восьми человек он",
            "genre": [],
            "category": {
                "name": "Фильмы",
                "slug": "films"
            }
        },
        {
            "id": 2,
            "name": "Зверополис",
            "year": 2016,
            "rating": null,
            "description": "Отважная крольчиха делает карьеру в полиции звериного города. Оскароносная комедия с серьезным подте",
            "genre": [],
            "category": {
                "name": "Мультфильмы",
                "slug": "multfilms"
            }
        }
    ]
}
```
### Ознакомиться с тестовым проектом

Тестовый деплой проекта выполнен на сервере 51.250.21.181

## Автор

Козлов Андрей. Студент 31 когорты. Yandex-praktikum
