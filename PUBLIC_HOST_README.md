# تشغيل السيرفر على Public Host

تم تحديث الإعدادات لجعل التطبيق متاحًا على host عام بدلاً من localhost فقط.

## التغييرات التي تمت:

1. ✅ تحديث `ALLOWED_HOSTS` في `settings.py` لقبول جميع الـ hosts
2. ✅ إضافة دعم متغيرات البيئة للإعدادات
3. ✅ إنشاء سكريبتات لتشغيل السيرفر على 0.0.0.0

## طرق التشغيل:

### الطريقة 1: استخدام السكريبتات الجاهزة

**على Windows:**
```bash
cd omantel
run_public.bat
```

**على Linux/Mac:**
```bash
cd omantel
chmod +x run_public.sh
./run_public.sh
```

**أو استخدام Python مباشرة:**
```bash
cd omantel
python run_public.py
```

### الطريقة 2: استخدام Django مباشرة

```bash
cd omantel
python manage.py runserver 0.0.0.0:8000
```

## الوصول للتطبيق:

بعد تشغيل السيرفر، يمكن الوصول للتطبيق من:

1. **من نفس الجهاز:**
   - http://localhost:8000
   - http://127.0.0.1:8000

2. **من أجهزة أخرى على نفس الشبكة:**
   - http://YOUR_IP_ADDRESS:8000
   
   **للعثور على عنوان IP الخاص بك:**
   - Windows: `ipconfig` (ابحث عن IPv4 Address)
   - Linux/Mac: `ifconfig` أو `ip addr`

## ملاحظات الأمان:

⚠️ **للإنتاج (Production):**
- قم بتعيين `DEBUG = False` في `settings.py`
- حدد `ALLOWED_HOSTS` بدقة بدلاً من `["*"]`
- استخدم HTTPS
- قم بتغيير `SECRET_KEY`

**مثال للإنتاج:**
```python
DEBUG = False
ALLOWED_HOSTS = ["your-domain.com", "www.your-domain.com"]
```

## استخدام متغيرات البيئة:

يمكنك استخدام متغيرات البيئة لتخصيص الإعدادات:

```bash
# Windows PowerShell
$env:DEBUG="False"
$env:ALLOWED_HOSTS="your-domain.com,www.your-domain.com"
$env:SECRET_KEY="your-secret-key-here"

# Linux/Mac
export DEBUG=False
export ALLOWED_HOSTS="your-domain.com,www.your-domain.com"
export SECRET_KEY="your-secret-key-here"
```

## استكشاف الأخطاء:

إذا واجهت مشاكل في الوصول:

1. تأكد من أن السيرفر يعمل على `0.0.0.0:8000` وليس `127.0.0.1:8000`
2. تحقق من إعدادات الجدار الناري (Firewall) - قد تحتاج لفتح المنفذ 8000
3. تأكد من أن جميع الأجهزة على نفس الشبكة
4. تحقق من `ALLOWED_HOSTS` في `settings.py`
