"""Configuration for APK Bot"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot configuration with proper error handling"""
    
    # Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
    
    # Parse ADMIN_IDS safely
    _admin_ids_str = os.getenv("ADMIN_IDS", "").strip()
    try:
        ADMIN_IDS = [int(x.strip()) for x in _admin_ids_str.split(",") if x.strip()] if _admin_ids_str else []
    except ValueError as e:
        print(f"❌ Error parsing ADMIN_IDS: {e}")
        print(f"   Make sure ADMIN_IDS contains only comma-separated integers")
        ADMIN_IDS = []
    
    # Paths
    APKTOOL_PATH = os.getenv("APKTOOL_PATH", "apktool").strip()
    JAVA_PATH = os.getenv("JAVA_PATH", "java").strip()
    WORK_DIR = os.getenv("WORK_DIR", "/tmp/apk_work").strip()
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/tmp/apk_output").strip()
    
    # Default values
    DEFAULT_BRANDING = os.getenv("DEFAULT_BRANDING", "@ApkVzlomers").strip()
    DEFAULT_TITLE = os.getenv("DEFAULT_TITLE", "ApkVzlomers").strip()
    
    # APK processing settings
    MAX_FILE_SIZE = 2000 * 1024 * 1024  # 2GB
    ALLOWED_EXTENSIONS = ['.apk']
    
    # Validation
    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []
        
        if not cls.BOT_TOKEN:
            errors.append("❌ BOT_TOKEN is not set in .env file")
        
        if not cls.ADMIN_IDS:
            errors.append("⚠️  ADMIN_IDS is empty - no one can access the bot")
        
        if errors:
            print("\n🔴 Configuration Errors:")
            for error in errors:
                print(f"   {error}")
            print("\nPlease check your .env file\n")
            return False
        
        return True

config = Config()

# Validate on import
if not config.validate():
    print("⚠️  Bot may not work correctly with current configuration")
