"""
Traffic monitoring via UPnP router with SQLite database storage.
Handles uint32 counters rollover.
"""
import os
import time
import threading
import logging
from datetime import datetime
import sqlite3
import upnpclient
from app.core.config import DB_PATH, ROUTER_NAME, UPNP_SERVICE_TYPE, UPNP_ACTION_RECEIVED, UPNP_ACTION_SENT

logger = logging.getLogger(__name__)
MAX_UI4 = 4_294_967_295

class NetworkMonitor:
    def __init__(self, device_name=ROUTER_NAME, service_type=UPNP_SERVICE_TYPE, action_received=UPNP_ACTION_RECEIVED, action_sent=UPNP_ACTION_SENT, db_path=DB_PATH):
        self.device_name = device_name
        self.service_type = service_type
        self.action_received = action_received
        self.action_sent = action_sent
        self.db_path = db_path
        self.device = None
        self.service = None
        self.conn = None

        self.last_raw_sent = None
        self.last_raw_received = None

        self._connect_db()
        self._create_table()

    def _connect_db(self):
        try:
            db_dir = os.path.dirname(self.db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            logger.info("Connected to SQLite")
        except Exception as e:
            logger.error(f"DB connection error: {e}")
            self.conn = None

    def _ensure_connection(self):
        if self.conn is None:
            self._connect_db()
            return
        try:
            self.conn.execute("SELECT 1")
        except Exception:
            logger.warning("DB connection lost, reconnecting...")
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None
            self._connect_db()

    def _create_table(self):
        self._ensure_connection()
        if not self.conn:
            return
        try:
            with self.conn:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS traffic_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP NOT NULL,
                        sent_bytes_diff INTEGER NOT NULL,
                        received_bytes_diff INTEGER NOT NULL,
                        raw_sent_bytes INTEGER NOT NULL,
                        raw_received_bytes INTEGER NOT NULL
                    )
                """)
                self.conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_traffic_logs_timestamp
                    ON traffic_logs(timestamp)
                """)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS notified_alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        alert_date TEXT NOT NULL,
                        threshold_mb INTEGER NOT NULL
                    )
                """)
                self.conn.execute("""
                    CREATE UNIQUE INDEX IF NOT EXISTS idx_notified_alerts_date_threshold
                    ON notified_alerts(alert_date, threshold_mb)
                """)
            logger.info("Database tables are ready")
        except Exception as e:
            logger.error(f"Table creation error: {e}")
            self._rollback()

    def _rollback(self):
        if self.conn:
            try:
                self.conn.rollback()
            except Exception:
                pass

    def discover_device(self):
        logger.info(f"Attempting to connect to '{self.device_name}' with service type '{self.service_type}'...")
        try:
            devices = upnpclient.discover()
        except Exception as e:
            logger.error(f"UPnP discovery error: {e}")
            return False

        for device in devices:
            if (
                "InternetGatewayDevice" in device.device_type
                and device.friendly_name == self.device_name
            ):
                logger.info(f"Router found: {device.friendly_name}")
                self.device = device

                for svc in device.services:
                    if svc.service_type == self.service_type:
                        self.service = svc
                        logger.info(f"Service bound by type: {svc.service_type}")
                        self._init_last_raw()
                        return True

                logger.warning(
                    f"Router found but no service matching type '{self.service_type}'. "
                    f"Available: {[s.service_type for s in device.services]}"
                )
                return False

        logger.warning(f"Router '{self.device_name}' not found")
        return False

    def _init_last_raw(self):
        raw = self.get_raw_traffic()
        if raw:
            self.last_raw_sent = raw["sent_bytes"]
            self.last_raw_received = raw["received_bytes"]
            logger.info(
                f"Init raw counters: sent={self.last_raw_sent}, recv={self.last_raw_received}"
            )

    def get_raw_traffic(self):
        if not self.service:
            logger.warning("UPnP service not initialized")
            return None
        try:
            resp_recv = getattr(self.service, self.action_received)()
            received = int(list(resp_recv.values())[0])

            resp_sent = getattr(self.service, self.action_sent)()
            sent = int(list(resp_sent.values())[0])

            return {"sent_bytes": sent, "received_bytes": received}
        except Exception as e:
            logger.error(f"Error reading from router: {e}")
            return None

    @staticmethod
    def _calc_diff(current, previous):
        if current < previous:
            return MAX_UI4 - previous + current + 1
        return current - previous

    def get_adjusted_traffic(self):
        self._ensure_connection()
        if not self.conn:
            return None

        raw = self.get_raw_traffic()
        if not raw:
            return None

        curr_sent = raw["sent_bytes"]
        curr_received = raw["received_bytes"]

        if self.last_raw_sent is None or self.last_raw_received is None:
            self._init_last_raw()
            total = self._get_total_from_db()
            return {"sent_mb": total["sent_mb"], "received_mb": total["received_mb"]}

        diff_sent = self._calc_diff(curr_sent, self.last_raw_sent)
        diff_received = self._calc_diff(curr_received, self.last_raw_received)

        total = self._get_total_from_db()
        return {
            "sent_mb": (total["sent_bytes"] + diff_sent) / (1024 * 1024),
            "received_mb": (total["received_bytes"] + diff_received) / (1024 * 1024),
        }

    def _get_total_from_db(self):
        self._ensure_connection()
        empty = {"sent_bytes": 0, "received_bytes": 0, "sent_mb": 0.0, "received_mb": 0.0}
        if not self.conn:
            return empty
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT
                    COALESCE(SUM(sent_bytes_diff), 0) as total_sent,
                    COALESCE(SUM(received_bytes_diff), 0) as total_received
                FROM traffic_logs
            """)
            row = cur.fetchone()
            sent = int(row["total_sent"]) if row["total_sent"] else 0
            recv = int(row["total_received"]) if row["total_received"] else 0
            return {
                "sent_bytes": sent,
                "received_bytes": recv,
                "sent_mb": sent / (1024 * 1024),
                "received_mb": recv / (1024 * 1024),
            }
        except Exception as e:
            logger.error(f"Error fetching sum from DB: {e}")
            self._rollback()
            return empty

    def get_traffic_for_period(self, start_time):
        self._ensure_connection()
        if not self.conn:
            return None
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT
                    COALESCE(SUM(sent_bytes_diff), 0) as total_sent,
                    COALESCE(SUM(received_bytes_diff), 0) as total_received
                FROM traffic_logs
                WHERE timestamp >= ?
            """, (start_time,))
            row = cur.fetchone()
            sent = int(row["total_sent"]) if row["total_sent"] else 0
            recv = int(row["total_received"]) if row["total_received"] else 0
            return {
                "sent_bytes": sent,
                "received_bytes": recv,
                "sent_mb": sent / (1024 * 1024),
                "received_mb": recv / (1024 * 1024),
            }
        except Exception as e:
            logger.error(f"Error fetching traffic for period: {e}")
            self._rollback()
            return None

    def log_to_db(self):
        self._ensure_connection()
        if not self.conn:
            return

        raw = self.get_raw_traffic()
        if not raw:
            return

        curr_sent = raw["sent_bytes"]
        curr_received = raw["received_bytes"]

        if self.last_raw_sent is None or self.last_raw_received is None:
            self.last_raw_sent = curr_sent
            self.last_raw_received = curr_received
            logger.info("First log entry - raw counters initialized")
            return

        diff_sent = self._calc_diff(curr_sent, self.last_raw_sent)
        diff_received = self._calc_diff(curr_received, self.last_raw_received)

        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO traffic_logs
                    (timestamp, sent_bytes_diff, received_bytes_diff,
                     raw_sent_bytes, raw_received_bytes)
                    VALUES (?, ?, ?, ?, ?)
                """, (datetime.now(), diff_sent, diff_received,
                      curr_sent, curr_received))

            self.last_raw_sent = curr_sent
            self.last_raw_received = curr_received

            logger.info(
                f"Logged diff: sent={diff_sent / 1024 / 1024:.2f}MB, "
                f"recv={diff_received / 1024 / 1024:.2f}MB"
            )
        except Exception as e:
            logger.error(f"DB log error: {e}")
            self._rollback()

    def start_logging(self, interval_minutes=5):
        def loop():
            while True:
                try:
                    self.log_to_db()
                except Exception as e:
                    logger.error(f"Error in logging loop: {e}")
                time.sleep(interval_minutes * 60)

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()
        logger.info(f"Background logger started (interval {interval_minutes} min)")

    def get_speed(self, interval=10):
        raw1 = self.get_raw_traffic()
        if not raw1:
            return None

        time.sleep(interval)

        raw2 = self.get_raw_traffic()
        if not raw2:
            return None

        sent_diff = self._calc_diff(raw2["sent_bytes"], raw1["sent_bytes"])
        received_diff = self._calc_diff(raw2["received_bytes"], raw1["received_bytes"])

        return {
            "upload_mbps": (sent_diff * 8) / (interval * 1_000_000),
            "download_mbps": (received_diff * 8) / (interval * 1_000_000),
            "sent_diff_mb": sent_diff / (1024 * 1024),
            "received_diff_mb": received_diff / (1024 * 1024),
        }

    def get_notified_thresholds(self, alert_date: str) -> set[int]:
        self._ensure_connection()
        if not self.conn:
            return set()
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT threshold_mb FROM notified_alerts WHERE alert_date = ?
            """, (alert_date,))
            rows = cur.fetchall()
            return {int(row["threshold_mb"]) for row in rows}
        except Exception as e:
            logger.error(f"Error reading notified alerts: {e}")
            self._rollback()
            return set()

    def add_notified_threshold(self, alert_date: str, threshold_mb: int):
        self._ensure_connection()
        if not self.conn:
            return
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT OR IGNORE INTO notified_alerts (alert_date, threshold_mb)
                    VALUES (?, ?)
                """, (alert_date, threshold_mb))
            logger.info(f"Saved notified threshold to DB: {alert_date} - {threshold_mb}MB")
        except Exception as e:
            logger.error(f"Error saving notified alert: {e}")
            self._rollback()

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                logger.info("DB connection closed")
            except Exception:
                pass
