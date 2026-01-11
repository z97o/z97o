#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py migrate

# Seed once (won't crash deploy if already seeded)
python manage.py seed_from_excel || true

python manage.py collectstatic --noinput
