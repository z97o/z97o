# ⚡ نشر سريع على Render

## الخطوات السريعة (5 دقائق)

### 1️⃣ سجّل دخول على Render
- اذهب: https://render.com
- اضغط "Sign up with GitHub"
- سجّل دخول بحساب GitHub

### 2️⃣ أنشئ Web Service
- اضغط "New +" > "Web Service"
- اختر "Connect GitHub repository"
- اختر: **z97o/z97o**
- اضغط "Connect"

### 3️⃣ أضف Environment Variables
في قسم "Environment Variables"، أضف:

```
SECRET_KEY = (أنشئ مفتاح سري - استخدم: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DEBUG = False
ALLOWED_HOSTS = (اتركه فارغاً أولاً، Render سيضيفه)
```

### 4️⃣ انشر
- اضغط "Create Web Service"
- انتظر 5-10 دقائق
- احصل على الرابط!

### 5️⃣ حدّث ALLOWED_HOSTS
بعد الحصول على الرابط (مثلاً: `https://omantel-netinsight.onrender.com`):
- اذهب إلى Environment Variables
- حدّث `ALLOWED_HOSTS` = `omantel-netinsight.onrender.com`
- احفظ

---

## ✅ جاهز!

موقعك الآن على الإنترنت! 🌐

---

**للمزيد من التفاصيل:** راجع [DEPLOY_RENDER.md](DEPLOY_RENDER.md)
