# Reports API - Backend Service

Бэкенд сервис на FastAPI с JWT-аутентификацией и системой отчётов.

## Cтарт

### Требования
- Python 3.10+
- pip

### Установка

1. Клонируйте репозиторий:
```bash
git clone <your-repo-url>
cd FastAPI
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
```

3. Активируйте виртуальное окружение:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

5. (Опционально) Создайте файл `.env` на основе `.env.example`:
```bash
copy .env.example .env
```

6. Запустите сервер:
```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: http://127.0.0.1:8000

Интерактивная документация API: http://127.0.0.1:8000/docs

## Краткая структура проекта

```
FastAPI/
|-main.py              # Основной файл приложения
|-config.py            # Конфигурация и настройки
|-database.py          # Настройка подключения к БД
|-models.py            # SQLAlchemy модели (User, Report)
|-schemas.py           # Pydantic схемы для валидации
|-auth.py              # Логика аутентификации и JWT
|-routers/
|   |-auth.py          # Эндпоинты аутентификации
|   |-reports.py       # Эндпоинты для работы с отчётами
|-requirements.txt     # Зависимости проекта
|-.env.example         # Пример конфигурации
|-README.md            # Документация
```

Ниже описана более подробная структура проекта.

## Аутентификация

### Как это работает

Система аутентификации построена на **JWT (JSON Web Tokens)** и использует **OAuth2 с Bearer токенами**.

#### Поток аутентификации

1. **Регистрация**: `POST /auth/register`
   - Пароли хэшируются с использованием bcrypt
   - По умолчанию создаётся пользователь с ролью `staff`
   - Email и username должны быть уникальными

2. **Вход**: `POST /auth/login`
   - Возвращает JWT токен при успешной аутентификации
   - Токен действителен 30 минут (настраивается в `.env`)

3. **Использование токена**
   - Клиент добавляет токен в заголовок: `Authorization: Bearer <token>`
   - При каждом запросе к защищённым эндпоинтам вызывается `get_current_user()`

4. **Получение информации о текущем пользователе**: `GET /auth/me`
   - Требуется передать JWT токен в заголовке `Authorization: Bearer <token>`

#### Роли пользователей

- **admin** - администратор
  - Может видеть все отчёты в системе (`GET /reports`)
  - Полный доступ ко всем данным
  
- **staff** - обычный сотрудник
  - Может создавать отчёты
  - Видит только свои отчёты (`GET /reports` фильтрует по `user_id`)

#### Авторизация в эндпоинтах

В `routers/reports.py` реализована проверка прав доступа:

```python
# В GET /reports
if current_user.role == UserRole.staff:
    # staff видит только свои отчёты
    reports = db.query(Report).filter(Report.user_id == current_user.id).all()
else:
    # admin видит все отчёты
    reports = db.query(Report).all()
```

### Создание администратора

#### Вариант 1: Через API при регистрации

![alt text](/images/admin_reg.png)

Ответ:


![alt text](/images/admin_reg_res.png)

#### Вариант 2: Вручную через скрипт (для продакшена)

Используем файл `create_admin.py`:

```python
from database import SessionLocal
from models import User, UserRole
from auth import get_password_hash

db = SessionLocal()
admin = User(
    username="admin",
    email="admin@company.com",
    hashed_password=get_password_hash("secure_password"),
    role=UserRole.admin
)
db.add(admin)
db.commit()
print("Admin created successfully!")
```

Запустите: `python create_admin.py`

Админ будет создан, можем это проверить использовав API:

Авторизация (username:admin, password:secure_password):
![alt text](/images/admin_check1.png)

Проверка с помощью ендпоинта `/auth/me`:
![alt text](/images/admin_check2.png)

## API Эндпоинты

### Аутентификация

| Метод | URL | Описание | Требует Auth |
|-------|-----|----------|--------------|
| POST | /auth/register | Регистрация нового пользователя | Нет |
| POST | /auth/login | Вход и получение JWT токена | Нет |
| GET | /auth/me | Информация о текущем пользователе | Да |

### Отчёты

| Метод | URL | Описание | Требует Auth |
|-------|-----|----------|--------------|
| POST | /reports | Создание нового отчёта | Да |
| GET | /reports | Получение списка отчётов | Да |

## База данных

По умолчанию используется **SQLite** (`app.db`).

### Таблицы

**users**
- `id` - первичный ключ
- `username` - уникальное имя пользователя
- `email` - уникальный email
- `hashed_password` - хэшированный пароль
- `role` - роль (admin/staff)
- `created_at` - время создания

**reports**
- `id` - первичный ключ
- `category` - категория отчёта
- `message` - текст отчёта (не может быть пустым)
- `user_id` - автор отчёта (FK на users)
- `created_at` - время создания

## Примеры использования

### 1. Регистрация пользователя
![alt text](/images/staff_reg.png)

Ответ:
![alt text](/images/staff_reg_res.png)

### 2. Вход в систему
![alt text](/images/login.png)

Ответ:
![alt text](/images/login_res.png)

### 3. Создание отчёта
![alt text](/images/post_report.png)

Ответ:
![alt text](/images/post_report_res.png)

### 4. Получение отчётов
![alt text](/images/get_reports.png)

## Технологии, которые я использовал

- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - валидация данных
- **python-jose** - работа с JWT
- **passlib** - хэширование паролей
- **uvicorn** - ASGI сервер
