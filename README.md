# Платформа для публикации платного контента

## Описание проекта

Это платформа, на которой пользователи могут публиковать записи. Записи могут быть либо бесплатными (доступными для всех без регистрации), либо платными (доступными только авторизованным пользователям, оплатившим разовую подписку через Stripe).

## Функциональные возможности

- Регистрация и аутентификация пользователей по номеру телефона.
- Публикация бесплатных и платных записей.
- Оплата разовой подписки через Stripe для доступа к платным записям.
- CRUD операции для записей.
- Разграничение доступа к записям в зависимости от статуса подписки.

## Стек технологий

- Python
- Django
- PostgreSQL
- Docker
- Stripe

## Установка и настройка

### Предварительные требования

- Python 3.8+
- PostgreSQL
- Docker и Docker Compose

### Установка:
Клонируйте репрозиторий:
git clone https://github.com/EvgeniyKhan/post

### Создайте виртуальное окружение и активируйте его:
python -m venv env
source env/bin/activate (Для Windows используйте env\Scripts\activate)

### Установите зависимости:
pip install -r requirements.txt

Создайте файл .env с содержимым, который находится в файле .env_exmape
### Запуск проекта:
docker-compose up -d --build
