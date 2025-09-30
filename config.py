import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    # Download settings
    DOWNLOAD_PATH = "downloads"
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit for Telegram
