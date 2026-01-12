# إعداد GitHub للـ Deployment

هذا الدليل يشرح كيفية إعداد المشروع على GitHub ونشره.

## 📋 المتطلبات

- حساب GitHub
- Git مثبت على جهازك
- Python 3.11+ مثبت

## 🚀 الخطوات

### 1. إنشاء Repository على GitHub

1. اذهب إلى [GitHub](https://github.com) وأنشئ repository جديد
2. اختر اسم للمشروع (مثلاً: `omantel-netinsight`)
3. لا تقم بتهيئة README أو .gitignore (موجود بالفعل)

### 2. ربط المشروع المحلي بـ GitHub

افتح Terminal في مجلد المشروع وقم بتنفيذ:

```bash
cd omantel

# تهيئة Git (إذا لم تكن مهيأ)
git init

# إضافة جميع الملفات
git add .

# عمل commit أولي
git commit -m "Initial commit: Omantel NetInsight project"

# إضافة remote repository (استبدل YOUR_USERNAME و YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# رفع الكود
git branch -M main
git push -u origin main
```

### 3. إعداد GitHub Secrets (للـ Deployment)

إذا كنت تستخدم Render أو أي خدمة deployment أخرى:

1. اذهب إلى Settings > Secrets and variables > Actions
2. أضف الـ Secrets التالية:
   - `RENDER_API_KEY`: مفتاح API من Render
   - `RENDER_SERVICE_ID`: معرف الخدمة من Render

### 4. إعداد Render للـ Deployment من GitHub

1. اذهب إلى [Render Dashboard](https://dashboard.render.com)
2. أنشئ Web Service جديد
3. اختر "Connect GitHub repository"
4. اختر repository الخاص بك
5. Render سيكتشف `render.yaml` تلقائياً

### 5. إعداد Environment Variables على Render

في Render Dashboard، أضف المتغيرات التالية:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
PYTHON_VERSION=3.13.0
```

## 🔄 GitHub Actions

تم إعداد GitHub Actions تلقائياً:

- **CI Workflow** (`ci.yml`): يعمل على كل push/PR للتحقق من الكود
- **Deploy Workflow** (`deploy.yml`): يعمل على push للـ main branch

### عرض نتائج Actions

1. اذهب إلى repository على GitHub
2. اضغط على تبويب "Actions"
3. ستجد جميع الـ workflows والنتائج

## 📝 ملفات GitHub المهمة

- `.github/workflows/ci.yml` - للاختبارات التلقائية
- `.github/workflows/deploy.yml` - للـ deployment التلقائي
- `render.yaml` - إعدادات Render للـ deployment

## 🔐 الأمان

⚠️ **مهم جداً:**

1. **لا ترفع ملف `.env`** - يحتوي على معلومات حساسة
2. **لا ترفع `db.sqlite3`** - قاعدة البيانات موجودة في `.gitignore`
3. **استخدم GitHub Secrets** للمعلومات الحساسة
4. **غير `SECRET_KEY`** في الإنتاج

## 🛠️ أوامر Git المفيدة

```bash
# عرض حالة الملفات
git status

# إضافة ملفات
git add .

# عمل commit
git commit -m "وصف التغييرات"

# رفع التغييرات
git push

# سحب آخر التحديثات
git pull

# إنشاء branch جديد
git checkout -b feature/new-feature

# عرض الفروع
git branch
```

## 🌐 خيارات Deployment الأخرى

بالإضافة لـ Render، يمكنك استخدام:

1. **Railway**: https://railway.app
2. **Heroku**: https://heroku.com
3. **Fly.io**: https://fly.io
4. **DigitalOcean App Platform**: https://www.digitalocean.com/products/app-platform

## 📞 الدعم

إذا واجهت مشاكل:
1. تحقق من logs في GitHub Actions
2. تحقق من logs في خدمة الـ deployment
3. تأكد من أن جميع Environment Variables مضبوطة بشكل صحيح
