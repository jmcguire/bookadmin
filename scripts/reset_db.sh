#!/bin/bash

rm -f db.sqlite3
find books/migrations -name '0*.py' -delete

uv run python manage.py makemigrations
uv run python manage.py migrate
rm -rf .mypy_cache
uv run mypy books

DJANGO_SUPERUSER_PASSWORD=admin \
  uv run python manage.py createsuperuser \
  --noinput \
  --username admin \
  --email admin@localhost
