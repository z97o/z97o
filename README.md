# Omantel NetInsight Dashboard

نظام إدارة وتحليل البيانات لشبكة Omantel.

## 🚀 المميزات

- لوحة تحكم شاملة لمراقبة الشبكة
- إدارة الشكاوى (Complaints Management)
- تحليل البيانات الإقليمية
- خرائط تفاعلية للأبراج
- تقارير KPI مفصلة

## 📋 المتطلبات

- Python 3.11+
- Django 5.2+
- SQLite (للتنمية) / PostgreSQL (للإنتاج)

## 🛠️ التثبيت

### 1. استنساخ المشروع

```bash
git clone https://github.com/YOUR_USERNAME/omantel-netinsight.git
cd omantel-netinsight/omantel
```

### 2. إنشاء Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 4. إعداد قاعدة البيانات

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. تحميل البيانات (اختياري)

```bash
python manage.py seed_from_excel --verbosity 2
```

### 6. تشغيل السيرفر

```bash
# للتطوير المحلي
python manage.py runserver

# للوصول العام (من أجهزة أخرى على الشبكة)
python manage.py runserver 0.0.0.0:8000
# أو استخدم
run_public.bat  # Windows
./run_public.sh  # Linux/Mac
```

## 🌐 الوصول للتطبيق

- **محلي**: http://localhost:8000
- **شبكة**: http://YOUR_IP_ADDRESS:8000

## 📁 هيكل المشروع

```
omantel/
├── api/              # API endpoints
├── complaints/       # إدارة الشكاوى
├── core/            # النماذج الأساسية
├── dashboard/       # لوحة التحكم الرئيسية
├── regions/         # البيانات الإقليمية
├── towers/           # إدارة الأبراج
├── data/            # ملفات البيانات
├── static/          # الملفات الثابتة
└── templates/       # قوالب HTML
```

## 🔧 الإعدادات

يمكنك تخصيص الإعدادات عبر متغيرات البيئة:

```bash
# Windows PowerShell
$env:SECRET_KEY="your-secret-key"
$env:DEBUG="False"
$env:ALLOWED_HOSTS="your-domain.com"

# Linux/Mac
export SECRET_KEY="your-secret-key"
export DEBUG="False"
export ALLOWED_HOSTS="your-domain.com"
```

## 🚀 النشر على GitHub

راجع ملف [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) للتعليمات الكاملة.

### خطوات سريعة:

1. إنشاء repository على GitHub
2. ربط المشروع المحلي:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
3. إعداد GitHub Secrets (للـ deployment)
4. ربط مع Render أو أي خدمة deployment

## 📚 الوثائق

- [تشغيل على Public Host](PUBLIC_HOST_README.md)
- [إعداد GitHub للـ Deployment](GITHUB_DEPLOYMENT.md)

## 🔐 الأمان

⚠️ **للإنتاج:**
- قم بتعيين `DEBUG = False`
- استخدم `SECRET_KEY` قوي
- حدد `ALLOWED_HOSTS` بدقة
- استخدم HTTPS
- استخدم قاعدة بيانات آمنة (PostgreSQL)

## 📝 الترخيص

هذا المشروع مخصص لاستخدام Omantel.

## 👥 المساهمون

- فريق تطوير Omantel NetInsight

## 📞 الدعم

للأسئلة والدعم، يرجى فتح issue على GitHub.
