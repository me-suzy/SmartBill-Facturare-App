@echo off
echo ========================================
echo    SMARTBILL APP - STARTING...
echo ========================================
echo.

REM Verifică dacă Python este instalat
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nu este instalat sau nu este în PATH!
    echo Instalează Python de la https://python.org
    pause
    exit /b 1
)

echo ✅ Python găsit!
echo.

REM Verifică dacă fișierele necesare există
if not exist "app.py" (
    echo ❌ Fișierul app.py nu a fost găsit!
    echo Asigură-te că ești în directorul corect.
    pause
    exit /b 1
)

echo ✅ Fișierele necesare găsite!
echo.

REM Pornește aplicația
echo 🚀 Pornesc SmartBill App...
echo 🌐 Aplicația va fi disponibilă la: http://localhost:5000
echo 📱 Browser-ul se va deschide automat în 3 secunde...
echo.
echo 💡 Pentru a opri aplicația, apasă Ctrl+C
echo.

python app.py

echo.
echo 👋 Aplicația s-a închis.
pause 