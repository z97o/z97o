# 🚀 رفع الملفات إلى GitHub الآن

## الطريقة السريعة (إذا كان Git مثبتاً)

### الطريقة 1: استخدام ملف Batch

1. انقر نقراً مزدوجاً على: `push-to-github.bat`
2. اتبع التعليمات على الشاشة
3. في النهاية، نفّذ: `git push -u origin main`

---

### الطريقة 2: الأوامر اليدوية

افتح PowerShell في مجلد `omantel` ونفّذ:

```powershell
# 1. الانتقال للمجلد
cd C:\Users\z97o\Desktop\project\omantel

# 2. تهيئة Git (للمرة الأولى فقط)
git init

# 3. إضافة جميع الملفات
git add .

# 4. إنشاء commit
git commit -m "Initial commit: Omantel NetInsight project"

# 5. ربط المشروع بـ GitHub
git remote add origin https://github.com/z97o/z97o.git

# 6. تغيير اسم الفرع إلى main
git branch -M main

# 7. رفع الملفات
git push -u origin main
```

---

## ⚠️ إذا ظهر خطأ "git is not recognized"

### تثبيت Git:

1. **حمّل Git:**
   - اذهب إلى: https://git-scm.com/download/win
   - حمّل "Git for Windows"
   - شغّل المثبت

2. **خيارات التثبيت المهمة:**
   - اختر "Git from the command line and also from 3rd-party software"
   - اختر "Use bundled OpenSSH"
   - باقي الخيارات يمكنك تركها افتراضية

3. **بعد التثبيت:**
   - أعد فتح PowerShell
   - نفّذ الأوامر مرة أخرى

---

## 🔐 Personal Access Token

عند `git push`، سيُطلب منك:

- **اسم المستخدم:** `z97o`
- **كلمة المرور:** Personal Access Token (ليس كلمة المرور العادية!)

### إنشاء Token:

1. اذهب إلى: https://github.com/settings/tokens
2. اضغط "Generate new token" > "Generate new token (classic)"
3. أدخل اسم للـ Token (مثلاً: "omantel-project")
4. اختر الصلاحيات:
   - ✅ `repo` (Full control of private repositories)
5. اضغط "Generate token"
6. **انسخ Token فوراً** (لن تتمكن من رؤيته مرة أخرى!)
7. استخدمه ككلمة مرور عند `git push`

---

## ✅ التحقق من النجاح

بعد الرفع الناجح:

1. اذهب إلى: https://github.com/z97o/z97o
2. يجب أن ترى جميع الملفات
3. راجع تبويب "Actions" - يجب أن ترى workflows تعمل

---

## 🛠️ استكشاف الأخطاء

### خطأ: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/z97o/z97o.git
```

### خطأ: "failed to push"
- تأكد من أن Token صحيح
- تأكد من أن Repository موجود على GitHub
- جرب: `git push -u origin main --force` (بحذر!)

### خطأ: "authentication failed"
- تأكد من استخدام Token وليس كلمة المرور
- أنشئ Token جديد إذا لزم الأمر

---

## 📝 ملخص الأوامر الكاملة

```powershell
cd C:\Users\z97o\Desktop\project\omantel
git init
git add .
git commit -m "Initial commit: Omantel NetInsight project"
git remote add origin https://github.com/z97o/z97o.git
git branch -M main
git push -u origin main
```

**جاهز! 🚀**
