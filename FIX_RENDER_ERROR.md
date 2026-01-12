# 🔧 حل خطأ Render: ModuleNotFoundError: No module named 'app'

## المشكلة

Render يحاول تشغيل `gunicorn app:app` لكن المشروع في مجلد فرعي `omantel`.

## ✅ الحل

تم تحديث `render.yaml` لإضافة `rootDir: omantel`.

### الخطوة 1: رفع التحديثات

```powershell
cd C:\Users\z97o\Desktop\project\omantel
$env:Path += ";C:\Program Files\Git\bin"
git add render.yaml
git commit -m "Fix Render: Add rootDir to render.yaml"
git push
```

### الخطوة 2: إعادة النشر

Render سيكتشف التحديثات تلقائياً ويعيد النشر.

أو يدوياً:
1. اذهب إلى Render Dashboard
2. اضغط على الخدمة
3. اضغط **"Manual Deploy"** > **"Deploy latest commit"**

---

## 🔍 التحقق من الإعدادات في Render Dashboard

إذا لم يعمل، تحقق من:

1. **Root Directory:** يجب أن يكون `omantel`
2. **Start Command:** يجب أن يكون `gunicorn omantel.wsgi:application`

### كيفية التحقق:

1. اذهب إلى Render Dashboard
2. اضغط على الخدمة `omantel-netinsight`
3. اذهب إلى **"Settings"**
4. تحقق من:
   - **Root Directory:** `omantel`
   - **Start Command:** `gunicorn omantel.wsgi:application`

---

## 🛠️ إذا استمر الخطأ

### الحل البديل: تحديث الإعدادات يدوياً

في Render Dashboard > Settings:

1. **Root Directory:** ضع `omantel`
2. **Start Command:** ضع `gunicorn omantel.wsgi:application`
3. احفظ التغييرات

---

## ✅ بعد الإصلاح

1. انتظر اكتمال النشر (5-10 دقائق)
2. تحقق من Logs للتأكد من عدم وجود أخطاء
3. افتح: https://omantel-netinsight.onrender.com
4. يجب أن يعمل الموقع الآن!

---

**ارفع التحديثات الآن! 🚀**
