University API (FastAPI + PostgreSQL)

Проект по БД: предметная область Университет.
Таблицы: teacher, subject, lesson.
Реализовано REST API с CRUD, пагинацией, JOIN/WHERE/SORT/GROUP BY/UPDATE запросами, а также JSONB + regex + pg_trgm/GIN.

============================================================
Требования
- Docker
- Python 3.6+
- pip / venv
============================================================

1) Поднять PostgreSQL в Docker

docker run -d --name postgres_anatoly \
  -e POSTGRES_USER=anatoly \
  -e POSTGRES_PASSWORD=anatoly \
  -e POSTGRES_DB=postgres \
  -p 5410:5432 \
  postgres:14


2) Инициализация БД (создать пользователя/БД/таблицы)

Запуск init-скрипта:
bash scripts/db_init.sh


3) Установка зависимостей

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


4) Запуск API

source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000


5) Заполнение БД тестовыми данными (через REST API)

1) Запустить API
2) В другом терминале:

source .venv/bin/activate
python scripts/fill_db.py


Основные эндпоинты

CRUD + пагинация:
- GET /teachers?limit=20&offset=0
- GET /subjects?limit=20&offset=0
- GET /lessons?limit=20&offset=0

JOIN:
- GET /lessons/detailed?limit=...&offset=...

WHERE + сортировка параметром:
- GET /lessons/search?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD&gruppa=...&auditoriya=...&sort_by=data&sort_dir=desc

GROUP BY:
- GET /teachers/stats/lessons-count

UPDATE с условием:
- PATCH /subjects/bulk/mark-nonmandatory?min_hours=50

Regex поиск:
- GET /teachers/search/regex?pattern=...

JSONB поиск по meta:
- GET /lessons/by-meta?key=note&value=test