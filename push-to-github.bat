@echo off
REM Script لرفع الملفات إلى GitHub
REM Repository: https://github.com/z97o/z97o.git

echo ========================================
echo   رفع الملفات إلى GitHub
echo ========================================
echo.

REM التحقق من Git
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [خطأ] Git غير مثبت!
    echo.
    echo يرجى تثبيت Git من: https://git-scm.com/download/win
    echo ثم أعد تشغيل هذا الملف
    pause
    exit /b 1
)

echo [1/6] التحقق من Git...
git --version
echo.

echo [2/6] تهيئة Git repository...
if not exist .git (
    git init
    echo تم تهيئة Git repository
) else (
    echo Git repository موجود بالفعل
)
echo.

echo [3/6] إضافة جميع الملفات...
git add .
echo تمت إضافة الملفات
echo.

echo [4/6] إنشاء commit...
git commit -m "Initial commit: Omantel NetInsight project"
echo تم إنشاء commit
echo.

echo [5/6] ربط المشروع بـ GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/z97o/z97o.git
echo تم ربط المشروع بـ GitHub
echo.

echo [6/6] تغيير اسم الفرع إلى main...
git branch -M main
echo.

echo ========================================
echo   جاهز للرفع!
echo ========================================
echo.
echo الآن قم بتنفيذ الأمر التالي:
echo   git push -u origin main
echo.
echo ملاحظة: سيُطلب منك:
echo   - اسم المستخدم: z97o
echo   - كلمة المرور: Personal Access Token
echo.
echo للحصول على Token: https://github.com/settings/tokens
echo.
pause
