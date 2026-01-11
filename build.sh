#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "=== START BUILD.SH ==="
python --version
pwd
ls -la
ls -la data || true

pip install -r requirements.txt

echo "=== RUN MIGRATIONS ==="
python manage.py migrate

echo "=== RUN SEED_FROM_EXCEL ==="
python manage.py seed_from_excel --verbosity 2 || true

echo "=== COLLECTSTATIC ==="
python manage.py collectstatic --noinput

echo "=== END BUILD.SH ==="
