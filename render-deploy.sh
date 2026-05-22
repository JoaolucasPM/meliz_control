#!/bin/bash
set -e

echo "Sincronizando Alembic..."
flask --app src.app db stamp head || true

echo "Aplicando migrations..."
flask --app src.app db upgrade

echo "Iniciando aplicação..."
gunicorn --workers 1 --threads 2 src.wsgi:app