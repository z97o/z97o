# Simple script to add Git to PATH in current session
$env:Path += ";C:\Program Files\Git\bin"
Write-Host "Git added to PATH. Testing..." -ForegroundColor Green
git --version
