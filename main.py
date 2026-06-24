"""
Main orchestrator. Starts network monitoring, optional web dashboard, and Telegram bot.
"""
import sys
import signal
import asyncio
import logging
import threading

from app.core.config import LOG_INTERVAL_MINUTES, ENABLE_WEB_DASHBOARD
from app.core.monitor import NetworkMonitor
from app.bot_module.bot import start_bot
from app.web.server import run_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

def main():
    monitor = NetworkMonitor()

    if not monitor.discover_device():
        logger.error("Could not find UPnP router. Exiting.")
        sys.exit(1)

    # Start background database logger
    monitor.start_logging(interval_minutes=LOG_INTERVAL_MINUTES)

    # Start Flask dashboard server if enabled
    if ENABLE_WEB_DASHBOARD:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        logger.info("Flask server started in background thread")
    else:
        logger.info("Web dashboard is disabled in configuration")

    # Graceful shutdown handler
    def handle_signal(sig, frame):
        logger.info(f"Signal {sig} received, shutting down...")
        monitor.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    # Start Telegram bot (blocks main thread)
    try:
        asyncio.run(start_bot(monitor))
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
    finally:
        monitor.close()

if __name__ == "__main__":
    main()
