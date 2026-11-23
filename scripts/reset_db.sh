#!/bin/bash
set -e

rm -f db.sqlite3
find books/migrations -name '0*.py' -delete

uv run python manage.py makemigrations
uv run python manage.py migrate

DJANGO_SUPERUSER_PASSWORD=admin \
  uv run python manage.py createsuperuser \
  --noinput \
  --username admin \
  --email admin@localhost
