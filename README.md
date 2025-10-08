
# Live Tracker

**Live Tracker** — backend-приложение для трекинга задач, созданное с использованием **FastAPI** и асинхронного подхода. 
Приложение обеспечивает авторизацию пользователей, управление задачами и разворачивается в Docker-контейнерах.

## 🚀 Основные возможности

- 🔐 JWT авторизация и регистрация пользователей
- ✅ CRUD-операции с задачами: добавление, удаление, редактирование и просмотр
- 🔒 Безопасное хранение паролей с хешированием
- 🐳 Запуск в изолированных Docker-контейнерах
- 📦 Все зависимости указаны в `requirements.txt`

## 📦 Установка и запуск

### ⚙️ Требования

- Python 3.10+
- Docker и Docker Compose
- Git

### 🔧 Шаги запуска

1. Клонировать репозиторий:

```bash
git clone https://github.com/boomb00xxx/live-tracker.git
cd live-tracker
````

2. Установить зависимости (опционально, для локального запуска без Docker):

```bash
pip install -r backend/requirements.txt
```

3. Создать файл `.env` в папке `backend` и указать там:

```env
DB_USER=user
DB_PASSWORD=password
DB_HOST=db
DB_PORT=port
DB_NAME=db_name


DEBUG=True/False
SECRET_KEY=your_secret_key
```

4. Собрать и запустить контейнеры:

```bash
docker-compose up --build
```

5. Инициализировать базу данных внутри контейнера:

```bash
docker exec -it backend-web-1 /bin/bash
cd ./src/db
python3 init_db.py
exit
```

6. Открыть index.html из папки frontend, либо открыть в браузере SwaggerUi:

[http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Тестирование

Тесты расположены в директории `backend/src/tests`.

Для запуска тестов:

```bash
cd backend
pytest -v -s
```

## 🧑‍💻 Контакты и поддержка

Автор проекта — [boomb00xxx](https://github.com/boomb00xxx)
