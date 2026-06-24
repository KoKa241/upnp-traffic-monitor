"""
Telegram bot for monitoring traffic and sending daily alerts.
"""
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app.core.config import (
    TELEGRAM_TOKEN,
    TG_CHAT_ID,
    DAILY_ALERT_THRESHOLDS_MB,
    SPEED_MEASURE_SECONDS,
    ALERT_CHECK_SECONDS,
    LANGUAGE
)
from app.core.monitor import NetworkMonitor
from app.core.locale import LOCALES

logger = logging.getLogger(__name__)

# Fallback to English if language is not supported
lang_dict = LOCALES.get(LANGUAGE, LOCALES["en"])

async def start_bot(monitor: NetworkMonitor):
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    current_date = datetime.now().date()
    notified_today: set[int] = monitor.get_notified_thresholds(current_date.isoformat())
    last_check_date = current_date

    if TG_CHAT_ID:
        logger.info(f"Using TG_CHAT_ID from environment: {TG_CHAT_ID}")
    else:
        logger.warning("TG_CHAT_ID is not configured in the environment! Alerts will not be sent.")

    async def check_daily_traffic_alerts():
        nonlocal notified_today, last_check_date
        if TG_CHAT_ID is None:
            return

        current_date = datetime.now().date()
        if last_check_date != current_date:
            notified_today = monitor.get_notified_thresholds(current_date.isoformat())
            last_check_date = current_date
            logger.info(f"New day detected: {current_date}, loaded notified thresholds from DB: {notified_today}")

        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        traffic = monitor.get_traffic_for_period(today_start)
        if not traffic:
            return

        total_mb = traffic["sent_mb"] + traffic["received_mb"]
        for threshold in DAILY_ALERT_THRESHOLDS_MB:
            if total_mb >= threshold and threshold not in notified_today:
                threshold_gb = threshold / 1024
                # Use localized text
                alert_text = lang_dict["alert_msg"].format(int(threshold_gb), (total_mb / threshold) * 100)
                try:
                    await bot.send_message(TG_CHAT_ID, alert_text)
                    monitor.add_notified_threshold(current_date.isoformat(), threshold)
                    notified_today.add(threshold)
                    logger.info(f"Alert sent to Telegram: {threshold_gb}GB threshold")
                except Exception as e:
                    logger.error(f"Failed to send Telegram alert: {e}")

    async def monitoring_loop():
        while True:
            try:
                await check_daily_traffic_alerts()
            except Exception as e:
                logger.error(f"Error in monitoring check loop: {e}")
            await asyncio.sleep(ALERT_CHECK_SECONDS)

    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        if TG_CHAT_ID is None or message.chat.id != TG_CHAT_ID:
            logger.warning(f"Unauthorized bot access attempt from chat_id: {message.chat.id}")
            return
        await message.reply(lang_dict["cmd_start"])

    @dp.message(Command("traffic"))
    async def cmd_traffic(message: Message):
        if TG_CHAT_ID is None or message.chat.id != TG_CHAT_ID:
            logger.warning(f"Unauthorized bot access attempt from chat_id: {message.chat.id}")
            return
        adjusted = monitor.get_adjusted_traffic()
        if not adjusted:
            await message.reply(lang_dict["err_get_traffic"])
            return

        total_mb = adjusted["sent_mb"] + adjusted["received_mb"]
        upload_gb = adjusted['sent_mb'] / 1024
        download_gb = adjusted['received_mb'] / 1024
        total_gb = total_mb / 1024
        
        msg = lang_dict["traffic_msg"].format(upload_gb, download_gb, total_gb)
        await message.reply(msg)

    @dp.message(Command("speed"))
    async def cmd_speed(message: Message):
        if TG_CHAT_ID is None or message.chat.id != TG_CHAT_ID:
            logger.warning(f"Unauthorized bot access attempt from chat_id: {message.chat.id}")
            return
        await message.reply(lang_dict["speed_measuring"].format(SPEED_MEASURE_SECONDS))

        speed = await asyncio.to_thread(monitor.get_speed, interval=SPEED_MEASURE_SECONDS)
        if not speed:
            await message.reply(lang_dict["speed_err"])
            return

        msg = lang_dict["speed_msg"].format(
            SPEED_MEASURE_SECONDS,
            speed['upload_mbps'],
            speed['sent_diff_mb'],
            speed['download_mbps'],
            speed['received_diff_mb']
        )
        await message.reply(msg)

    @dp.message(Command("daily"))
    async def cmd_daily(message: Message):
        if TG_CHAT_ID is None or message.chat.id != TG_CHAT_ID:
            logger.warning(f"Unauthorized bot access attempt from chat_id: {message.chat.id}")
            return
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        traffic = monitor.get_traffic_for_period(today_start)
        if not traffic:
            await message.reply(lang_dict["err_get_daily"])
            return

        total_mb = traffic["sent_mb"] + traffic["received_mb"]
        total_gb = total_mb / 1024

        progress = ""
        for threshold in DAILY_ALERT_THRESHOLDS_MB:
            if total_mb < threshold:
                remaining = (threshold - total_mb) / 1024
                progress = lang_dict["daily_remaining"].format(threshold / 1024, remaining)
                break

        msg = lang_dict["daily_msg"].format(
            traffic['sent_mb'] / 1024,
            traffic['received_mb'] / 1024,
            total_gb,
            progress
        )
        await message.reply(msg)

    @dp.message(Command("monthly"))
    async def cmd_monthly(message: Message):
        if TG_CHAT_ID is None or message.chat.id != TG_CHAT_ID:
            logger.warning(f"Unauthorized bot access attempt from chat_id: {message.chat.id}")
            return
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        traffic = monitor.get_traffic_for_period(month_start)
        if not traffic:
            await message.reply(lang_dict["err_get_monthly"])
            return

        total_mb = traffic["sent_mb"] + traffic["received_mb"]
        msg = lang_dict["monthly_msg"].format(
            traffic['sent_mb'] / 1024,
            traffic['received_mb'] / 1024,
            total_mb / 1024
        )

        await message.reply(msg)

    @dp.message(Command("alerts"))
    async def cmd_alerts(message: Message):
        if TG_CHAT_ID is None or message.chat.id != TG_CHAT_ID:
            logger.warning(f"Unauthorized bot access attempt from chat_id: {message.chat.id}")
            return
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        traffic = monitor.get_traffic_for_period(today_start)
        if not traffic:
            await message.reply(lang_dict["err_get_traffic"])
            return

        total_mb = traffic["sent_mb"] + traffic["received_mb"]
        text = lang_dict["cmd_alerts"].format(total_mb / 1024)

        current_date_str = datetime.now().date().isoformat()
        db_notified = monitor.get_notified_thresholds(current_date_str)

        for threshold in DAILY_ALERT_THRESHOLDS_MB:
            thr_gb = threshold / 1024
            if threshold in db_notified:
                text += f"✅ {thr_gb:.0f} GB — {lang_dict['alert_reached']}\n"
            elif total_mb >= threshold:
                text += f"⚠️ {thr_gb:.0f} GB — {lang_dict['alert_passed']}\n"
            else:
                remaining = (threshold - total_mb) / 1024
                text += f"⏳ {thr_gb:.0f} GB — {lang_dict['alert_remaining'].format(remaining)}\n"

        await message.reply(text)

    async def on_startup():
        asyncio.create_task(monitoring_loop())
        logger.info(lang_dict["bot_started"])

    dp.startup.register(on_startup)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
