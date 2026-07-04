# APK Subscription Bot - Quick Start Guide

## ⚡ Быстрый старт (Quick Start)

### Windows
```powershell
# 1. Установи зависимости один раз
pip install -r requirements.txt

# 2. Отредактируй .env файл с твоими данными
# BOT_TOKEN=твой_токен_от_BotFather
# ADMIN_IDS=твой_ID

# 3. Запусти бота
python bot.py
```

### Linux/macOS
```bash
# 1. Установи зависимости
pip install -r requirements.txt

# 2. Отредактируй .env
nano .env

# 3. Запусти бота
python3 bot.py
```

## 📋 Получить необходимые данные

1. **BOT_TOKEN** - пиши @BotFather в Telegram → /newbot
2. **ADMIN_IDS** - пиши @userinfobot в Telegram → узнаешь свой ID
3. **WORK_DIR** - папка для временных файлов (например: C:\temp\apk_work)
4. **OUTPUT_DIR** - папка для готовых APK (например: C:\temp\apk_output)

## 🎮 Использование в Telegram

1. Найди своего бота (по имени которое дал @BotFather)
2. Напиши `/start`
3. Выбери действие:
   - **📁 Загрузить файлы** - обработать несколько APK
   - **📄 Загрузить файл** - обработать один APK
4. Отправь APK файлы
5. Отправь ссылку на подписку (t.me/YourChannel или @YourChannel)
6. Выбери заголовок или пропусти
7. Жди результат ⏳

## 🐳 Docker (если установлен Docker)

```bash
docker build -t apk-bot .
docker run -d --name apk-bot \
  -v /path/to/work:/tmp/apk_work \
  -v /path/to/output:/tmp/apk_output \
  --env-file .env \
  apk-bot
```

## 🆘 Решение проблем

| Ошибка | Решение |
|--------|---------|
| `apktool: command not found` | Переустанови apktool и добавь в PATH |
| `BOT_TOKEN not set` | Проверь .env файл и заполни BOT_TOKEN |
| `ADMIN_IDS is empty` | Заполни ADMIN_IDS в .env своим Telegram ID |
| APK processing fails | Убедись что файл это реально APK, не поврежден |

## 📚 Документация

Полная документация - смотри README.md

## 🚀 Готово!

Теперь бот готов к работе! Отправляй APK файлы и получай результаты 💪
