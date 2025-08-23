@echo off
echo =====================================
echo   🎁 Telegram Gift Bot - Запуск
echo =====================================
echo.

REM Проверка Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python не найден!
    echo 📥 Скачайте с https://python.org
    echo    ОБЯЗАТЕЛЬНО поставьте галочку "Add Python to PATH"
    pause
    exit /b 1
)

REM Проверка зависимостей
echo 🔍 Проверка зависимостей...
python -c "import telethon" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Установка зависимостей...
    pip install -r requirements.txt
)

REM Проверка .env файла
if not exist .env (
    echo ⚠️  Файл .env не найден!
    echo 📋 Скопируйте env.example в .env
    echo    И заполните API ключи
    pause
    exit /b 1
)

REM Проверка бюджетов
if not exist budgets.json (
    echo ⚠️  Файл budgets.json не найден!
    echo 📋 Скопируйте budgets.example.json в budgets.json
    echo    И настройте свои каналы
    pause
    exit /b 1
)

echo ✅ Все проверки пройдены!
echo 🚀 Запуск бота...
echo.

python monitor_multi_advanced.py

echo.
echo 🛑 Бот остановлен
pause
