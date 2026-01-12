@echo off
REM Script to run Django server on public host (Windows)
REM This allows the server to be accessible from other devices on the network

echo Starting Django server on public host (0.0.0.0:8000)...
echo The server will be accessible from other devices on your network.
echo.
echo To access from other devices, use:
echo   http://YOUR_IP_ADDRESS:8000
echo.
echo To find your IP address, run: ipconfig
echo.

python manage.py runserver 0.0.0.0:8000
