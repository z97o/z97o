# 🚀 دليل إعداد Git و GitHub

دليل سريع لإعداد المشروع على GitHub.

## الخطوة 1: تهيئة Git

```bash
cd omantel
git init
```

## الخطوة 2: إضافة الملفات

```bash
git add .
git commit -m "Initial commit: Omantel NetInsight project"
```

## الخطوة 3: إنشاء Repository على GitHub

1. اذهب إلى https://github.com/new
2. اختر اسم للمشروع (مثلاً: `omantel-netinsight`)
3. **لا** تضع علامة على "Initialize with README" (موجود بالفعل)
4. اضغط "Create repository"

## الخطوة 4: ربط المشروع بـ GitHub

```bash
# استبدل YOUR_USERNAME و YOUR_REPO_NAME بالقيم الصحيحة
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## الخطوة 5: التحقق

اذهب إلى repository على GitHub وتأكد من أن جميع الملفات موجودة.

## 🔄 العمل اليومي

### إضافة تغييرات جديدة:

```bash
git add .
git commit -m "وصف التغييرات"
git push
```

### سحب آخر التحديثات:

```bash
git pull
```

### إنشاء branch جديد:

```bash
git checkout -b feature/new-feature
# اعمل التغييرات
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

## ⚠️ ملاحظات مهمة

- **لا ترفع** ملفات حساسة (`.env`, `db.sqlite3`)
- **تحقق** من `.gitignore` قبل الرفع
- **استخدم** commit messages واضحة ووصفية

## 🔐 GitHub Secrets (للـ Deployment)

إذا كنت تستخدم Render أو أي خدمة deployment:

1. اذهب إلى: Settings > Secrets and variables > Actions
2. أضف:
   - `RENDER_API_KEY`
   - `RENDER_SERVICE_ID`

## 📚 المزيد من المعلومات

راجع [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) للتفاصيل الكاملة عن الـ deployment.
