# 🔧 حل خطأ: cd: omantel: No such file or directory

## المشكلة
Render لا يجد مجلد `omantel` لأن المشروع موجود مباشرة في جذر repository على GitHub.

## ✅ الحل

تم تحديث `render.yaml` لإزالة `cd omantel &&` من جميع الأوامر.

### الخطوة 1: رفع التحديثات

```powershell
cd C:\Users\z97o\Desktop\project\omantel
$env:Path += ";C:\Program Files\Git\bin"
git add render.yaml
git commit -m "Fix: Remove cd omantel - project is in repo root"
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

### تحديث Build Command يدوياً في Render Dashboard

1. اذهب إلى Render Dashboard > Settings
2. ابحث عن **"Build Command"**
3. ضع (بدون `cd omantel`):
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && (python manage.py seed_from_excel --verbosity 2 || echo "Seed completed")
   ```
4. احفظ التغييرات

### تحديث Start Command

1. في نفس الصفحة، ابحث عن **"Start Command"**
2. ضع (بدون `cd omantel`):
   ```bash
   python -m gunicorn omantel.wsgi:application --bind 0.0.0.0:$PORT
   ```
3. احفظ التغييرات

### Root Directory

1. في Settings، ابحث عن **"Root Directory"**
2. اتركه **فارغاً تماماً**
3. احفظ التغييرات

---

## 📋 ملاحظات

- المشروع موجود مباشرة في جذر repository على GitHub
- لا حاجة لـ `cd omantel` لأن الملفات موجودة في الجذر
- `requirements.txt` موجود مباشرة في الجذر
- `manage.py` موجود مباشرة في الجذر

---

## ✅ بعد الإصلاح

1. انتظر اكتمال النشر (5-10 دقائق)
2. تحقق من Logs - يجب ألا ترى `No such file or directory`
3. افتح: https://omantel-netinsight.onrender.com
4. يجب أن يعمل الموقع الآن!

---

**ارفع التحديثات الآن! 🚀**
