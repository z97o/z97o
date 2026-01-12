# 🚀 نشر الموقع على Render - دليل شامل

دليل خطوة بخطوة لنشر موقع Omantel NetInsight على Render.

## 📋 المتطلبات

- ✅ حساب GitHub (لديك: z97o)
- ✅ المشروع على GitHub (لديك: https://github.com/z97o/z97o)
- ✅ حساب Render (مجاني)

---

## 🎯 الخطوات

### الخطوة 1: إنشاء حساب على Render

1. اذهب إلى: **https://render.com**
2. اضغط **"Get Started for Free"**
3. اختر **"Sign up with GitHub"**
4. سجّل دخول بحساب GitHub الخاص بك
5. امنح Render الصلاحيات المطلوبة

---

### الخطوة 2: إنشاء Web Service جديد

1. في Render Dashboard، اضغط **"New +"**
2. اختر **"Web Service"**
3. اختر **"Connect GitHub repository"**
4. ابحث عن repository: **`z97o/z97o`**
5. اضغط **"Connect"**

---

### الخطوة 3: إعداد الخدمة

Render سيكتشف `render.yaml` تلقائياً ويقترح الإعدادات.

**تأكد من:**
- ✅ **Name**: `omantel-netinsight` (أو أي اسم تريده)
- ✅ **Region**: اختر الأقرب لك (مثلاً: Singapore)
- ✅ **Branch**: `main`
- ✅ **Root Directory**: اتركه فارغاً (أو `omantel` إذا كان المشروع في مجلد فرعي)
- ✅ **Environment**: `Python 3`
- ✅ **Build Command**: سيتم ملؤه تلقائياً من `render.yaml`
- ✅ **Start Command**: سيتم ملؤه تلقائياً من `render.yaml`

---

### الخطوة 4: إعداد Environment Variables

في قسم **"Environment Variables"**، أضف المتغيرات التالية:

#### متغيرات مطلوبة:

1. **SECRET_KEY**
   - اضغط **"Add Environment Variable"**
   - Key: `SECRET_KEY`
   - Value: أنشئ مفتاح سري قوي
   - يمكنك استخدام هذا الأمر في PowerShell:
     ```powershell
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - أو استخدم: https://djecrety.ir/

2. **DEBUG**
   - Key: `DEBUG`
   - Value: `False`

3. **ALLOWED_HOSTS**
   - Key: `ALLOWED_HOSTS`
   - Value: اتركه فارغاً أولاً، Render سيضيفه تلقائياً بعد النشر
   - أو أضف: `omantel-netinsight.onrender.com` (استبدل بالاسم الذي اخترته)

#### متغيرات اختيارية:

4. **PYTHON_VERSION**
   - Key: `PYTHON_VERSION`
   - Value: `3.13.0`

---

### الخطوة 5: إعداد قاعدة البيانات (اختياري)

إذا كنت تريد قاعدة بيانات PostgreSQL:

1. في Render Dashboard، اضغط **"New +"**
2. اختر **"PostgreSQL"**
3. اختر الخطة المجانية
4. بعد الإنشاء، Render سيعطيك:
   - `DATABASE_URL`
5. أضف في Environment Variables:
   - Key: `DATABASE_URL`
   - Value: (سيتم ملؤه تلقائياً)

**ملاحظة:** المشروع يستخدم SQLite افتراضياً، وهذا يعمل على Render أيضاً.

---

### الخطوة 6: النشر

1. راجع جميع الإعدادات
2. اضغط **"Create Web Service"**
3. Render سيبدأ في البناء والنشر
4. انتظر حتى يكتمل البناء (قد يستغرق 5-10 دقائق)

---

### الخطوة 7: الحصول على الرابط

بعد اكتمال النشر:

1. في صفحة الخدمة، ستجد **"URL"**
2. الرابط سيكون مثل: `https://omantel-netinsight.onrender.com`
3. اضغط على الرابط لفتح الموقع

---

## 🔧 تحديث ALLOWED_HOSTS بعد النشر

بعد الحصول على الرابط:

1. اذهب إلى Environment Variables في Render
2. حدّث `ALLOWED_HOSTS`:
   - Value: `omantel-netinsight.onrender.com` (استبدل بالرابط الفعلي)
3. احفظ التغييرات
4. Render سيعيد تشغيل الخدمة تلقائياً

---

## ✅ التحقق من النشر

بعد النشر الناجح:

1. ✅ افتح الرابط في المتصفح
2. ✅ يجب أن ترى الموقع يعمل
3. ✅ تحقق من أن HTTPS يعمل (Render يوفر HTTPS تلقائياً)

---

## 🔄 تحديث الموقع

عندما تقوم بتحديثات:

1. ارفع التغييرات إلى GitHub:
   ```powershell
   git add .
   git commit -m "Update site"
   git push
   ```

2. Render سيكتشف التغييرات تلقائياً ويعيد النشر

أو يمكنك:

1. اذهب إلى Render Dashboard
2. اضغط على الخدمة
3. اضغط **"Manual Deploy"** > **"Deploy latest commit"**

---

## 🛠️ استكشاف الأخطاء

### خطأ: "Build failed"

- تحقق من `requirements.txt`
- تحقق من logs في Render Dashboard
- تأكد من أن Python version صحيح

### خطأ: "Application error"

- تحقق من Environment Variables
- تحقق من `ALLOWED_HOSTS`
- راجع logs في Render Dashboard

### الموقع بطيء في التحميل الأول

- هذا طبيعي على الخطة المجانية
- Render يوقف الخدمة بعد 15 دقيقة من عدم الاستخدام
- التحميل الأول بعد التوقف قد يستغرق 30-60 ثانية

---

## 📝 ملخص Environment Variables

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=omantel-netinsight.onrender.com
PYTHON_VERSION=3.13.0
```

---

## 🎉 جاهز!

بعد النشر، سيكون موقعك متاحاً على:
**https://omantel-netinsight.onrender.com**

(استبدل بالرابط الفعلي الذي يعطيك إياه Render)

---

## 📞 المساعدة

إذا واجهت مشاكل:
1. راجع logs في Render Dashboard
2. تحقق من Environment Variables
3. تأكد من أن الكود على GitHub محدث

**جاهز للنشر! 🚀**
