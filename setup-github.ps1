# PowerShell Script لإعداد GitHub
# قم بتشغيل هذا السكريبت بعد تثبيت Git

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  إعداد GitHub للمشروع" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# التحقق من Git
Write-Host "التحقق من تثبيت Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ Git مثبت: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git غير مثبت!" -ForegroundColor Red
    Write-Host "يرجى تثبيت Git من: https://git-scm.com/download/win" -ForegroundColor Red
    Write-Host "ثم أعد تشغيل هذا السكريبت" -ForegroundColor Red
    exit 1
}

Write-Host ""

# التحقق من وجود .git
if (Test-Path .git) {
    Write-Host "✓ Git repository موجود بالفعل" -ForegroundColor Green
} else {
    Write-Host "تهيئة Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ تم تهيئة Git repository" -ForegroundColor Green
}

Write-Host ""

# طلب معلومات GitHub
Write-Host "أدخل معلومات GitHub:" -ForegroundColor Cyan
$githubUsername = Read-Host "اسم المستخدم على GitHub"
$repoName = Read-Host "اسم Repository (مثلاً: omantel-netinsight)"

if ([string]::IsNullOrWhiteSpace($githubUsername) -or [string]::IsNullOrWhiteSpace($repoName)) {
    Write-Host "✗ يجب إدخال اسم المستخدم واسم Repository" -ForegroundColor Red
    exit 1
}

$repoUrl = "https://github.com/$githubUsername/$repoName.git"

Write-Host ""
Write-Host "سيتم ربط المشروع بـ: $repoUrl" -ForegroundColor Yellow
$confirm = Read-Host "هل أنت متأكد؟ (y/n)"

if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "تم الإلغاء" -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# إضافة الملفات
Write-Host "إضافة الملفات..." -ForegroundColor Yellow
git add .
Write-Host "✓ تمت إضافة الملفات" -ForegroundColor Green

# Commit
Write-Host "إنشاء commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Omantel NetInsight project"
Write-Host "✓ تم إنشاء commit" -ForegroundColor Green

# ربط بـ GitHub
Write-Host "ربط المشروع بـ GitHub..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote origin موجود بالفعل. هل تريد تحديثه؟" -ForegroundColor Yellow
    $updateRemote = Read-Host "(y/n)"
    if ($updateRemote -eq "y" -or $updateRemote -eq "Y") {
        git remote set-url origin $repoUrl
        Write-Host "✓ تم تحديث remote" -ForegroundColor Green
    }
} else {
    git remote add origin $repoUrl
    Write-Host "✓ تم ربط المشروع بـ GitHub" -ForegroundColor Green
}

# تغيير اسم الفرع
Write-Host "تغيير اسم الفرع إلى main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✓ تم تغيير اسم الفرع" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  جاهز للرفع!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "الخطوة التالية:" -ForegroundColor Yellow
Write-Host "1. تأكد من إنشاء Repository على GitHub: $repoUrl" -ForegroundColor White
Write-Host "2. قم بتنفيذ: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "ملاحظة: قد يُطلب منك اسم المستخدم و Personal Access Token" -ForegroundColor Yellow
Write-Host "للحصول على Token: https://github.com/settings/tokens" -ForegroundColor Yellow
Write-Host ""
