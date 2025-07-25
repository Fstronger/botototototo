import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

from handlers.quote_handler import handle_q
from handlers.weather_handler import handle_weather
from handlers.phrase_handler import handle_phrases
from handlers.affirmation_handler import handle_affirmation
from handlers.cat_handler import handle_cat
from handlers.help_handler import handle_help
# from handlers.balodya_handler import handle_volodya

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    print("✅ Бот запущен!")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("q", handle_q))
    app.add_handler(CommandHandler("w", handle_weather))
    app.add_handler(CommandHandler("a", handle_affirmation))
    app.add_handler(CommandHandler("cat", handle_cat))
    app.add_handler(CommandHandler("h", handle_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phrases))
    # app.add_handler(CommandHandler("v", handle_volodya))

    app.run_polling()

if __name__ == "__main__":
    main()
