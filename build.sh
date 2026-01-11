#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "=== BUILD START ==="
pwd
ls -la
ls -la data || true

pip install -r requirements.txt
python manage.py migrate

echo "=== SEED START ==="
python manage.py seed_from_excel --verbosity 2 || true
echo "=== SEED END ==="

python manage.py collectstatic --noinput
echo "=== BUILD END ==="
