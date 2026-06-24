# Translation dictionary for multilingual support.
# Supports en, ru, uk.

LOCALES = {
    "en": {
        # Bot strings
        "bot_started": "Bot started, monitoring active",
        "new_day": "New day: {}, resetting notifications",
        "alert_msg": "⚠️ Traffic alert: {} GB reached ({:.1f}% of limit)!",
        "limit_reached": "🚨 Traffic limit reached: {} GB!",
        "cmd_start": "Traffic Monitor Bot. Commands:\n/traffic - Current traffic stats\n/speed - Test internet speed (10s)\n/daily - Detailed stats for today\n/monthly - Detailed stats for current month\n/alerts - Daily threshold status",
        "cmd_alerts": "🔔 Alerts for today:\n\nTraffic: {:.2f} GB\n\n",
        "alert_passed": "reached (skipped notification)",
        "alert_reached": "reached",
        "alert_remaining": "remaining: {:.2f} GB",
        "err_get_traffic": "❌ Error fetching traffic.",
        "traffic_msg": "📊 Current traffic:\n\n⬆️ Upload: {:.2f} GB\n⬇️ Download: {:.2f} GB\n📦 Total: {:.2f} GB",
        "speed_measuring": "⏳ Measuring speed... ({} seconds)",
        "speed_err": "❌ Error calculating speed.",
        "speed_msg": "⚡ Speed (over {}s):\n\n⬆️ Upload: {:.2f} Mbps ({:.2f} MB)\n⬇️ Download: {:.2f} Mbps ({:.2f} MB)",
        "err_get_daily": "❌ Error fetching daily traffic.",
        "daily_remaining": "\n\n📌 Until alert ({:.0f} GB): {:.2f} GB remaining",
        "daily_msg": "📅 Traffic today:\n\n⬆️ Upload: {:.2f} GB\n⬇️ Download: {:.2f} GB\n📦 Total: {:.2f} GB{}",
        "err_get_monthly": "❌ Error fetching monthly traffic.",
        "monthly_msg": "📆 Traffic this month:\n\n⬆️ Upload: {:.2f} GB\n⬇️ Download: {:.2f} GB\n📦 Total: {:.2f} GB",
        
        # Dashboard strings
        "dashboard_title": "Traffic Dashboard",
        "day_traffic": "Day Traffic",
        "month_traffic": "Month Traffic",
        "limit_text": "Limit",
        "next_update": "Next update in:",
        "refresh_now": "Refresh Now",
        "loading": "Loading..."
    },
    "ru": {
        # Bot strings
        "bot_started": "Бот запущен, мониторинг активен",
        "new_day": "Новый день: {}, сброс уведомлений",
        "alert_msg": "⚠️ Лимит трафика: достигнуто {} ГБ ({:.1f}% от лимита)!",
        "limit_reached": "🚨 Лимит трафика исчерпан: {} ГБ!",
        "cmd_start": "Бот мониторинга трафика. Команды:\n/traffic - Текущий трафик\n/speed - Тест скорости интернета (10 сек)\n/daily - Детальная статистика за сегодня\n/monthly - Детальная статистика за месяц\n/alerts - Статус лимитов на сегодня",
        "cmd_alerts": "🔔 Уведомления за сегодня:\n\nТрафик: {:.2f} ГБ\n\n",
        "alert_passed": "достигнуто (пропущено)",
        "alert_reached": "достигнуто",
        "alert_remaining": "осталось {:.2f} ГБ",
        "err_get_traffic": "❌ Ошибка получения трафика.",
        "traffic_msg": "📊 Текущий трафик:\n\n⬆️ Исходящий: {:.2f} ГБ\n⬇️ Входящий: {:.2f} ГБ\n📦 Всего: {:.2f} ГБ",
        "speed_measuring": "⏳ Измеряю скорость... ({} секунд)",
        "speed_err": "❌ Ошибка расчета скорости.",
        "speed_msg": "⚡ Скорость (за {} сек):\n\n⬆️ Исходящая: {:.2f} Мбит/с ({:.2f} МБ)\n⬇️ Входящая: {:.2f} Мбит/с ({:.2f} МБ)",
        "err_get_daily": "❌ Ошибка получения трафика за день.",
        "daily_remaining": "\n\n📌 До уведомления ({:.0f} ГБ): осталось {:.2f} ГБ",
        "daily_msg": "📅 Трафик за сегодня:\n\n⬆️ Исходящий: {:.2f} ГБ\n⬇️ Входящий: {:.2f} ГБ\n📦 Всего: {:.2f} ГБ{}",
        "err_get_monthly": "❌ Ошибка получения трафика за месяц.",
        "monthly_msg": "📆 Трафик за месяц:\n\n⬆️ Исходящий: {:.2f} ГБ\n⬇️ Входящий: {:.2f} ГБ\n📦 Всего: {:.2f} ГБ",

        # Dashboard strings
        "dashboard_title": "Панель управления трафиком",
        "day_traffic": "Трафик за день",
        "month_traffic": "Трафик за месяц",
        "limit_text": "Лимит",
        "next_update": "Следующее обновление через:",
        "refresh_now": "Обновить сейчас",
        "loading": "Загрузка..."
    },
    "uk": {
        # Bot strings
        "bot_started": "Бот запущений, моніторинг активний",
        "new_day": "Новий день: {}, скидання сповіщень",
        "alert_msg": "⚠️ Ліміт трафіку: досягнуто {} ГБ ({:.1f}% від ліміту)!",
        "limit_reached": "🚨 Ліміт трафіку вичерпано: {} ГБ!",
        "cmd_start": "Бот моніторингу трафіку. Команди:\n/traffic - Поточний трафік\n/speed - Тест швидкості інтернету (10 сек)\n/daily - Детальна статистика за сьогодні\n/monthly - Детальна статистика за місяць\n/alerts - Статус лімітів на сьогодні",
        "cmd_alerts": "🔔 Сповіщення за сьогодні:\n\nТрафік: {:.2f} ГБ\n\n",
        "alert_passed": "досягнуто (пропущено)",
        "alert_reached": "досягнуто",
        "alert_remaining": "залишилось {:.2f} ГБ",
        "err_get_traffic": "❌ Помилка отримання трафіку.",
        "traffic_msg": "📊 Поточний трафік:\n\n⬆️ Вихідний: {:.2f} ГБ\n⬇️ Вхідний: {:.2f} ГБ\n📦 Всього: {:.2f} ГБ",
        "speed_measuring": "⏳ Вимірюю швидкість... ({} секунд)",
        "speed_err": "❌ Помилка розрахунку швидкості.",
        "speed_msg": "⚡ Швидкість (за {} сек):\n\n⬆️ Вихідна: {:.2f} Мбіт/с ({:.2f} МБ)\n⬇️ Вхідна: {:.2f} Мбіт/с ({:.2f} МБ)",
        "err_get_daily": "❌ Помилка отримання трафіку за день.",
        "daily_remaining": "\n\n📌 До сповіщення ({:.0f} ГБ): залишилось {:.2f} ГБ",
        "daily_msg": "📅 Трафік за сьогодні:\n\n⬆️ Вихідний: {:.2f} ГБ\n⬇️ Вхідний: {:.2f} ГБ\n📦 Всього: {:.2f} ГБ{}",
        "err_get_monthly": "❌ Помилка отримання трафіку за місяць.",
        "monthly_msg": "📆 Трафік за місяць:\n\n⬆️ Вихідний: {:.2f} ГБ\n⬇️ Вхідний: {:.2f} ГБ\n📦 Всього: {:.2f} ГБ",

        # Dashboard strings
        "dashboard_title": "Панель керування трафіком",
        "day_traffic": "Трафик за день",
        "month_traffic": "Трафик за місяць",
        "limit_text": "Лимит",
        "next_update": "Наступне оновлення через:",
        "refresh_now": "Оновити зараз",
        "loading": "Завантаження..."
    }
}
