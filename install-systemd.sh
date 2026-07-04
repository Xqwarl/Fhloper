#!/bin/bash

# ============================================
# APK Bot - Systemd Service Installer
# ============================================

clear

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║    APK Bot - Systemd Service Installer           ║"
echo "║                                                    ║"
echo "║  Установка бота как системный сервис            ║"
echo "║  (автозапуск при загрузке сервера)              ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Get current username
CURRENT_USER=$(whoami)
HOME_DIR=$(eval echo ~$CURRENT_USER)
BOT_PATH="$HOME_DIR/Fhloper"

echo "Пользователь: $CURRENT_USER"
echo "Папка бота: $BOT_PATH"
echo ""

# Check if bot directory exists
if [ ! -d "$BOT_PATH" ]; then
    echo "❌ Папка $BOT_PATH не найдена"
    echo "   Сначала установи бот: bash install-linux.sh"
    exit 1
fi

# Check if .env exists
if [ ! -f "$BOT_PATH/.env" ]; then
    echo "❌ Файл $BOT_PATH/.env не найден"
    echo "   Отредактируй .env файл"
    exit 1
fi

echo "Создание systemd сервиса..."
echo ""

# Create systemd service file
sudo bash -c "cat > /etc/systemd/system/apk-bot.service << 'EOF'
[Unit]
Description=APK Subscription Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$BOT_PATH
ExecStart=/usr/bin/python3 $BOT_PATH/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=apk-bot

[Install]
WantedBy=multi-user.target
EOF"

echo "✅ Сервис создан"
echo ""

# Reload systemd
echo "Обновление systemd..."
sudo systemctl daemon-reload
echo "✅ systemd обновлен"
echo ""

# Enable the service
echo "Включение автозапуска..."
sudo systemctl enable apk-bot
echo "✅ Автозапуск включен"
echo ""

# Ask to start now
echo "Запустить бота сейчас? (y/n)"
read -r response
if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    sudo systemctl start apk-bot
    echo "✅ Бот запущен"
    echo ""
    echo "Смотреть логи:"
    echo "sudo journalctl -u apk-bot -f"
fi

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║              ✅ Sервис установлен!              ║"
echo "║                                                    ║"
echo "║  Полезные команды:                                ║"
echo "║                                                    ║"
echo "║  Статус:                                          ║"
echo "║  sudo systemctl status apk-bot                    ║"
echo "║                                                    ║"
echo "║  Запустить:                                       ║"
echo "║  sudo systemctl start apk-bot                     ║"
echo "║                                                    ║"
echo "║  Остановить:                                      ║"
echo "║  sudo systemctl stop apk-bot                      ║"
echo "║                                                    ║"
echo "║  Перезагрузить:                                   ║"
echo "║  sudo systemctl restart apk-bot                   ║"
echo "║                                                    ║"
echo "║  Логи (реальное время):                           ║"
echo "║  sudo journalctl -u apk-bot -f                   ║"
echo "║                                                    ║"
echo "║  Последние 100 строк логов:                       ║"
echo "║  sudo journalctl -u apk-bot -n 100               ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
