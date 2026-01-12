# Fix Git in current PowerShell session
# Run this script in any PowerShell window

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Fixing Git in PowerShell" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Add Git to PATH
$gitPath = "C:\Program Files\Git\bin"
if (Test-Path $gitPath) {
    if ($env:Path -notlike "*$gitPath*") {
        $env:Path += ";$gitPath"
        Write-Host "[OK] Git added to PATH" -ForegroundColor Green
    } else {
        Write-Host "[OK] Git already in PATH" -ForegroundColor Green
    }
} else {
    Write-Host "[ERROR] Git not found at expected path" -ForegroundColor Red
    Write-Host "   Expected path: $gitPath" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check Git
Write-Host "Checking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "[OK] $gitVersion" -ForegroundColor Green
    Write-Host ""
    Write-Host "[OK] Git is working now!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now use git commands in this window" -ForegroundColor Cyan
} catch {
    Write-Host "[ERROR] Git is still not available" -ForegroundColor Red
    Write-Host "   You may need to restart PowerShell" -ForegroundColor Yellow
}

Write-Host ""
