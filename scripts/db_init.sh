#!/usr/bin/env bash
set -euo pipefail

CONTAINER="postgres_anatoly"
ADMIN_USER="anatoly"
ADMIN_DB="postgres"

DB_NAME="university_db"
APP_USER="university_app"
APP_PASS="university_pass"

docker exec -i "$CONTAINER" psql -U "$ADMIN_USER" -d "$ADMIN_DB" <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$APP_USER') THEN
    CREATE ROLE $APP_USER LOGIN PASSWORD '$APP_PASS';
  END IF;
END;
\$\$;
SQL

if ! docker exec -i "$CONTAINER" psql -U "$ADMIN_USER" -d "$ADMIN_DB" -tAc \
  "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1; then
  docker exec -i "$CONTAINER" psql -U "$ADMIN_USER" -d "$ADMIN_DB" -c \
    "CREATE DATABASE $DB_NAME OWNER $APP_USER;"
fi

docker exec -i "$CONTAINER" psql -U "$ADMIN_USER" -d "$ADMIN_DB" -c \
  "ALTER DATABASE $DB_NAME OWNER TO $APP_USER;"

docker exec -i "$CONTAINER" psql -U "$ADMIN_USER" -d "$DB_NAME" <<SQL
CREATE TABLE IF NOT EXISTS teacher (
  id BIGSERIAL PRIMARY KEY,
  fio TEXT NOT NULL,
  kafedra TEXT NOT NULL,
  dolzhnost TEXT NOT NULL,
  uch_stepen TEXT
);

CREATE TABLE IF NOT EXISTS subject (
  id BIGSERIAL PRIMARY KEY,
  nazvanie TEXT NOT NULL UNIQUE,
  chislo_chasov INT NOT NULL CHECK (chislo_chasov > 0),
  vid_proverki TEXT NOT NULL,
  obyazatelnost BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS lesson (
  id BIGSERIAL PRIMARY KEY,
  teacher_id BIGINT NOT NULL REFERENCES teacher(id) ON DELETE RESTRICT,
  subject_id BIGINT NOT NULL REFERENCES subject(id) ON DELETE RESTRICT,
  data DATE NOT NULL,
  vremya TIME NOT NULL,
  auditoriya TEXT NOT NULL,
  vid_zanyatiya TEXT NOT NULL,
  gruppa TEXT NOT NULL
);

ALTER TABLE teacher OWNER TO $APP_USER;
ALTER TABLE subject OWNER TO $APP_USER;
ALTER TABLE lesson OWNER TO $APP_USER;
SQL
