# 🔧 حل مشكلة عدم ظهور الأبراج على Render

## المشكلة
الموقع على Render (https://omantel-netinsight.onrender.com) يظهر 0 أبراج لأن قاعدة البيانات فارغة.

## ✅ الحل

تم تحديث `render.yaml` لتحميل البيانات تلقائياً عند النشر.

### الخطوة 1: رفع التحديثات إلى GitHub

```powershell
cd C:\Users\z97o\Desktop\project\omantel
$env:Path += ";C:\Program Files\Git\bin"
git add render.yaml
git commit -m "Add data seeding to Render build"
git push
```

### الخطوة 2: إعادة النشر على Render

Render سيكتشف التحديثات تلقائياً ويعيد النشر. أو:

1. اذهب إلى [Render Dashboard](https://dashboard.render.com)
2. اضغط على الخدمة `omantel-netinsight`
3. اضغط **"Manual Deploy"** > **"Deploy latest commit"**

### الخطوة 3: انتظار اكتمال النشر

- قد يستغرق 5-10 دقائق
- راقب Logs للتأكد من نجاح `seed_from_excel`

---

## 🔍 التحقق من Logs على Render

1. اذهب إلى Render Dashboard
2. اضغط على الخدمة
3. اذهب إلى تبويب **"Logs"**
4. ابحث عن:
   - `Importing sheet: Infrastructure`
   - `Imported/updated X towers`

---

## 🛠️ إذا لم تعمل تلقائياً

### الحل البديل: تحميل البيانات يدوياً

يمكنك استخدام Render Shell:

1. في Render Dashboard، اضغط على الخدمة
2. اضغط **"Shell"** (في القائمة الجانبية)
3. نفّذ:
   ```bash
   python manage.py seed_from_excel --verbosity 2
   ```

أو استخدم Render API/CLI.

---

## 📋 ملاحظات

- `seed_from_excel` يحتاج ملف Excel في `data/NetInsight_Large_Detailed_Dataset.xlsx`
- تأكد من أن الملف موجود في GitHub repository
- إذا لم يكن موجوداً، سيتم تخطي التحميل (بفضل `|| echo`)

---

## ✅ بعد النشر

1. انتظر اكتمال النشر
2. افتح: https://omantel-netinsight.onrender.com
3. يجب أن ترى الأبراج الآن!

---

**ارفع التحديثات إلى GitHub الآن! 🚀**
