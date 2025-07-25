import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
import asyncio

# Загружаем токен
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = -1002849329220

# Локальный файл логов
LOG_FILE = "logs/bot.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_event(event_type: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [{event_type}] {message}"

    # Пишем в файл
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

    # Пытаемся отправить в Telegram
    try:
        asyncio.run(send_to_telegram(formatted))
    except RuntimeError:
        # Если уже запущен event loop (внутри бота), используем create_task
        try:
            asyncio.create_task(send_to_telegram(formatted))
        except Exception as e:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[ERROR] Telegram send task failed: {e}\n")

async def send_to_telegram(text: str):
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[ERROR] Telegram send failed: {e}\n")
