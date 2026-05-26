#!/bin/bash
set -e

flask --app src.app db upgrade

gunicorn --workers 1 src.wsgi:app