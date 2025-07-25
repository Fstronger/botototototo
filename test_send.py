import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = -1002849329220  # твой канал

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(chat_id=CHAT_ID, text="✅ Тестовое сообщение из скрипта. Бот работает!")
        print("✅ УСПЕШНО: сообщение отправлено")
    except Exception as e:
        print("❌ ОШИБКА при отправке:", e)

if __name__ == "__main__":
    asyncio.run(main())
