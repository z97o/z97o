# Generate Django Secret Key for Render
Write-Host "Generating Django SECRET_KEY..." -ForegroundColor Cyan
Write-Host ""

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Write-Host ""
Write-Host "Copy this key and use it as SECRET_KEY in Render Environment Variables" -ForegroundColor Green
