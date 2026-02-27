import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
API_URL = os.getenv("API_URL", "https://apiv3.bubilet.com.tr/session/183692/city/34/tickets")

# SECURITY: Replace the placeholder below with your actual Bearer token or set it in .env
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
CF_CLEARANCE_COOKIE = os.getenv("CF_CLEARANCE_COOKIE", "")

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Referer": "https://www.bubilet.com.tr/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Authorization": f"Bearer {AUTH_TOKEN}"
}

if CF_CLEARANCE_COOKIE:
    HEADERS["Cookie"] = f"cf_clearance={CF_CLEARANCE_COOKIE}"

CHECK_INTERVAL = 3600 # Seconds (e.g., 1 hour)
