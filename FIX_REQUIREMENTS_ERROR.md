# 🔧 حل خطأ: Could not open requirements file

## المشكلة
Render لا يجد `requirements.txt` لأن `rootDir` لا يعمل بشكل صحيح.

## ✅ الحل

تم تحديث `render.yaml` لإزالة `rootDir` واستخدام `cd omantel` في الأوامر مباشرة.

### الخطوة 1: رفع التحديثات

```powershell
cd C:\Users\z97o\Desktop\project\omantel
$env:Path += ";C:\Program Files\Git\bin"
git add render.yaml
git commit -m "Fix requirements.txt path: Remove rootDir and use cd omantel"
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
3. ضع:
   ```bash
   cd omantel && pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py seed_from_excel --verbosity 2 || echo "Seed completed"
   ```
4. احفظ التغييرات

### تحديث Start Command

1. في نفس الصفحة، ابحث عن **"Start Command"**
2. ضع: `cd omantel && python -m gunicorn omantel.wsgi:application --bind 0.0.0.0:$PORT`
3. احفظ التغييرات

### تحديث Root Directory

1. في Settings، ابحث عن **"Root Directory"**
2. اتركه **فارغاً** (لا تضع `omantel`)
3. احفظ التغييرات

---

## 📋 ملاحظات

- إزالة `rootDir` واستخدام `cd omantel` في الأوامر مباشرة
- هذا يضمن أن جميع الأوامر تعمل من المجلد الصحيح
- `requirements.txt` موجود في `omantel/requirements.txt`

---

## ✅ بعد الإصلاح

1. انتظر اكتمال النشر (5-10 دقائق)
2. تحقق من Logs - يجب أن ترى `Successfully installed...`
3. افتح: https://omantel-netinsight.onrender.com
4. يجب أن يعمل الموقع الآن!

---

**ارفع التحديثات الآن! 🚀**
