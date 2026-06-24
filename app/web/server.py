"""
Flask API server serving traffic stats and the dashboard.
"""
import os
import calendar
import logging
from datetime import datetime
import sqlite3
from flask import Flask, jsonify, render_template

from app.core.config import DB_PATH, MONTHLY_LIMIT_GB, FLASK_HOST, FLASK_PORT, LOG_INTERVAL_MINUTES, LANGUAGE
from app.core.locale import LOCALES

logger = logging.getLogger(__name__)

# Resolve templates directory relative to this file so it works from any CWD
_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
app = Flask(__name__, template_folder=_TEMPLATES_DIR)

def get_db_data():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        cur = conn.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(sent_bytes_diff + received_bytes_diff), 0)
            FROM traffic_logs
            WHERE timestamp >= ?
        """, (month_start,))
        month_bytes = cur.fetchone()[0]

        cur.execute("""
            SELECT COALESCE(SUM(sent_bytes_diff + received_bytes_diff), 0)
            FROM traffic_logs
            WHERE timestamp >= ?
        """, (day_start,))
        day_bytes = cur.fetchone()[0]

        return month_bytes, day_bytes
    except Exception as e:
        logger.error(f"DB Error: {e}")
        return 0, 0
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

@app.route("/", methods=["GET"])
def index():
    refresh_interval_seconds = int((LOG_INTERVAL_MINUTES * 60) / 2)
    lang = LANGUAGE if LANGUAGE in LOCALES else "en"
    return render_template(
        "dashboard.html",
        refresh_interval_seconds=refresh_interval_seconds,
        t=LOCALES[lang]
    )

@app.route("/traffic", methods=["GET"])
def get_traffic():
    month_bytes, day_bytes = get_db_data()
    month_gb = month_bytes / (1024 ** 3)
    day_gb = day_bytes / (1024 ** 3)

    now = datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    day_limit = MONTHLY_LIMIT_GB / days_in_month

    return jsonify({
        "month_gb": round(month_gb, 2),
        "month_limit": MONTHLY_LIMIT_GB,
        "day_gb": round(day_gb, 2),
        "day_limit": round(day_limit, 2),
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

def run_server():
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_server()
