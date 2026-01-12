# ⚡ بدء سريع - إعداد GitHub

## 🎯 الخطوات السريعة

### 1️⃣ تثبيت Git

إذا لم يكن Git مثبتاً:
- **Windows**: حمّل من https://git-scm.com/download/win
- شغّل المثبت واتبع التعليمات
- أعد فتح PowerShell بعد التثبيت

### 2️⃣ إنشاء Repository على GitHub

1. اذهب إلى: https://github.com/new
2. أدخل اسم المشروع (مثلاً: `omantel-netinsight`)
3. **⚠️ لا تضع علامة على "Initialize with README"**
4. اضغط "Create repository"

### 3️⃣ تشغيل السكريبت التلقائي

```powershell
cd C:\Users\z97o\Desktop\project\omantel
.\setup-github.ps1
```

السكريبت سيقوم بـ:
- ✅ التحقق من Git
- ✅ تهيئة Repository
- ✅ إضافة الملفات
- ✅ ربط المشروع بـ GitHub

### 4️⃣ رفع الكود

بعد تشغيل السكريبت، نفّذ:

```powershell
git push -u origin main
```

**ملاحظة:** سيُطلب منك:
- اسم المستخدم على GitHub
- Personal Access Token (ككلمة مرور)

للحصول على Token: https://github.com/settings/tokens

---

## 🔄 أوامر يدوية (بدون سكريبت)

إذا كنت تفضل العمل يدوياً:

```powershell
# 1. الانتقال للمجلد
cd C:\Users\z97o\Desktop\project\omantel

# 2. تهيئة Git
git init

# 3. إضافة الملفات
git add .

# 4. Commit
git commit -m "Initial commit"

# 5. ربط بـ GitHub (استبدل بالقيم الصحيحة)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 6. رفع الكود
git branch -M main
git push -u origin main
```

---

## ✅ التحقق من النجاح

بعد الرفع:
1. اذهب إلى repository على GitHub
2. تحقق من وجود جميع الملفات
3. راجع تبويب "Actions" - يجب أن ترى workflows تعمل

---

## 📚 للمزيد من التفاصيل

راجع:
- [SETUP_GITHUB.md](SETUP_GITHUB.md) - دليل شامل
- [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) - إعداد الـ deployment

---

**جاهز! 🚀**
