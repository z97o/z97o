# 🔧 حل خطأ: gunicorn: command not found

## المشكلة
Render لا يجد أمر `gunicorn` رغم أنه موجود في `requirements.txt`.

## ✅ الحل

تم تحديث `render.yaml` لاستخدام `python -m gunicorn` بدلاً من `gunicorn` مباشرة.

### الخطوة 1: رفع التحديثات

```powershell
cd C:\Users\z97o\Desktop\project\omantel
$env:Path += ";C:\Program Files\Git\bin"
git add render.yaml
git commit -m "Fix gunicorn command: Use python -m gunicorn"
git push
```

### الخطوة 2: إعادة النشر

Render سيكتشف التحديثات تلقائياً ويعيد النشر.

أو يدوياً:
1. اذهب إلى Render Dashboard
2. اضغط على الخدمة
3. اضغط **"Manual Deploy"** > **"Deploy latest commit"**

---

## 🔍 إذا استمر الخطأ

### تحديث Start Command يدوياً في Render Dashboard

1. اذهب إلى Render Dashboard > Settings
2. ابحث عن **"Start Command"**
3. ضع: `python -m gunicorn omantel.wsgi:application --bind 0.0.0.0:$PORT`
4. احفظ التغييرات

---

## 📋 ملاحظات

- `python -m gunicorn` يستخدم gunicorn كـ module بدلاً من command
- `--bind 0.0.0.0:$PORT` يخبر gunicorn بالاستماع على المنفذ الصحيح
- `$PORT` متغير بيئة توفره Render تلقائياً

---

## ✅ بعد الإصلاح

1. انتظر اكتمال النشر (5-10 دقائق)
2. تحقق من Logs - يجب ألا ترى `command not found`
3. افتح: https://omantel-netinsight.onrender.com
4. يجب أن يعمل الموقع الآن!

---

**ارفع التحديثات الآن! 🚀**
