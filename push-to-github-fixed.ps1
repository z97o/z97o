# PowerShell Script لرفع الملفات إلى GitHub
# هذا السكريبت يضيف Git إلى PATH ثم يرفع الملفات

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  رفع الملفات إلى GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# إضافة Git إلى PATH
$gitPath = "C:\Program Files\Git\bin"
if (Test-Path $gitPath) {
    $env:Path += ";$gitPath"
    Write-Host "✓ تم إضافة Git إلى PATH" -ForegroundColor Green
} else {
    Write-Host "✗ Git غير موجود في المسار المتوقع" -ForegroundColor Red
    exit 1
}

# التحقق من Git
Write-Host "التحقق من Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git غير متاح" -ForegroundColor Red
    exit 1
}

Write-Host ""

# الانتقال لمجلد المشروع
$projectPath = "C:\Users\z97o\Desktop\project\omantel"
Set-Location $projectPath
Write-Host "المجلد الحالي: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# تهيئة Git
Write-Host "[1/7] تهيئة Git repository..." -ForegroundColor Yellow
if (-not (Test-Path .git)) {
    git init
    Write-Host "✓ تم تهيئة Git repository" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository موجود بالفعل" -ForegroundColor Green
}
Write-Host ""

# إضافة الملفات
Write-Host "[2/7] إضافة جميع الملفات..." -ForegroundColor Yellow
git add .
Write-Host "✓ تمت إضافة الملفات" -ForegroundColor Green
Write-Host ""

# التحقق من وجود تغييرات
Write-Host "[3/7] التحقق من التغييرات..." -ForegroundColor Yellow
$status = git status --short
if ($status) {
    Write-Host "✓ يوجد ملفات للرفع" -ForegroundColor Green
} else {
    Write-Host "⚠ لا توجد تغييرات جديدة" -ForegroundColor Yellow
}
Write-Host ""

# Commit
Write-Host "[4/7] إنشاء commit..." -ForegroundColor Yellow
try {
    git commit -m "Initial commit: Omantel NetInsight project"
    Write-Host "✓ تم إنشاء commit" -ForegroundColor Green
} catch {
    Write-Host "⚠ قد يكون هناك commit موجود بالفعل" -ForegroundColor Yellow
}
Write-Host ""

# ربط بـ GitHub
Write-Host "[5/7] ربط المشروع بـ GitHub..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote origin موجود: $remoteExists" -ForegroundColor Yellow
    $update = Read-Host "هل تريد تحديثه؟ (y/n)"
    if ($update -eq "y" -or $update -eq "Y") {
        git remote set-url origin https://github.com/z97o/z97o.git
        Write-Host "✓ تم تحديث remote" -ForegroundColor Green
    }
} else {
    git remote add origin https://github.com/z97o/z97o.git
    Write-Host "✓ تم ربط المشروع بـ GitHub" -ForegroundColor Green
}
Write-Host ""

# تغيير اسم الفرع
Write-Host "[6/7] تغيير اسم الفرع إلى main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✓ تم تغيير اسم الفرع" -ForegroundColor Green
Write-Host ""

# رفع الملفات
Write-Host "[7/7] رفع الملفات إلى GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠ سيُطلب منك:" -ForegroundColor Yellow
Write-Host "   - اسم المستخدم: z97o" -ForegroundColor White
Write-Host "   - كلمة المرور: Personal Access Token" -ForegroundColor White
Write-Host ""
Write-Host "للحصول على Token: https://github.com/settings/tokens" -ForegroundColor Cyan
Write-Host ""
Write-Host "اضغط Enter للمتابعة..." -ForegroundColor Yellow
Read-Host

git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ تم رفع الملفات بنجاح!" -ForegroundColor Green
    Write-Host "  راجع: https://github.com/z97o/z97o" -ForegroundColor Cyan
} else {
    Write-Host "  ⚠ حدث خطأ أثناء الرفع" -ForegroundColor Yellow
    Write-Host "  تحقق من Token والاتصال بالإنترنت" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
