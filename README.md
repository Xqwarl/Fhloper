# 🎮 APK Subscription Bot - Telegram бот для обработки APK файлов

## 📋 Описание

Профессиональный Telegram бот для администраторов, который:
- ✅ Обрабатывает APK файлы (по одному или пакетно)
- ✅ Встраивает таблицу подписки с кастомным брендингом
- ✅ Добавляет ссылки на подписку в приложения
- ✅ Кастомизирует заголовки и брендинг
- ✅ Автоматически собирает и подписывает APK файлы
- ✅ Работает на Windows, Linux и Mac
- ✅ Поддерживает Docker для сервера

## ✨ Возможности

✅ **Только для админов** - Управление через `.env`  
✅ **Массовая обработка** - Несколько APK одновременно  
✅ **Кастомный брендинг** - Замена текста на свой  
✅ **Кастомные заголовки** - Установка своих названий таблицы  
✅ **Красивый интерфейс** - Таблица в современном дизайне  
✅ **Автоматическая подпись** - APK сам подписывается и оптимизируется  
✅ **Полная модификация** - Настоящая модификация smali кода  
✅ **Асинхронная обработка** - Бот не зависает при обработке  

---

# 🪟 УСТАНОВКА НА WINDOWS

## Шаг 1️⃣: Установи необходимое ПО

Скачай и установи (в любом порядке):

1. **Python 3.11+** → https://www.python.org/downloads/
   - ⚠️ **ВАЖНО:** При установке поставь галку **"Add Python to PATH"**
   - Выбери 64-bit версию для Windows

2. **Java (OpenJDK 11)** → https://adoptopenjdk.net/
   - Скачай версию **11** для Windows
   - При установке оставь всё как есть

3. **Git** → https://git-scm.com/download/win
   - Стандартная установка

4. **VS Code** (опционально) → https://code.visualstudio.com/

**После каждой установки перезагрузи компьютер!**

---

## Шаг 2️⃣: Проверь что всё установилось

Открой **PowerShell** (нажми **Win + X** → выбери **PowerShell** или **Terminal**)

Проверь версии:

```powershell
python --version
```

Должно вывести: `Python 3.11.x`

```powershell
java -version
```

Должно вывести: `openjdk version "11.x.x"`

```powershell
git --version
```

Должно вывести: `git version 2.x.x`

Если что-то не нашло → переустанови ПО и убедись что поставил галку "Add to PATH"

---

## Шаг 3️⃣: Установи apktool

В PowerShell выполни эти команды:

```powershell
# Создай папку для apktool
mkdir C:\apktool
cd C:\apktool
```

```powershell
# Скачай apktool
curl -L -o apktool.jar https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar
```

```powershell
# Создай bat файл
@"
@echo off
java -jar "%~dp0apktool.jar" %*
"@ | Out-File -Encoding ASCII apktool.bat
```

```powershell
# Проверь что работает
.\apktool
```

Должна вывести справка apktool.

---

## Шаг 4️⃣: Добавь apktool в PATH

Это нужно чтобы apktool работал из любой папки.

**Пошагово:**

1. Нажми **Win + X** → выбери **System** (Система)
2. Слева найди **Advanced system settings** (Дополнительные параметры системы)
3. Нажми кнопку **Environment Variables** (Переменные окружения)
4. Внизу найди **Path** → выбери и нажми **Edit** (Изменить)
5. Нажми **New** (Создать) и вставь: `C:\apktool`
6. Нажми **OK** → **OK** → **OK**
7. **Закрой и переоткрой PowerShell**

Проверь:

```powershell
apktool
```

Должна вывести справка.

---

## Шаг 5️⃣: Скачай репо

```powershell
cd $HOME\Documents
git clone https://github.com/Xqwarl/Fhloper.git
cd Fhloper
```

---

## Шаг 6️⃣: Установи Python зависимости

```powershell
pip install -r requirements.txt
```

Подожди пока установится (1-2 минуты).

---

## Шаг 7️⃣: Создай рабочие папки

```powershell
mkdir C:\temp\apk_work
mkdir C:\temp\apk_output
```

---

## Шаг 8️⃣: Получи данные для бота

### BOT_TOKEN:
1. Открой Telegram
2. Найди **@BotFather**
3. Напиши: `/newbot`
4. Следуй инструкциям
5. Он даст токен вида: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`
6. **Скопируй токен**

### ADMIN_ID:
1. Открой Telegram
2. Найди **@userinfobot**
3. Нажми **Start**
4. Он скажет твой ID (например: `123456789`)
5. **Скопируй число**

---

## Шаг 9️⃣: Создай файл .env

**Способ 1 (через PowerShell):**

```powershell
cd $HOME\Documents\Fhloper
notepad .env
```

Откроется Блокнот. Вставь содержимое ниже.

**Способ 2 (через Проводник):**
1. Открой `C:\Users\[ТвоеИмя]\Documents\Fhloper`
2. Правый клик → Создать → Текстовый документ
3. Переименуй в `.env`
4. Открой двойным кликом (откроется Блокнот)

**Содержимое .env файла:**

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMIN_IDS=123456789
APKTOOL_PATH=apktool
JAVA_PATH=java
WORK_DIR=C:\temp\apk_work
OUTPUT_DIR=C:\temp\apk_output
DEFAULT_BRANDING=@ApkVzlomers
DEFAULT_TITLE=ApkVzlomers
```

**Замени:**
- `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` → твой BOT_TOKEN
- `123456789` → твой ADMIN_ID

**Сохрани:**
- Ctrl + S
- Закрой блокнот

---

## Шаг 🔟: Создай bat файл для быстрого запуска

**В папке Fhloper создай файл `run.bat`:**

```batch
@echo off
CLS
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║        APK Subscription Bot - Windows              ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo Запуск бота...
echo.

python bot.py

pause
```

**Как создать:**
1. Открой Блокнот
2. Вставь текст выше
3. Сохрани как `run.bat` в папке `C:\Users\[ТвоеИмя]\Documents\Fhloper`
4. Теперь можно просто двойной клик по `run.bat` чтобы запустить бота!

---

## ✅ Готово! Запусти бота

### Способ 1: PowerShell

```powershell
cd C:\Users\[ТвоеИмя]\Documents\Fhloper
python bot.py
```

### Способ 2: Двойной клик

1. Открой `C:\Users\[ТвоеИмя]\Documents\Fhloper`
2. Двойной клик по `run.bat`

### Способ 3: VS Code

1. Открой VS Code
2. Ctrl + K Ctrl + O
3. Выбери папку `Fhloper`
4. Ctrl + ` (откроется Terminal внизу)
5. Введи: `python bot.py`

**Если всё правильно, увидишь:**

```
2026-07-04 21:05:00,123 - __main__ - INFO - 🚀 Starting APK Bot...
2026-07-04 21:05:00,456 - __main__ - INFO - Admin IDs: [123456789]
2026-07-04 21:05:00,789 - __main__ - INFO - Default branding: @ApkVzlomers
2026-07-04 21:05:01,012 - __main__ - INFO - ✅ Bot started! Waiting for commands...
```

**Готово! Бот работает! 🎉**

---

# 🐧 УСТАНОВКА НА LINUX / СЕРВЕР

## Быстрая установка (одной командой)

```bash
# Скачай и запусти скрипт
curl -fsSL https://raw.githubusercontent.com/Xqwarl/Fhloper/main/install-linux.sh | bash
```

Или вручную:

---

## Вручную - Шаг за шагом

### Шаг 1️⃣: Обнови систему

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Шаг 2️⃣: Установи зависимости

```bash
sudo apt-get install -y \
  python3.11 \
  python3-pip \
  openjdk-11-jdk \
  git \
  wget \
  unzip \
  curl
```

### Шаг 3️⃣: Установи apktool

```bash
# Скачай apktool
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar

# Переместить в /usr/local/bin
sudo mv apktool_2.7.0.jar /usr/local/bin/

# Создай скрипт
sudo bash -c 'echo "#!/bin/bash" > /usr/local/bin/apktool'
sudo bash -c 'echo "java -jar /usr/local/bin/apktool_2.7.0.jar \"\$@\"" >> /usr/local/bin/apktool'

# Дай права на выполнение
sudo chmod +x /usr/local/bin/apktool

# Проверь что работает
apktool
```

### Шаг 4️⃣: Скачай репо

```bash
cd ~
git clone https://github.com/Xqwarl/Fhloper.git
cd Fhloper
```

### Шаг 5️⃣: Установи Python зависимости

```bash
pip install -r requirements.txt
```

### Шаг 6️⃣: Создай рабочие папки

```bash
mkdir -p /tmp/apk_work
mkdir -p /tmp/apk_output

# Дай права
chmod 777 /tmp/apk_work
chmod 777 /tmp/apk_output
```

### Шаг 7️⃣: Создай .env файл

```bash
cp .env.example .env
nano .env
```

Вставь (замени на свои данные):

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMIN_IDS=123456789
APKTOOL_PATH=/usr/local/bin/apktool
JAVA_PATH=/usr/bin/java
WORK_DIR=/tmp/apk_work
OUTPUT_DIR=/tmp/apk_output
DEFAULT_BRANDING=@ApkVzlomers
DEFAULT_TITLE=ApkVzlomers
```

Сохрани: **Ctrl + X** → **Y** → **Enter**

### Шаг 8️⃣: Запусти бота

```bash
cd ~/Fhloper
python3 bot.py
```

---

## 🐳 Запуск через Docker (для сервера)

### Установи Docker

```bash
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

### Запусти бота в Docker

```bash
cd ~/Fhloper

# Создай .env
cp .env.example .env
nano .env  # Заполни данные

# Собери и запусти
docker build -t apk-bot .
docker run -d --name apk-bot \
  -v /tmp/apk_work:/tmp/apk_work \
  -v /tmp/apk_output:/tmp/apk_output \
  --env-file .env \
  apk-bot

# Смотреть логи
docker logs -f apk-bot
```

---

## 🔄 Запуск бота при загрузке сервера (systemd)

### Создай systemd сервис

```bash
sudo nano /etc/systemd/system/apk-bot.service
```

Вставь (замени `username` на твоё имя пользователя):

```ini
[Unit]
Description=APK Subscription Bot
After=network.target

[Service]
Type=simple
User=username
WorkingDirectory=/home/username/Fhloper
ExecStart=/usr/bin/python3 /home/username/Fhloper/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Сохрани: **Ctrl + X** → **Y** → **Enter**

### Активируй сервис

```bash
# Обнови systemd
sudo systemctl daemon-reload

# Включи автозапуск
sudo systemctl enable apk-bot

# Запусти сервис
sudo systemctl start apk-bot

# Проверь статус
sudo systemctl status apk-bot

# Смотреть логи
sudo journalctl -u apk-bot -f
```

---

## 📜 Полезные команды Linux

```bash
# Проверить статус бота
sudo systemctl status apk-bot

# Остановить бота
sudo systemctl stop apk-bot

# Запустить бота
sudo systemctl start apk-bot

# Перезагрузить бота
sudo systemctl restart apk-bot

# Смотреть логи в реальном времени
sudo journalctl -u apk-bot -f

# Смотреть последние 100 строк логов
sudo journalctl -u apk-bot -n 100

# Отключить автозапуск
sudo systemctl disable apk-bot

# Удалить сервис
sudo systemctl stop apk-bot
sudo rm /etc/systemd/system/apk-bot.service
sudo systemctl daemon-reload
```

---

# 🎮 ИСПОЛЬЗОВАНИЕ БОТА В TELEGRAM

1. **Найди своего бота** в Telegram (по имени от @BotFather)
2. **Напиши `/start`** - откроется админ-панель
3. **Выбери действие:**
   - **📁 Загрузить файлы** - несколько APK за раз
   - **📄 Загрузить файл** - один APK
4. **Отправь APK файл(ы)** - просто перетащи в чат
5. **Отправь ссылку на подписку:**
   - `https://t.me/YourChannel`
   - или просто `@YourChannel`
6. **Выбери заголовок:**
   - Напиши свой текст
   - или нажми **"Пропустить"** для стандартного
7. **Жди результат** ⏳ (может занять 2-5 минут)
8. **Скачай готовый APK** с встроенной таблицей подписки

---

# 📊 Дизайн таблицы

Таблица которая встраивается в APK:

```
╔════════════════════════════╗
║   ApkVzlomers              ║
╠════════════════════════════╣
║ Сборка    │    Статус      ║
║ @ApkVzl.. │ ✓ Активна     ║
╠════════════════════════════╣
║     📲 Подписаться         ║
╚════════════════════════════╝
```

**Цвета:**
- Фон: `#1a1a2e` (тёмный)
- Заголовок: `#16213e` (ещё темнее)
- Текст: `#eaeaea` (светлый)
- Кнопка: `#e94560` (красная)
- Статус: `#4CAF50` (зелёная)

---

# 🆘 РЕШЕНИЕ ПРОБЛЕМ

## Windows

### ❌ "python: команда не найдена"

```powershell
# Проверь
where python

# Если не найдено:
# 1. Переустанови Python
# 2. ПОСТАВЬ ГАЛКУ "Add Python to PATH"
# 3. Перезагрузи компьютер
```

### ❌ "apktool: команда не найдена"

```powershell
# Проверь что файлы на месте
dir C:\apktool

# Должно быть: apktool.jar и apktool.bat

# Если нет - переделай шаг 3 установки

# Если есть но не работает:
# Повтори шаг 4 (добавление в PATH)
# Перезагрузи PowerShell
```

### ❌ "BOT_TOKEN not set"

```powershell
# Проверь что файл .env в папке Fhloper
dir .env

# Если нет - создай его (шаг 9)
# Если есть - убедись что там реальный токен
# Не забудь перезагрузить PowerShell
```

### ❌ "java: команда не найдена"

```powershell
# Переустанови Java:
# 1. https://adoptopenjdk.net/ версия 11
# 2. Установи
# 3. Перезагрузи компьютер
# 4. Проверь: java -version
```

---

## Linux

### ❌ "apktool: command not found"

```bash
# Проверь
which apktool

# Если не найдено - переделай установку apktool
sudo apt-get install apktool
# или вручную (шаг 3)
```

### ❌ "Permission denied"

```bash
# Дай права
sudo chmod +x /usr/local/bin/apktool
sudo chown $USER:$USER /tmp/apk_work /tmp/apk_output
```

### ❌ "java: command not found"

```bash
# Установи Java
sudo apt-get install openjdk-11-jdk

# Проверь версию
java -version
```

### ❌ Бот не запускается в systemd

```bash
# Смотри логи
sudo journalctl -u apk-bot -n 50

# Проверь что .env файл есть и заполнен
cat ~/Fhloper/.env

# Проверь права
ls -la ~/Fhloper/.env
```

---

# 📁 Структура папок

**Windows:**
```
C:\Users\[ТвоеИмя]\
├── Documents\
│   └── Fhloper\          ← здесь репо
│       ├── bot.py
│       ├── config.py
│       ├── .env          ← твой файл
│       ├── run.bat       ← для запуска
│       └── ...
├── apktool\              ← apktool
│   ├── apktool.jar
│   └── apktool.bat
└── temp\
    ├── apk_work\        ← временные файлы
    └── apk_output\      ← готовые APK
```

**Linux:**
```
/home/username/
├── Fhloper/              ← здесь репо
│   ├── bot.py
│   ├── config.py
│   └── .env              ← твой файл
└── /tmp
    ├── apk_work/         ← временные файлы
    └── apk_output/       ← готовые APK
```

---

# 🔐 Безопасность

- ✅ **Только админы** - Доступ через ADMIN_IDS
- ✅ **Локальная обработка** - Файлы не отправляются на сервер
- ✅ **Безопасная подпись** - Используется стандартная Android подпись
- ✅ **Чистка** - Временные файлы удаляются после обработки
- ✅ **.env в .gitignore** - Твой токен не загружается на GitHub

---

# 📝 Конфигурация

## Переменные окружения (.env)

| Переменная | Описание | Пример |
|------------|---------|--------|
| `BOT_TOKEN` | Токен Telegram бота | `123456:ABC...` |
| `ADMIN_IDS` | ID администраторов (через запятую) | `123456789,987654321` |
| `APKTOOL_PATH` | Путь к apktool | `/usr/local/bin/apktool` |
| `JAVA_PATH` | Путь к Java | `/usr/bin/java` |
| `WORK_DIR` | Папка для временных файлов | `/tmp/apk_work` |
| `OUTPUT_DIR` | Папка для готовых APK | `/tmp/apk_output` |
| `DEFAULT_BRANDING` | Брендинг по умолчанию | `@ApkVzlomers` |
| `DEFAULT_TITLE` | Заголовок по умолчанию | `ApkVzlomers` |

---

# 📞 Поддержка

Если что-то не работает:

1. Проверь раздел **"РЕШЕНИЕ ПРОБЛЕМ"** выше
2. Смотри логи (в Terminal где запущен бот)
3. Убедись что все шаги установки выполнены
4. Попробуй переустановить зависимости: `pip install -r requirements.txt`

---

# 📄 Лицензия

Этот проект для личного использования с твоими APK файлами.

⚠️ **ВАЖНО:** Обрабатывай только те APK файлы, на которые у тебя есть права!

---

**Готов обрабатывать APK? 🚀 Настрой `.env` и запусти бота!**
