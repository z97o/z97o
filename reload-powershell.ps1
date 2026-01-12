# إعادة تحميل PATH في PowerShell الحالي
# هذا السكريبت يعيد تحميل PATH بدون إعادة تشغيل PowerShell

Write-Host "إعادة تحميل PATH..." -ForegroundColor Yellow

# إعادة تحميل PATH من النظام
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "✓ تم إعادة تحميل PATH" -ForegroundColor Green
Write-Host ""

# التحقق من Git
Write-Host "التحقق من Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ Git غير متاح. قد تحتاج لإعادة تشغيل PowerShell" -ForegroundColor Yellow
    Write-Host "أو أضف Git يدوياً:" -ForegroundColor Yellow
    Write-Host '  $env:Path += ";C:\Program Files\Git\bin"' -ForegroundColor Cyan
}

Write-Host ""
Write-Host "جاهز!" -ForegroundColor Green
