"""Configuration for APK Bot"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(","))) if os.getenv("ADMIN_IDS") else []
    APKTOOL_PATH = os.getenv("APKTOOL_PATH", "apktool")
    JAVA_PATH = os.getenv("JAVA_PATH", "java")
    WORK_DIR = os.getenv("WORK_DIR", "/tmp/apk_work")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/tmp/apk_output")
    DEFAULT_BRANDING = os.getenv("DEFAULT_BRANDING", "@ApkVzlomers")
    DEFAULT_TITLE = os.getenv("DEFAULT_TITLE", "ApkVzlomers")
    
    # APK processing settings
    MAX_FILE_SIZE = 2000 * 1024 * 1024  # 2GB
    ALLOWED_EXTENSIONS = ['.apk']

config = Config()
