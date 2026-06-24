const translations = {
    en: {
        title_main: "🚀 Setup Wizard",
        step1_title: "Step 1: Router Discovery",
        step1_desc: "Searching for UPnP-enabled gateway devices in your local network...",
        btn_discover: "Discover Devices",
        choose_router: "Select your router:",
        router_not_found: "No UPnP devices found.",
        step2_title: "Step 2: Monitoring Settings",
        step2_desc: "Select the service that outputs statistics and specify action methods.",
        service_placeholder: "Select service...",
        label_recv: "Action for Received Traffic",
        label_sent: "Action for Sent Traffic",
        btn_next: "Next",
        select_service_alert: "Please select a service",
        service_recommended: "Recommended",
        avail_methods: "Available methods:",
        step3_title: "Step 3: Telegram Setup",
        step3_desc: "Enter your Telegram bot token (you can get one from @BotFather).",
        step3_desc2: "Now send any message to your bot from your Telegram account.",
        btn_poll: "Waiting for message...",
        btn_poll_success: "Success!",
        btn_poll_timeout: "Timeout. Click to try again.",
        enter_token_alert: "Please enter your bot token!",
        chat_id_found: "Chat ID: {id} found!",
        step4_title: "Step 4: Web Dashboard",
        label_dashboard: "Enable Web Dashboard",
        desc_dashboard: "If enabled, visual traffic statistics will be available at the server address (port 5005).",
        label_monthly_limit: "Monthly Traffic Limit (GB)",
        btn_step4_next: "Next",
        step5_title: "Step 5: Autostart on Boot",
        step5_desc: "Install a systemd service so the monitor starts automatically on every boot (Linux / Raspberry Pi OS only). Skip this if using Docker.",
        label_systemd: "Create systemd service",
        desc_systemd: "Requires sudo access on the device running this setup server.",
        systemd_installing: "Installing service...",
        systemd_ok: "✅ Service installed! Use: sudo systemctl start/stop traffic-monitor",
        systemd_fail: "⚠️ Failed: ",
        btn_save: "Save and Finish",
        save_error: "Error saving settings: ",
        step6_title: "✅ Setup Completed!",
        step6_desc: "Configuration settings saved successfully.",
        step6_desc2: "You can close this window and start the application in your terminal:",
        step6_systemd_hint: "sudo systemctl start traffic-monitor"
    },
    ru: {
        title_main: "🚀 Мастер Настройки",
        step1_title: "Шаг 1: Поиск Роутера",
        step1_desc: "Ищем UPnP-устройства в вашей локальной сети...",
        btn_discover: "Найти Устройства",
        choose_router: "Выберите роутер:",
        router_not_found: "Устройства не найдены.",
        step2_title: "Шаг 2: Параметры Мониторинга",
        step2_desc: "Выберите службу, которая отдает трафик, и методы сбора данных.",
        service_placeholder: "Выберите службу...",
        label_recv: "Метод входящего трафика",
        label_sent: "Метод исходящего трафика",
        btn_next: "Далее",
        select_service_alert: "Пожалуйста, выберите службу",
        service_recommended: "Рекомендуется",
        avail_methods: "Доступные методы:",
        step3_title: "Шаг 3: Настройка Telegram",
        step3_desc: "Введите токен вашего бота (получить можно у @BotFather).",
        step3_desc2: "Теперь отправьте любое сообщение вашему боту с вашего Telegram-аккаунта.",
        btn_poll: "Ожидание сообщения...",
        btn_poll_success: "Успешно!",
        btn_poll_timeout: "Время вышло. Нажмите для повтора.",
        enter_token_alert: "Пожалуйста, введите токен бота!",
        chat_id_found: "Chat ID: {id} найден!",
        step4_title: "Шаг 4: Веб-Дашборд",
        label_dashboard: "Включить Веб-Дашборд",
        desc_dashboard: "Если включено, визуальная статистика будет доступна по адресу сервера (порт 5005).",
        label_monthly_limit: "Месячный лимит трафика (ГБ)",
        btn_step4_next: "Далее",
        step5_title: "Шаг 5: Автозапуск при загрузке",
        step5_desc: "Создайте systemd-службу для автоматического запуска при каждой загрузке (только Linux / Raspberry Pi OS). Пропустите, если используете Docker.",
        label_systemd: "Создать systemd-службу",
        desc_systemd: "Требует права sudo на устройстве, где запущен этот мастер настройки.",
        systemd_installing: "Установка службы...",
        systemd_ok: "✅ Служба установлена! Команды: sudo systemctl start/stop traffic-monitor",
        systemd_fail: "⚠️ Ошибка: ",
        btn_save: "Сохранить и Завершить",
        save_error: "Ошибка сохранения: ",
        step6_title: "✅ Настройка Завершена!",
        step6_desc: "Параметры конфигурации успешно сохранены.",
        step6_desc2: "Вы можете закрыть это окно и запустить приложение в терминале:",
        step6_systemd_hint: "sudo systemctl start traffic-monitor"
    },
    uk: {
        title_main: "🚀 Майстер Налаштування",
        step1_title: "Крок 1: Пошук Роутера",
        step1_desc: "Шукаємо пристрої з підтримкою UPnP у вашій локальній мережі...",
        btn_discover: "Знайти Пристрої",
        choose_router: "Оберіть роутер:",
        router_not_found: "Пристрої не знайдені.",
        step2_title: "Крок 2: Параметри Мониторингу",
        step2_desc: "Оберіть службу, яка віддає статистику, та вкажіть методи.",
        service_placeholder: "Оберіть службу...",
        label_recv: "Метод вхідного трафіку",
        label_sent: "Метод вихідного трафіку",
        btn_next: "Далі",
        select_service_alert: "Будь ласка, оберіть службу",
        service_recommended: "Рекомендується",
        avail_methods: "Доступні методи:",
        step3_title: "Крок 3: Налаштування Telegram",
        step3_desc: "Введіть токен вашого бота (отримати можна у @BotFather).",
        step3_desc2: "Тепер надішліть будь-яке повідомлення вашому боту з вашого Telegram-акаунта.",
        btn_poll: "Очікування повідомлення...",
        btn_poll_success: "Успішно!",
        btn_poll_timeout: "Час вийшов. Натисніть для повтору.",
        enter_token_alert: "Будь ласка, введіть токен бота!",
        chat_id_found: "Chat ID: {id} знайдено!",
        step4_title: "Крок 4: Веб-Дашборд",
        label_dashboard: "Увімкнути Веб-Дашборд",
        desc_dashboard: "Якщо увімкнено, візуальна статистика буде доступна за адресою сервера (порт 5005).",
        label_monthly_limit: "Місячний ліміт трафіку (ГБ)",
        btn_step4_next: "Далі",
        step5_title: "Крок 5: Автозапуск при завантаженні",
        step5_desc: "Створіть systemd-службу для автоматического запуску при кожному завантаженні (тільки Linux / Raspberry Pi OS). Пропустіть, якщо використовуєте Docker.",
        label_systemd: "Створити systemd-службу",
        desc_systemd: "Потрібен sudo-доступ на пристрої, де запущено цей майстер налаштування.",
        systemd_installing: "Встановлення служби...",
        systemd_ok: "✅ Службу встановлено! Команды: sudo systemctl start/stop traffic-monitor",
        systemd_fail: "⚠️ Помилка: ",
        btn_save: "Зберегти та Завершити",
        save_error: "Помилка збереження: ",
        step6_title: "✅ Встановлення Завершено!",
        step6_desc: "Параметри конфігурації успішно збережено.",
        step6_desc2: "Ви можете закрити це вікно та запустити додаток у терміналі:",
        step6_systemd_hint: "sudo systemctl start traffic-monitor"
    }
};

let currentLang = "en";

function applyLanguage(lang) {
    currentLang = lang;
    const t = translations[lang];

    document.getElementById('title-main').innerText = t.title_main;
    document.getElementById('step1-title').innerText = t.step1_title;
    document.getElementById('step1-desc').innerText = t.step1_desc;
    document.getElementById('btn-discover').innerText = t.btn_discover;

    document.getElementById('step2-title').innerText = t.step2_title;
    document.getElementById('step2-desc').innerText = t.step2_desc;
    document.getElementById('service-placeholder').innerText = t.service_placeholder;
    document.getElementById('label-recv').innerText = t.label_recv;
    document.getElementById('label-sent').innerText = t.label_sent;
    document.getElementById('btn-step2-next').innerText = t.btn_next;

    document.getElementById('step3-title').innerText = t.step3_title;
    document.getElementById('step3-desc').innerText = t.step3_desc;
    document.getElementById('step3-desc2').innerText = t.step3_desc2;

    const btnPoll = document.getElementById('btn-poll');
    if (!btnPoll.disabled) btnPoll.innerText = t.btn_poll;

    document.getElementById('step4-title').innerText = t.step4_title;
    document.getElementById('label-dashboard').innerText = t.label_dashboard;
    document.getElementById('desc-dashboard').innerText = t.desc_dashboard;
    document.getElementById('label-monthly-limit').innerText = t.label_monthly_limit;
    document.getElementById('btn-step4-next').innerText = t.btn_step4_next;

    document.getElementById('step5-title').innerText = t.step5_title;
    document.getElementById('step5-desc').innerText = t.step5_desc;
    document.getElementById('label-systemd').innerText = t.label_systemd;
    document.getElementById('desc-systemd').innerText = t.desc_systemd;
    document.getElementById('btn-save').innerText = t.btn_save;

    document.getElementById('step6-title').innerText = t.step6_title;
    document.getElementById('step6-desc').innerText = t.step6_desc;
    document.getElementById('step6-desc2').innerText = t.step6_desc2;
}

document.getElementById('lang-select').addEventListener('change', (e) => {
    applyLanguage(e.target.value);
});

let configData = {
    router_name: "",
    service_type: "",
    action_received: "",
    action_sent: "",
    bot_token: "",
    chat_id: "",
    enable_dashboard: true,
    language: "en"
};
let currentServices = [];

function showStep(num) {
    document.querySelectorAll('.step').forEach(el => el.classList.remove('active'));
    document.getElementById('step-' + num).classList.add('active');
}

// Step 1 Discovery
document.getElementById('btn-discover').addEventListener('click', async (e) => {
    e.target.setAttribute('aria-busy', 'true');
    document.getElementById('device-list').innerHTML = '';

    try {
        const res = await fetch('/api/discover');
        const data = await res.json();

        if (data.success && data.devices.length > 0) {
            let html = `<p>${translations[currentLang].choose_router}</p>`;
            data.devices.forEach(d => {
                html += `<button class="secondary outline" onclick="selectDevice(${d.id}, '${d.name}')">${d.name}</button><br>`;
            });
            document.getElementById('device-list').innerHTML = html;
        } else {
            document.getElementById('device-list').innerHTML = `<p style="color:red">${translations[currentLang].router_not_found}</p>`;
        }
    } catch (err) {
        console.error(err);
    }
    e.target.setAttribute('aria-busy', 'false');
});

async function selectDevice(id, name) {
    configData.router_name = name;
    const res = await fetch(`/api/services?device_id=${id}`);
    const data = await res.json();

    if (data.success) {
        currentServices = data.services;
        const select = document.getElementById('service-select');
        select.innerHTML = `<option value="" selected disabled id="service-placeholder">${translations[currentLang].service_placeholder}</option>`;
        data.services.forEach(s => {
            const badge = s.is_recommended ? ` ★ ${translations[currentLang].service_recommended || 'Recommended'}` : '';
            select.innerHTML += `<option value="${s.id}">${s.service_type}${badge}</option>`;
        });
        showStep(2);
    }
}

// Step 2 Services
document.getElementById('service-select').addEventListener('change', (e) => {
    const sId = e.target.value;
    const service = currentServices.find(s => s.id == sId);
    configData.service_type = service.service_type;

    document.getElementById('actions-info').innerHTML = `<div class="action-list">${translations[currentLang].avail_methods}<br>${service.actions.join(', ')}</div>`;

    const recvSelect = document.getElementById('action-recv');
    const sentSelect = document.getElementById('action-sent');
    recvSelect.innerHTML = ''; sentSelect.innerHTML = '';

    service.actions.forEach(a => {
        recvSelect.innerHTML += `<option value="${a}" ${a === 'GetTotalBytesReceived' ? 'selected' : ''}>${a}</option>`;
        sentSelect.innerHTML += `<option value="${a}" ${a === 'GetTotalBytesSent' ? 'selected' : ''}>${a}</option>`;
    });
});

document.getElementById('btn-step2-next').addEventListener('click', () => {
    if (!configData.service_type) return alert(translations[currentLang].select_service_alert);
    configData.action_received = document.getElementById('action-recv').value;
    configData.action_sent = document.getElementById('action-sent').value;
    showStep(3);
});

// Step 3 Telegram Bot
let pollingInterval = null;
document.getElementById('btn-poll').addEventListener('click', async (e) => {
    const token = document.getElementById('bot-token').value;
    if (!token) return alert(translations[currentLang].enter_token_alert);
    configData.bot_token = token;

    e.target.setAttribute('aria-busy', 'true');
    e.target.innerText = translations[currentLang].btn_poll;

    let attempts = 0;
    pollingInterval = setInterval(async () => {
        attempts++;
        if (attempts > 30) {
            clearInterval(pollingInterval);
            e.target.setAttribute('aria-busy', 'false');
            e.target.innerText = translations[currentLang].btn_poll_timeout;
            return;
        }

        try {
            const res = await fetch('/api/poll_telegram', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bot_token: token })
            });
            const data = await res.json();

            if (data.success && data.chat_id) {
                clearInterval(pollingInterval);
                configData.chat_id = data.chat_id;
                document.getElementById('chat-id-result').innerText = translations[currentLang].chat_id_found.replace('{id}', data.chat_id);
                e.target.setAttribute('aria-busy', 'false');
                e.target.innerText = translations[currentLang].btn_poll_success;
                e.target.disabled = true;

                setTimeout(() => showStep(4), 1500);
            }
        } catch (err) { console.error(err); }
    }, 2000);
});

// Step 4 → Step 5
document.getElementById('btn-step4-next').addEventListener('click', () => {
    configData.enable_dashboard = document.getElementById('enable-dashboard').checked;
    configData.monthly_limit = document.getElementById('monthly-limit').value || "250";
    showStep(5);
});

// Step 5: systemd + Save
document.getElementById('btn-save').addEventListener('click', async (e) => {
    e.target.setAttribute('aria-busy', 'true');
    configData.language = currentLang;
    const t = translations[currentLang];

    // Optionally install systemd service
    if (document.getElementById('enable-systemd').checked) {
        document.getElementById('systemd-result').innerText = t.systemd_installing;
        try {
            const sr = await fetch('/api/install_service', { method: 'POST' });
            const sd = await sr.json();
            document.getElementById('systemd-result').innerText = sd.success ? t.systemd_ok : t.systemd_fail + sd.error;
            // Show hint on success page
            if (sd.success) {
                const hint = document.getElementById('step6-systemd-hint');
                hint.style.display = 'block';
                hint.innerHTML = '🖥️ ' + t.step6_systemd_hint;
            }
        } catch (err) {
            document.getElementById('systemd-result').innerText = t.systemd_fail + err;
        }
    }

    try {
        const res = await fetch('/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(configData)
        });
        const data = await res.json();
        if (data.success) {
            showStep(6);
        } else {
            alert(t.save_error + data.error);
        }
    } catch (err) {
        console.error(err);
    }
    e.target.setAttribute('aria-busy', 'false');
});
// Theme switching handler
const themeSelect = document.getElementById('theme-select');
function applyTheme(theme) {
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
    localStorage.setItem('theme', theme);
    themeSelect.value = theme;
}

// Set initial selector state
themeSelect.value = localStorage.getItem('theme') || 'system';
themeSelect.addEventListener('change', (e) => {
    applyTheme(e.target.value);
});

// Initialize language
applyLanguage("en");
