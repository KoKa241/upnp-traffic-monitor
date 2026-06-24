"""
Interactive Command Line Setup Wizard.
Supports EN / RU / UK. Optionally installs a systemd service for autostart on Raspberry Pi OS.
"""
import os
import time
import sys
import subprocess
import requests
import upnpclient

SETUP_LOCALES = {
    "en": {
        "welcome": "Welcome to Traffic Monitor Setup Wizard!",
        "step_discover": "\n[Step 1] Discovering UPnP devices...",
        "err_discover": "Error discovering devices: {}",
        "no_devices": "No UPnP devices found. Make sure UPnP is enabled on your router.",
        "found_devices": "\nFound devices:",
        "choose_router": "\nSelect your router number: ",
        "invalid_num": "Invalid number.",
        "enter_num": "Please enter a number.",
        "selected_router": "\nSelected router: {}",
        "step_service": "\n[Step 2] Select monitoring service...",
        "no_services": "No available services found on this device.",
        "avail_services": "Available services:",
        "choose_service": "\nSelect service number (usually contains WANCommonInterfaceConfig): ",
        "selected_service": "\nSelected service type: {}",
        "service_recommended": "★ Recommended (standard WANCommonInterfaceConfig:1)",
        "avail_actions_service": "\nAvailable actions for this service:",
        "choose_received": "\nAction for RECEIVED traffic [default {}]: ",
        "choose_sent": "Action for SENT traffic [default {}]: ",
        "actions_set": "\nActions set:\n  Received: {}\n  Sent: {}",
        "step_bot": "\n[Step 3] Configure Telegram Bot...",
        "bot_instructions": "Create a bot via @BotFather in Telegram if you don't have one.",
        "enter_token": "Enter your bot token: ",
        "step_chat_id": "\n[Step 4] Fetching Chat ID...",
        "chat_id_instructions": "Send any message to your bot in Telegram right now.",
        "waiting_msg": "Waiting for message...",
        "chat_id_success": "Chat ID retrieved: {}",
        "chat_id_fail": "Could not retrieve message. Send /start to your bot after launching the application.",
        "step_dashboard": "\n[Step 5] Enable Web Dashboard?",
        "ask_dashboard": "Enable the Web Dashboard? (y/n) [default y]: ",
        "ask_monthly_limit": "Enter monthly traffic limit in GB [default 250.0]: ",
        "step_systemd": "\n[Step 6] Autostart on boot (systemd)?",
        "ask_systemd": "Create a systemd service to start on boot? (Skip if using Docker) (y/n) [default n]: ",
        "systemd_no_linux": "Skipping: not running on Linux.",
        "systemd_no_sudo": "Skipping: sudo is required to install a systemd service.",
        "systemd_ok": "✅ systemd service 'traffic-monitor' installed and enabled.\n   Manage with: sudo systemctl start/stop/status traffic-monitor",
        "systemd_fail": "Failed to install systemd service: {}",
        "step_save": "\n[Step 7] Saving configuration...",
        "env_updated": "File .env updated.",
        "success": "\n✅ Setup completed!\nStart the application with:\n  python main.py\n  -- or --\n  sudo systemctl start traffic-monitor  (if systemd was configured)",
    },
    "ru": {
        "welcome": "Добро пожаловать в Traffic Monitor Setup Wizard!",
        "step_discover": "\n[Шаг 1] Поиск UPnP устройств...",
        "err_discover": "Ошибка при поиске устройств: {}",
        "no_devices": "UPnP устройства не найдены. Убедитесь, что UPnP включен на вашем роутере.",
        "found_devices": "\nНайденные устройства:",
        "choose_router": "\nВыберите номер вашего роутера: ",
        "invalid_num": "Неверный номер.",
        "enter_num": "Введите число.",
        "selected_router": "\nВы выбрали роутер: {}",
        "step_service": "\n[Шаг 2] Выбор сервиса мониторинга...",
        "no_services": "У данного устройства не найдено доступных сервисов.",
        "avail_services": "Доступные сервисы:",
        "choose_service": "\nВыберите номер сервиса (обычно содержит WANCommonInterfaceConfig): ",
        "selected_service": "\nВы выбрали тип сервиса: {}",
        "service_recommended": "★ Рекомендуется (стандартный WANCommonInterfaceConfig:1)",
        "avail_actions_service": "\nДоступные действия для этого сервиса:",
        "choose_received": "\nДействие для ВХОДЯЩЕГО трафика [по умолчанию {}]: ",
        "choose_sent": "Действие для ИСХОДЯЩЕГО трафика [по умолчанию {}]: ",
        "actions_set": "\nУстановлены действия:\n  Received: {}\n  Sent: {}",
        "step_bot": "\n[Шаг 3] Настройка Telegram-бота...",
        "bot_instructions": "Создайте бота через @BotFather в Telegram, если у вас его ещё нет.",
        "enter_token": "Введите токен вашего бота: ",
        "step_chat_id": "\n[Шаг 4] Получение Chat ID...",
        "chat_id_instructions": "Отправьте любое сообщение вашему боту в Telegram прямо сейчас.",
        "waiting_msg": "Ожидание сообщения...",
        "chat_id_success": "Chat ID получен: {}",
        "chat_id_fail": "Не удалось получить сообщение. Отправьте /start вашему боту после запуска приложения.",
        "step_dashboard": "\n[Шаг 5] Включить Веб-Дашборд?",
        "ask_dashboard": "Включить веб-дашборд? (y/n) [по умолчанию y]: ",
        "ask_monthly_limit": "Введите месячный лимит трафика в ГБ [по умолчанию 250.0]: ",
        "step_systemd": "\n[Шаг 6] Автозапуск при загрузке (systemd)?",
        "ask_systemd": "Создать systemd-службу для автозапуска? (Пропустите, если используете Docker) (y/n) [по умолчанию n]: ",
        "systemd_no_linux": "Пропуск: не Linux-система.",
        "systemd_no_sudo": "Пропуск: для установки службы нужен sudo.",
        "systemd_ok": "✅ Служба 'traffic-monitor' установлена и включена в systemd.\n   Управление: sudo systemctl start/stop/status traffic-monitor",
        "systemd_fail": "Не удалось установить службу: {}",
        "step_save": "\n[Шаг 7] Сохранение конфигурации...",
        "env_updated": "Файл .env обновлен.",
        "success": "\n✅ Установка завершена!\nЗапустите приложение командой:\n  python main.py\n  -- или --\n  sudo systemctl start traffic-monitor  (если служба была настроена)",
    },
    "uk": {
        "welcome": "Ласкаво просимо до Traffic Monitor Setup Wizard!",
        "step_discover": "\n[Крок 1] Пошук UPnP пристроїв...",
        "err_discover": "Помилка при пошуку пристроїв: {}",
        "no_devices": "UPnP пристрої не знайдені. Переконайтеся, що UPnP увімкнено на вашому роутері.",
        "found_devices": "\nЗнайдені пристрої:",
        "choose_router": "\nОберіть номер вашого роутера: ",
        "invalid_num": "Невірний номер.",
        "enter_num": "Введіть число.",
        "selected_router": "\nВи обрали роутер: {}",
        "step_service": "\n[Крок 2] Вибір сервісу моніторингу...",
        "no_services": "У цього пристрою не знайдено доступних сервісів.",
        "avail_services": "Доступні сервіси:",
        "choose_service": "\nОберіть номер сервісу (зазвичай містить WANCommonInterfaceConfig): ",
        "selected_service": "\nВи обрали тип сервісу: {}",
        "service_recommended": "★ Рекомендується (стандартний WANCommonInterfaceConfig:1)",
        "avail_actions_service": "\nДоступні дії для цього сервісу:",
        "choose_received": "\nДія для ВХІДНОГО трафіку [типово {}]: ",
        "choose_sent": "Дія для ВИХІДНОГО трафіку [типово {}]: ",
        "actions_set": "\nВстановлено дії:\n  Received: {}\n  Sent: {}",
        "step_bot": "\n[Крок 3] Налаштування Telegram-бота...",
        "bot_instructions": "Створіть бота через @BotFather в Telegram, якщо у вас його ще немає.",
        "enter_token": "Введіть токен вашого бота: ",
        "step_chat_id": "\n[Крок 4] Отримання Chat ID...",
        "chat_id_instructions": "Надішліть будь-яке повідомлення вашому боту в Telegram просто зараз.",
        "waiting_msg": "Очікування повідомлення...",
        "chat_id_success": "Chat ID отримано: {}",
        "chat_id_fail": "Не вдалося отримати повідомлення. Надішліть /start вашому боту після запуску додатку.",
        "step_dashboard": "\n[Крок 5] Увімкнути Веб-Дашборд?",
        "ask_dashboard": "Увімкнути веб-дашборд? (y/n) [типово y]: ",
        "ask_monthly_limit": "Введіть місячний ліміт трафіку в ГБ [за замовчуванням 250.0]: ",
        "step_systemd": "\n[Крок 6] Автозапуск при завантаженні (systemd)?",
        "ask_systemd": "Створити systemd-службу для автозапуску? (Пропустіть, якщо використовуєте Docker) (y/n) [типово n]: ",
        "systemd_no_linux": "Пропуск: не Linux-система.",
        "systemd_no_sudo": "Пропуск: для встановлення служби потрібен sudo.",
        "systemd_ok": "✅ Службу 'traffic-monitor' встановлено та увімкнено в systemd.\n   Керування: sudo systemctl start/stop/status traffic-monitor",
        "systemd_fail": "Не вдалося встановити службу: {}",
        "step_save": "\n[Крок 7] Збереження конфігурації...",
        "env_updated": "Файл .env оновлено.",
        "success": "\n✅ Встановлення завершено!\nЗапустіть додаток командою:\n  python main.py\n  -- або --\n  sudo systemctl start traffic-monitor  (якщо службу було налаштовано)",
    },
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def install_systemd_service(work_dir: str, python_exec: str, t: dict) -> bool:
    """Write a systemd unit file and enable it. Requires sudo."""
    service_name = "traffic-monitor"
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
User={os.environ.get('SUDO_USER', 'pi')}

[Install]
WantedBy=multi-user.target
"""
    unit_path = f"/etc/systemd/system/{service_name}.service"
    try:
        # Write unit file via sudo tee
        proc = subprocess.run(
            ["sudo", "tee", unit_path],
            input=unit_content.encode(),
            capture_output=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.decode())

        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True, capture_output=True)
        subprocess.run(["sudo", "systemctl", "enable", service_name], check=True, capture_output=True)

        print(t["systemd_ok"])
        return True
    except Exception as e:
        print(t["systemd_fail"].format(e))
        return False


def main():
    clear_screen()
    print("┌─────────────────────────────────────────────────────┐")
    print("│               TRAFFIC MONITOR                       │")
    print("│                   by KoKa                           │")
    print("└─────────────────────────────────────────────────────┘")
    print("Select Setup Language / Выберите язык / Оберіть мову:")
    print("1. English (en)")
    print("2. Русский (ru)")
    print("3. Українська (uk)")
    print("=" * 55)

    lang_choice = "en"
    while True:
        choice = input("Enter choice (1-3) [default 1]: ").strip()
        if not choice or choice == "1":
            lang_choice = "en"
            break
        elif choice == "2":
            lang_choice = "ru"
            break
        elif choice == "3":
            lang_choice = "uk"
            break

    t = SETUP_LOCALES[lang_choice]

    clear_screen()
    print("┌─────────────────────────────────────────────────────┐")
    print("│               TRAFFIC MONITOR                       │")
    print("│                   by KoKa                           │")
    print("└─────────────────────────────────────────────────────┘")
    print(t["welcome"])
    print("=" * 55)

    # ── Step 1: Discover UPnP devices ────────────────────────────
    print(t["step_discover"])
    try:
        devices = upnpclient.discover()
    except Exception as e:
        print(t["err_discover"].format(e))
        return

    if not devices:
        print(t["no_devices"])
        return

    print(t["found_devices"])
    for i, d in enumerate(devices):
        print(f"  {i+1}. {d.friendly_name}  [{d.device_type}]")

    while True:
        try:
            choice = int(input(t["choose_router"]))
            if 1 <= choice <= len(devices):
                selected_device = devices[choice - 1]
                break
            else:
                print(t["invalid_num"])
        except ValueError:
            print(t["enter_num"])

    router_name = selected_device.friendly_name
    print(t["selected_router"].format(router_name))

    # ── Step 2: Select service & actions ─────────────────────────
    print(t["step_service"])
    services = selected_device.services
    if not services:
        print(t["no_services"])
        return

    RECOMMENDED_TYPE = "urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1"

    print(t["avail_services"])
    for i, s in enumerate(services):
        actions = [a.name for a in s.actions]
        is_recommended = s.service_type == RECOMMENDED_TYPE
        tag = f"  {t['service_recommended']}" if is_recommended else ""
        print(f"\n  {i+1}. {s.service_type}{tag}")
        print(f"     Actions: {', '.join(actions)}")

    while True:
        try:
            choice = int(input(t["choose_service"]))
            if 1 <= choice <= len(services):
                selected_service = services[choice - 1]
                selected_service_type = selected_service.service_type
                break
            else:
                print(t["invalid_num"])
        except ValueError:
            print(t["enter_num"])

    print(t["selected_service"].format(selected_service_type))

    print(t["avail_actions_service"])
    actions = [a.name for a in selected_service.actions]
    for i, a in enumerate(actions):
        print(f"  {i+1}. {a}")

    action_received = "GetTotalBytesReceived"
    action_sent = "GetTotalBytesSent"

    ans = input(t["choose_received"].format(action_received)).strip()
    if ans.isdigit() and 1 <= int(ans) <= len(actions):
        action_received = actions[int(ans) - 1]

    ans = input(t["choose_sent"].format(action_sent)).strip()
    if ans.isdigit() and 1 <= int(ans) <= len(actions):
        action_sent = actions[int(ans) - 1]

    print(t["actions_set"].format(action_received, action_sent))

    # ── Step 3: Telegram bot token ────────────────────────────────
    print(t["step_bot"])
    print(t["bot_instructions"])
    bot_token = input(t["enter_token"]).strip()

    # ── Step 4: Poll for chat_id ──────────────────────────────────
    print(t["step_chat_id"])
    print(t["chat_id_instructions"])

    chat_id = None
    print(t["waiting_msg"], end="", flush=True)

    for _ in range(30):
        try:
            url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
            resp = requests.get(url, params={"timeout": 2}, timeout=5)
            data = resp.json()
            if data.get("ok") and data.get("result"):
                for update in reversed(data["result"]):
                    if "message" in update:
                        chat_id = update["message"]["chat"]["id"]
                        break
            if chat_id:
                break
        except Exception:
            pass
        print(".", end="", flush=True)
        time.sleep(2)

    print()
    if chat_id:
        print(t["chat_id_success"].format(chat_id))
    else:
        print(t["chat_id_fail"])

    # ── Step 5: Web Dashboard ─────────────────────────────────────
    print(t["step_dashboard"])
    enable_dashboard = "true"
    ans = input(t["ask_dashboard"]).strip().lower()
    if ans in ("n", "no"):
        enable_dashboard = "false"

    monthly_limit = "250.0"
    limit_ans = input(t["ask_monthly_limit"]).strip()
    if limit_ans:
        try:
            monthly_limit = str(float(limit_ans))
        except ValueError:
            print("Invalid value. Using default 250.0 GB.")

    # ── Step 6: systemd autostart ─────────────────────────────────
    print(t["step_systemd"])
    ans = input(t["ask_systemd"]).strip().lower()
    if ans in ("y", "yes"):
        if sys.platform != "linux":
            print(t["systemd_no_linux"])
        else:
            # Check that sudo is available (quick test)
            check = subprocess.run(["sudo", "-n", "true"], capture_output=True)
            if check.returncode != 0:
                print(t["systemd_no_sudo"])
            else:
                work_dir = os.path.abspath(".")
                python_exec = sys.executable
                install_systemd_service(work_dir, python_exec, t)

    # ── Step 7: Save config ───────────────────────────────────────
    print(t["step_save"])

    def safe(v):
        return str(v or "").replace("\n", "").replace("\r", "")

    env_content = f"""# Telegram
TELEGRAM_TOKEN={safe(bot_token)}
TG_CHAT_ID={safe(chat_id) if chat_id else ""}

# Database
DB_PATH=data/traffic.db

# Router
ROUTER_NAME={safe(router_name)}
UPNP_SERVICE_TYPE={safe(selected_service_type)}
UPNP_ACTION_RECEIVED={safe(action_received)}
UPNP_ACTION_SENT={safe(action_sent)}

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5005
ENABLE_WEB_DASHBOARD={safe(enable_dashboard)}

# Localization
LANGUAGE={safe(lang_choice)}

# Traffic Limits
MONTHLY_LIMIT_GB={safe(monthly_limit)}
"""
    with open(".env", "w") as f:
        f.write(env_content)
    print(t["env_updated"])

    print(t["success"])


if __name__ == "__main__":
    main()
