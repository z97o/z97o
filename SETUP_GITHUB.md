# 🚀 دليل إعداد GitHub - خطوة بخطوة

## الخطوة 1: تثبيت Git (إذا لم يكن مثبتاً)

### على Windows:

1. اذهب إلى: https://git-scm.com/download/win
2. حمّل Git for Windows
3. شغّل المثبت واتبع التعليمات
4. اختر "Git from the command line and also from 3rd-party software"
5. بعد التثبيت، أعد فتح Terminal/PowerShell

### التحقق من التثبيت:

```powershell
git --version
```

يجب أن ترى شيئاً مثل: `git version 2.x.x`

---

## الخطوة 2: إعداد Git (للمرة الأولى فقط)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## الخطوة 3: إنشاء Repository على GitHub

1. اذهب إلى: https://github.com/new
2. أدخل اسم المشروع (مثلاً: `omantel-netinsight`)
3. اختر Public أو Private
4. **⚠️ مهم: لا تضع علامة على "Initialize with README"**
5. اضغط "Create repository"

---

## الخطوة 4: تهيئة المشروع المحلي

افتح PowerShell في مجلد `omantel` وقم بتنفيذ:

```powershell
# الانتقال لمجلد المشروع
cd C:\Users\z97o\Desktop\project\omantel

# تهيئة Git
git init

# إضافة جميع الملفات
git add .

# عمل commit أولي
git commit -m "Initial commit: Omantel NetInsight project"
```

---

## الخطوة 5: ربط المشروع بـ GitHub

```powershell
# استبدل YOUR_USERNAME و YOUR_REPO_NAME بالقيم الصحيحة
# مثال: git remote add origin https://github.com/ahmed/omantel-netinsight.git
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# تغيير اسم الفرع الرئيسي إلى main
git branch -M main

# رفع الكود
git push -u origin main
```

**ملاحظة:** سيطلب منك GitHub اسم المستخدم وكلمة المرور (أو Personal Access Token)

---

## الخطوة 6: إعداد GitHub Personal Access Token

إذا طُلب منك token:

1. اذهب إلى: https://github.com/settings/tokens
2. اضغط "Generate new token" > "Generate new token (classic)"
3. اختر الصلاحيات:
   - ✅ `repo` (Full control of private repositories)
4. اضغط "Generate token"
5. **انسخ Token فوراً** (لن تتمكن من رؤيته مرة أخرى)
6. استخدمه ككلمة مرور عند `git push`

---

## الخطوة 7: التحقق من النجاح

اذهب إلى repository على GitHub وتأكد من:
- ✅ جميع الملفات موجودة
- ✅ README.md يظهر بشكل صحيح
- ✅ تبويب "Actions" يعمل (قد يستغرق دقيقة)

---

## 🔄 العمل اليومي مع Git

### إضافة تغييرات جديدة:

```powershell
cd C:\Users\z97o\Desktop\project\omantel
git add .
git commit -m "وصف التغييرات"
git push
```

### سحب آخر التحديثات:

```powershell
git pull
```

### عرض حالة الملفات:

```powershell
git status
```

---

## 🛠️ استكشاف الأخطاء

### خطأ: "fatal: not a git repository"
```powershell
git init
```

### خطأ: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### خطأ: "failed to push"
- تأكد من أن Token صحيح
- تأكد من أن Repository موجود على GitHub
- جرب: `git push -u origin main --force` (بحذر!)

---

## 📝 مثال كامل

```powershell
# 1. الانتقال للمجلد
cd C:\Users\z97o\Desktop\project\omantel

# 2. تهيئة Git
git init

# 3. إضافة الملفات
git add .

# 4. Commit
git commit -m "Initial commit: Omantel NetInsight project"

# 5. ربط بـ GitHub (استبدل بالقيم الصحيحة)
git remote add origin https://github.com/YOUR_USERNAME/omantel-netinsight.git

# 6. رفع الكود
git branch -M main
git push -u origin main
```

---

## ✅ بعد الرفع الناجح

1. اذهب إلى repository على GitHub
2. تحقق من تبويب "Actions" - يجب أن ترى workflows تعمل
3. راجع `README.md` على GitHub
4. جاهز! 🎉

---

## 🔐 إعداد GitHub Secrets (للـ Deployment)

إذا كنت تريد استخدام GitHub Actions للـ deployment:

1. اذهب إلى: Settings > Secrets and variables > Actions
2. اضغط "New repository secret"
3. أضف:
   - Name: `RENDER_API_KEY`
   - Value: [مفتاح API من Render]
4. أضف:
   - Name: `RENDER_SERVICE_ID`
   - Value: [معرف الخدمة من Render]

---

## 📞 المساعدة

إذا واجهت أي مشاكل:
1. تحقق من أن Git مثبت: `git --version`
2. تحقق من الاتصال: `git remote -v`
3. راجع الأخطاء في Terminal

**جاهز للبدء! 🚀**
