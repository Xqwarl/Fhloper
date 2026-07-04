#!/bin/bash
# APK Subscription Bot - Telegram Bot for APK Processing

## 📋 Overview

This is a professional Telegram bot designed for administrators to:
- Process APK files (single or bulk)
- Embed subscription tables with custom branding
- Add subscription links to games
- Customize titles and branding
- Automatically rebuild and sign APK files

## ✨ Features

✅ **Admin-only access** - Controlled via `.env` configuration  
✅ **Bulk processing** - Handle multiple APK files at once  
✅ **Custom branding** - Replace default branding with your text  
✅ **Custom titles** - Set table header titles  
✅ **Professional UI** - Styled table matching modern design  
✅ **Auto-signing** - Automatically signs and aligns APK files  
✅ **No hardcoding** - All parameters are dynamic and customizable  
✅ **Full APK modification** - Uses apktool for proper decompilation/recompilation  

## 🚀 Quick Start

### Prerequisites

- Ubuntu/Debian Linux (or WSL)
- Docker (optional, but recommended)
- Python 3.11+
- Java 11+
- apktool installed

### Installation

#### Option 1: Docker (Recommended)

```bash
git clone https://github.com/Xqwarl/Fhloper.git
cd Fhloper

# Create .env file
cp .env.example .env
# Edit .env with your BOT_TOKEN and ADMIN_IDS

# Build and run Docker container
docker build -t apk-bot .
docker run -d --name apk-bot \
  -v /tmp/apk_work:/tmp/apk_work \
  -v /tmp/apk_output:/tmp/apk_output \
  --env-file .env \
  apk-bot
```

#### Option 2: Manual Installation

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk python3-pip git unzip

# Install apktool
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar
sudo mv apktool_2.7.0.jar /usr/local/bin/
echo '#!/bin/bash' | sudo tee /usr/local/bin/apktool > /dev/null
echo 'java -jar /usr/local/bin/apktool_2.7.0.jar "$@"' | sudo tee -a /usr/local/bin/apktool > /dev/null
sudo chmod +x /usr/local/bin/apktool

# Clone repository
git clone https://github.com/Xqwarl/Fhloper.git
cd Fhloper

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Create work directories
mkdir -p /tmp/apk_work /tmp/apk_output

# Run bot
python3 bot.py
```

### Configuration

Edit `.env` file:

```env
# Telegram Bot Token (get from @BotFather)
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Admin user IDs (comma-separated)
ADMIN_IDS=123456789,987654321

# APK Tool path
APKTOOL_PATH=/usr/bin/apktool

# Java path
JAVA_PATH=/usr/bin/java

# Working directories
WORK_DIR=/tmp/apk_work
OUTPUT_DIR=/tmp/apk_output

# Default branding (displayed in table)
DEFAULT_BRANDING=@ApkVzlomers

# Default title (table header)
DEFAULT_TITLE=ApkVzlomers
```

## 💻 Usage

### Start the Bot

```bash
python3 bot.py
```

### Telegram Bot Commands

1. **Send `/start`** to activate admin panel
2. **Select "📁 Загрузить файлы"** for bulk upload
3. **Select "📄 Загрузить файл"** for single file upload
4. **Send subscription link** (e.g., `https://t.me/ApkVzlomers` or `@ApkVzlomers`)
5. **Optionally customize title** or press "Пропустить" to use default
6. **Wait for processing** - Bot will rebuild and sign APK automatically
7. **Download modified APK** with embedded subscription table

## 📊 Table Design

The embedded table follows this design:
- **Dark theme** - Background: #1a1a2e, Header: #16213e
- **Professional colors** - Primary text: #eaeaea, Button: #e94560
- **No icons** - Clean table without decorative icons
- **Subscription button** - "📲 Подписаться" with click-to-subscribe functionality
- **Status indicator** - Shows build status (✓ Активна)

Example table output:
```
┌─────────────────────────┐
│   ApkVzlomers           │
├─────────────────────────┤
│ Сборка    │    Статус   │
│ @ApkVzl.. │ ✓ Активна  │
├─────────────────────────┤
│ 📲 Подписаться          │
└─────────────────────────┘
```

## 🔧 How It Works

1. **Decompile** - Uses apktool to extract APK bytecode (smali)
2. **Modify** - Injects subscription table into MainActivity
3. **Customize** - Replaces placeholder values with user inputs
4. **Rebuild** - Recompiles APK with modified code
5. **Sign** - Signs with debug key or custom keystore
6. **Align** - Optimizes APK with zipalign
7. **Deliver** - Sends processed APK back to user

## 📁 Project Structure

```
Fhloper/
├── bot.py                 # Main bot logic
├── config.py              # Configuration handler
├── apk_processor.py       # APK decompile/recompile logic
├── smali_modifier.py      # Smali bytecode modification
├── table_generator.py     # UI table generation
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔐 Security Notes

- **Admin-only** - Access controlled by ADMIN_IDS
- **No data logging** - Processes files locally, doesn't send to external services
- **Secure signing** - Uses standard Android signing mechanisms
- **Clean output** - Removes temporary files after processing

## 🐛 Troubleshooting

### apktool not found
```bash
# Check apktool installation
which apktool
# Install if missing
sudo apt-get install apktool
```

### Permission denied
```bash
# Fix file permissions
chmod +x /usr/local/bin/apktool
sudo chown $USER:$USER /tmp/apk_work /tmp/apk_output
```

### Java version error
```bash
# Check Java version
java -version
# Must be Java 11+
sudo apt-get install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### APK build fails
```bash
# Enable debug mode in config.py
# Check logs for detailed error messages
# Ensure APK is valid before processing
```

## 📝 License

This project is designed for personal use with your own APK files.  
**IMPORTANT**: Only process APK files you have the right to modify.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review logs in `/tmp/apk_work` and `/tmp/apk_output`
3. Create an issue on GitHub with detailed error messages

---

**Ready to process APKs?** 🚀 Configure your `.env` and run `python3 bot.py`!
