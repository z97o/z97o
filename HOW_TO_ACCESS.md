# 🌐 كيفية الوصول إلى الموقع

## الطريقة 1: تشغيل الموقع محلياً (على جهازك)

### الخطوة 1: تفعيل Virtual Environment

```powershell
cd C:\Users\z97o\Desktop\project\omantel
venv\Scripts\activate
```

### الخطوة 2: تشغيل السيرفر

**الطريقة السريعة:**
```powershell
.\start-site.bat
```

**أو يدوياً:**
```powershell
python manage.py runserver
```

### الخطوة 3: فتح الموقع

افتح المتصفح واذهب إلى:
- **http://localhost:8000**
- أو **http://127.0.0.1:8000**

---

## الطريقة 2: الوصول من أجهزة أخرى على نفس الشبكة

### الخطوة 1: تشغيل السيرفر على Public Host

```powershell
.\run_public.bat
```

أو:
```powershell
python manage.py runserver 0.0.0.0:8000
```

### الخطوة 2: معرفة عنوان IP الخاص بك

```powershell
ipconfig
```

ابحث عن **IPv4 Address** (مثلاً: `192.168.1.100`)

### الخطوة 3: الوصول من أجهزة أخرى

افتح المتصفح على الجهاز الآخر واذهب إلى:
- **http://YOUR_IP_ADDRESS:8000**
- مثال: `http://192.168.1.100:8000`

---

## الطريقة 3: نشر الموقع على الإنترنت (Production)

### استخدام Render (مجاني)

1. اذهب إلى: https://render.com
2. سجل دخول بحساب GitHub
3. اضغط "New" > "Web Service"
4. اختر repository: `z97o/z97o`
5. Render سيكتشف `render.yaml` تلقائياً
6. أضف Environment Variables:
   - `SECRET_KEY`: مفتاح سري
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app.onrender.com`
7. اضغط "Create Web Service"
8. بعد النشر، ستحصل على رابط مثل: `https://your-app.onrender.com`

### استخدام Railway

1. اذهب إلى: https://railway.app
2. سجل دخول بحساب GitHub
3. اضغط "New Project" > "Deploy from GitHub repo"
4. اختر repository
5. Railway سيكتشف Django تلقائياً
6. بعد النشر، ستحصل على رابط

---

## 🔧 استكشاف الأخطاء

### خطأ: "ModuleNotFoundError"

```powershell
# تأكد من تفعيل virtual environment
venv\Scripts\activate

# تثبيت المتطلبات
pip install -r requirements.txt
```

### خطأ: "No migrations to apply"

```powershell
python manage.py migrate
```

### خطأ: "Port 8000 already in use"

```powershell
# استخدم منفذ آخر
python manage.py runserver 8001
```

ثم افتح: http://localhost:8001

---

## 📝 ملخص سريع

**للوصول المحلي:**
```powershell
cd C:\Users\z97o\Desktop\project\omantel
venv\Scripts\activate
python manage.py runserver
# افتح: http://localhost:8000
```

**للوصول من أجهزة أخرى:**
```powershell
python manage.py runserver 0.0.0.0:8000
# استخدم: http://YOUR_IP:8000
```

---

## ✅ جاهز!

بعد تشغيل السيرفر، افتح المتصفح واذهب إلى **http://localhost:8000**
