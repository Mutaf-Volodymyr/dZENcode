# Comments for dZENcode

Этот проект реализован в качестве тестового задания dZENcode и предназначен для демонстрации HardSkills кандидата*. 
В проекте реализовано:
 - REST API для управления каскадных комментариев (с пагинацией, фильтрацией, правами и валидацией)
 - Рейтинги комментариев
 - templates для отображения ТОП комментариев в реальном времени (с автообновлением)
 - Аутентификация и верификация пользователя с помощью JWT
 - Фоновые задачи (события)
 - Кеширование
 - Авто-документация (redoc, swagger)

*Кандидат обладает скудными Front-End Skills и еще более скудными навыками дизайна, ввиду чего клиентская часть реализована очень плохо, что кандидат осознает.


## Технологии:
- Python
- Django
- DRF
- Celery
- Redis
- MySQL
- JWT
- WebSocket
- Docker
- Nginx

## Конечные точки
- `/` - templates c отображением комментариев в реальном времени (WebSocket)
- `admin/` - (админ панель не реализована)
- `api/v1/auth/login/` - (POST only) аутентификация
- `api/v1/auth/registration/` - (POST only) регистрация пользователя
- `api/v1/auth/password_update/` - (POST only) обновление пароля
- `api/v1/auth/logout/` - (POST only) выход
- `api/v1/docs/swagger/` - swagger
- `api/v1/docs/redoc/` - redoc
- `api/v1/comments/comments/` - (LIST/GET, POST)
- `api/v1/comments/comments/<int:pk>/` - (RETRIEVE/GET, PUT, PATCH)
- `api/v1/comments/comments/<int:pk>/like` - (POST only) поставить лайк
- `api/v1/comments/comments/<int:pk>/dislike` - (POST only) поставить дизлайк
- `api/v1/comments/comments/<int:pk>/neutral` - (POST only) сбросить оценку


## Установка и запуск проекта

1. Клонируйте репозиторий:

>git clone git@github.com:Mutaf-Volodymyr/dZENcode.git

2. Создайте `.env` по примеру `env.example`

3. Запустите Docker:

> docker-compose build

> docker-compose up -d



