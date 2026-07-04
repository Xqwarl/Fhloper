#!/bin/bash

# ============================================
# APK Subscription Bot - Linux Launcher
# ============================================

clear

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║          APK Subscription Bot - Linux              ║"
echo "║                                                    ║"
echo "║  Telegram Bot for APK Processing                  ║"
echo "╚════════════════════════════════════════════���═══════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен"
    echo "   Установи: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"

# Check if apktool is available
if ! command -v apktool &> /dev/null; then
    echo "❌ apktool не найден"
    echo "   Установи apktool (смотри README.md)"
    exit 1
fi

echo "✅ apktool найден"

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "❌ Java не установлена"
    echo "   Установи: sudo apt-get install openjdk-11-jdk"
    exit 1
fi

echo "✅ Java найдена: $(java -version 2>&1 | head -n 1)"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден"
    echo "   Создай: cp .env.example .env"
    echo "   Отредактируй: nano .env"
    exit 1
fi

echo "✅ .env файл найден"

# Check if requirements are installed
echo ""
echo "📦 Проверка зависимостей..."
python3 -c "import telegram" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Зависимости не установлены"
    echo "   Устанавливаю..."
    pip install -r requirements.txt
fi

echo "✅ Все зависимости установлены"

# Create work directories if they don't exist
echo ""
echo "📁 Проверка рабочих папок..."
mkdir -p /tmp/apk_work
mkdir -p /tmp/apk_output
echo "✅ Рабочие папки созданы"

# Display info
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║              Запуск бота...                        ║"
echo "║                                                    ║"
echo "║  Бот готов к обработке APK файлов                ║"
echo "║  Отправь /start боту в Telegram                  ║"
echo "║                                                    ║"
echo "║  Для остановки нажми Ctrl + C                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Run the bot
python3 bot.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Ошибка при запуске бота"
    echo "   Смотри сообщение об ошибке выше"
    exit 1
fi
