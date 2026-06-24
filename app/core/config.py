"""
Traffic Monitor Configuration.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT_ID_STR = os.getenv("TG_CHAT_ID")
try:
    TG_CHAT_ID = int(TG_CHAT_ID_STR) if TG_CHAT_ID_STR else None
except (ValueError, TypeError):
    TG_CHAT_ID = None

# SQLite
DB_PATH = os.getenv("DB_PATH", "data/traffic.db")

# UPnP Router
ROUTER_NAME = os.getenv("ROUTER_NAME", "Archer_A5")
UPNP_SERVICE_TYPE = os.getenv("UPNP_SERVICE_TYPE", "urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1")
UPNP_ACTION_RECEIVED = os.getenv("UPNP_ACTION_RECEIVED", "GetTotalBytesReceived")
UPNP_ACTION_SENT = os.getenv("UPNP_ACTION_SENT", "GetTotalBytesSent")

# Localization
LANGUAGE = os.getenv("LANGUAGE", "en").lower()

# Traffic Limits
MONTHLY_LIMIT_GB = float(os.getenv("MONTHLY_LIMIT_GB", "250.0"))
DAILY_ALERT_THRESHOLDS_MB = [4096, 5120, 6144, 7168, 8192, 10240]

# Intervals
LOG_INTERVAL_MINUTES = 5
ALERT_CHECK_SECONDS = 300
SPEED_MEASURE_SECONDS = 10

# Flask Dashboard
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5005))
ENABLE_WEB_DASHBOARD = os.getenv("ENABLE_WEB_DASHBOARD", "false").lower() == "true"
