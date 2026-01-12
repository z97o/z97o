# 🔧 حل مشكلة Git غير معروف في PowerShell

## المشكلة
Git مثبت لكن PowerShell لا يتعرفه (`git is not recognized`)

## ✅ الحل السريع

### الطريقة 1: استخدام السكريبت الجاهز (الأسهل)

1. انقر نقراً مزدوجاً على: `push-to-github-fixed.ps1`
2. إذا ظهرت رسالة أمان، اضغط "Run anyway" أو "تنفيذ"
3. اتبع التعليمات

### الطريقة 2: إضافة Git إلى PATH يدوياً (دائم)

#### الخطوة 1: فتح إعدادات البيئة

1. اضغط `Win + R`
2. اكتب: `sysdm.cpl` واضغط Enter
3. اضغط "Environment Variables" (متغيرات البيئة)

#### الخطوة 2: إضافة Git إلى PATH

1. في "System variables"، ابحث عن `Path`
2. اضغط "Edit" (تحرير)
3. اضغط "New" (جديد)
4. أضف: `C:\Program Files\Git\bin`
5. اضغط "OK" في جميع النوافذ

#### الخطوة 3: إعادة تشغيل PowerShell

- أغلق PowerShell الحالي
- افتح PowerShell جديد
- نفّذ: `git --version`

### الطريقة 3: استخدام المسار الكامل (مؤقت)

في PowerShell، استخدم المسار الكامل:

```powershell
# إضافة Git إلى PATH (للهذه الجلسة فقط)
$env:Path += ";C:\Program Files\Git\bin"

# التحقق
git --version

# الآن يمكنك استخدام git بشكل طبيعي
cd C:\Users\z97o\Desktop\project\omantel
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/z97o/z97o.git
git branch -M main
git push -u origin main
```

## 🚀 رفع الملفات الآن

بعد إصلاح PATH، نفّذ:

```powershell
# الانتقال للمجلد
cd C:\Users\z97o\Desktop\project\omantel

# إضافة Git إلى PATH (إذا لم تضفه بشكل دائم)
$env:Path += ";C:\Program Files\Git\bin"

# تهيئة Git
git init

# إضافة الملفات
git add .

# Commit
git commit -m "Initial commit: Omantel NetInsight project"

# ربط بـ GitHub
git remote add origin https://github.com/z97o/z97o.git

# تغيير اسم الفرع
git branch -M main

# رفع الملفات
git push -u origin main
```

## 🔐 Personal Access Token

عند `git push`، سيُطلب منك:
- **اسم المستخدم:** `z97o`
- **كلمة المرور:** Personal Access Token

للحصول على Token:
1. https://github.com/settings/tokens
2. Generate new token (classic)
3. اختر `repo`
4. انسخ Token واستخدمه ككلمة مرور

## ✅ التحقق

بعد الرفع:
- اذهب إلى: https://github.com/z97o/z97o
- يجب أن ترى جميع الملفات
