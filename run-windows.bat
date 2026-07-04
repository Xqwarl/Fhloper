@echo off
REM ============================================
REM APK Subscription Bot - Windows Launcher
REM ============================================

CLS
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║          APK Subscription Bot - Windows            ║
echo ║                                                    ║
echo ║  Telegram Bot for APK Processing                  ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не установлен или не добавлен в PATH
    echo    Скачай Python: https://www.python.org/downloads/
    echo    При установке поставь галку "Add Python to PATH"
    pause
    exit /b 1
)

echo ✅ Python найден

REM Check if apktool is available
apktool >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ apktool не найден
    echo    Убедись что установил apktool и добавил в PATH
    pause
    exit /b 1
)

echo ✅ apktool найден

REM Check if .env file exists
if not exist ".env" (
    echo ❌ Файл .env не найден
    echo    Создай .env файл с данными (смотри README.md)
    pause
    exit /b 1
)

echo ✅ .env файл найден

REM Check if requirements are installed
echo.
echo 📦 Проверка зависимостей...
python -c "import telegram" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Зависимости не установлены
    echo    Устанавливаю...
    pip install -r requirements.txt
)

echo ✅ Все зависимости установлены

REM Display info
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║              Запуск бота...                        ║
echo ║                                                    ║
echo ║  Бот готов к обработке APK файлов                ║
echo ║  Отправь /start боту в Telegram                  ║
echo ║                                                    ║
echo ║  Для остановки нажми Ctrl + C                    ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo.

REM Run the bot
python bot.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка при запуске бота
    echo    Смотри сообщение об ошибке выше
    pause
    exit /b 1
)

pause
