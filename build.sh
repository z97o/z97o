#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput

# لازم المايقريشن ينجح، لأنه أساس التشغيل
python manage.py migrate

# هذي لا تخلي الديبلوي يفشل لو صار خطأ
python manage.py create_admin || true
python manage.py seed_from_excel || true
