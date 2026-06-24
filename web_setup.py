"""
Web-based Setup Wizard (Flask, port 5001).
"""
import os
import sys
import socket
import subprocess
import threading
import requests
import upnpclient
from flask import Flask, render_template, jsonify, request

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a public DNS IP (doesn't send any data) to trigger routing
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Resolve templates relative to this file so CWD doesn't matter
_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "app", "web", "templates")
_STATIC_DIR = os.path.join(os.path.dirname(__file__), "app", "web", "static")
app = Flask(__name__, template_folder=_TEMPLATES_DIR, static_folder=_STATIC_DIR)

# Holds discovered devices between wizard steps
discovered_devices = []
discovered_devices_lock = threading.Lock()


@app.route("/")
def index():
    return render_template("setup.html")


@app.route("/api/discover", methods=["GET"])
def discover():
    global discovered_devices
    try:
        devices = upnpclient.discover()
        with discovered_devices_lock:
            discovered_devices = devices
            device_list = [
                {"id": i, "name": d.friendly_name, "type": d.device_type}
                for i, d in enumerate(discovered_devices)
            ]
        return jsonify({"success": True, "devices": device_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/services", methods=["GET"])
def get_services():
    device_id = request.args.get("device_id", type=int)
    with discovered_devices_lock:
        if device_id is None or device_id >= len(discovered_devices):
            return jsonify({"success": False, "error": "Invalid device ID"})
        device = discovered_devices[device_id]

    RECOMMENDED_TYPE = "urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1"
    services = [
        {
            "id": i,
            "service_type": s.service_type,
            "service_id": s.service_id,
            "actions": [a.name for a in s.actions],
            "is_recommended": s.service_type == RECOMMENDED_TYPE,
        }
        for i, s in enumerate(device.services)
    ]
    return jsonify({"success": True, "services": services})


@app.route("/api/poll_telegram", methods=["POST"])
def poll_telegram():
    bot_token = (request.json or {}).get("bot_token")
    if not bot_token:
        return jsonify({"success": False, "error": "Bot token missing"})

    try:
        resp = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getUpdates",
            params={"timeout": 2},
            timeout=5,
        )
        for update in reversed(resp.json().get("result") or []):
            if "message" in update:
                return jsonify({"success": True, "chat_id": update["message"]["chat"]["id"]})
        return jsonify({"success": False, "message": "No message received yet"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/install_service", methods=["POST"])
def install_service():
    """Create and enable a systemd unit file. Linux only, requires sudo."""
    if sys.platform != "linux":
        return jsonify({"success": False, "error": "Not a Linux system"})

    check = subprocess.run(["sudo", "-n", "true"], capture_output=True)
    if check.returncode != 0:
        return jsonify({"success": False, "error": "sudo required — run: sudo -v, then retry"})

    work_dir = os.path.abspath(".")
    python_exec = sys.executable
    service_user = os.environ.get("SUDO_USER", "pi")

    unit_content = f"""[Unit]
Description=Traffic Monitor (UPnP + Telegram bot)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory={work_dir}
ExecStart={python_exec} {os.path.join(work_dir, 'main.py')}
Restart=on-failure
RestartSec=10
User={service_user}

[Install]
WantedBy=multi-user.target
"""
    unit_path = "/etc/systemd/system/traffic-monitor.service"
    try:
        proc = subprocess.run(
            ["sudo", "tee", unit_path],
            input=unit_content.encode(),
            capture_output=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.decode())

        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True, capture_output=True)
        subprocess.run(["sudo", "systemctl", "enable", "traffic-monitor"], check=True, capture_output=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/save", methods=["POST"])
def save_config():
    data = request.json or {}
    def safe(v):
        return str(v or "").replace("\n", "").replace("\r", "")
    try:
        env_content = f"""# Telegram
TELEGRAM_TOKEN={safe(data.get('bot_token'))}
TG_CHAT_ID={safe(data.get('chat_id', ''))}

# Database
DB_PATH=data/traffic.db

# Router
ROUTER_NAME={safe(data.get('router_name'))}
UPNP_SERVICE_TYPE={safe(data.get('service_type'))}
UPNP_ACTION_RECEIVED={safe(data.get('action_received'))}
UPNP_ACTION_SENT={safe(data.get('action_sent'))}

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5005
ENABLE_WEB_DASHBOARD={'true' if data.get('enable_dashboard') else 'false'}

# Localization
LANGUAGE={safe(data.get('language', 'en'))}

# Traffic Limits
MONTHLY_LIMIT_GB={safe(data.get('monthly_limit', '250.0'))}
"""
        with open(".env", "w") as f:
            f.write(env_content)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    local_ip = get_local_ip()
    print("=" * 42)
    print("Web Setup Wizard running!")
    print(f"Open in your browser:")
    print(f"  Local:    http://localhost:5001")
    print(f"  Network:  http://{local_ip}:5001")
    print("=" * 42)
    app.run(host="0.0.0.0", port=5001, debug=False)
