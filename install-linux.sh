#!/bin/bash

# ============================================
# APK Bot - Linux Installation Script
# ============================================

clear

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║    APK Subscription Bot - Linux Installer         ║"
echo "║                                                    ║"
echo "║  Автоматическая установка всех зависимостей    ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Не запускай скрипт как root (sudo)"
    echo "   Запусти: bash install-linux.sh"
    exit 1
fi

echo "Шаг 1️⃣: Обновление системы..."
sudo apt-get update
sudo apt-get upgrade -y

echo ""
echo "Шаг 2️⃣: Установка зависимостей..."
sudo apt-get install -y \
    python3.11 \
    python3-pip \
    openjdk-11-jdk \
    git \
    wget \
    unzip \
    curl \
    build-essential

echo ""
echo "Шаг 3️⃣: Установка apktool..."
cd /tmp
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar 2>/dev/null
sudo mv apktool_2.7.0.jar /usr/local/bin/

sudo bash -c 'cat > /usr/local/bin/apktool << "EOF"
#!/bin/bash
java -jar /usr/local/bin/apktool_2.7.0.jar "$@"
EOF'

sudo chmod +x /usr/local/bin/apktool

echo ""
echo "Шаг 4️⃣: Скачивание репозитория..."
cd ~
git clone https://github.com/Xqwarl/Fhloper.git
cd Fhloper

echo ""
echo "Шаг 5️⃣: Установка Python зависимостей..."
pip install -r requirements.txt

echo ""
echo "Шаг 6️⃣: Создание рабочих папок..."
mkdir -p /tmp/apk_work
mkdir -p /tmp/apk_output
chmod 777 /tmp/apk_work
chmod 777 /tmp/apk_output

echo ""
echo "Шаг 7️⃣: Создание .env файла..."
cp .env.example .env

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║              ✅ Установка завершена!             ║"
echo "║                                                    ║"
echo "║  Теперь отредактируй .env файл:                  ║"
echo "║  nano ~/Fhloper/.env                             ║"
echo "║                                                    ║"
echo "║  Замени:                                          ║"
echo "║  BOT_TOKEN=твой_токен_от_BotFather               ║"
echo "║  ADMIN_IDS=твой_ID_от_userinfobot                ║"
echo "║                                                    ║"
echo "║  Затем запусти:                                   ║"
echo "║  python3 ~/Fhloper/bot.py                        ║"
echo "║                                                    ║"
echo "║  Или используй systemd:                           ║"
echo "║  bash ~/Fhloper/install-systemd.sh              ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

echo "Открыть .env в редакторе? (y/n)"
read -r response
if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    nano ~/Fhloper/.env
fi

echo ""
echo "Готово! 🚀"
echo ""
