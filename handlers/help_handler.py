# handlers/help_handler.py

from telegram import Update
from telegram.ext import ContextTypes

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "**Команды TOTOбота:**\n\n"
        "/q — сделать цитату из последнего сообщения. Создается через реплай\n"
        "/w — показать текущую погоду в заданном городе\n"
        "/a — твоя аффирмация дня (обновляется раз в 24 часа)\n"
        "/cat — твой котик дня (обновляется раз в 24 часа)\n"
        "/h — список всех доступных команд\n"
    )
    await update.message.reply_text(message, parse_mode="Markdown")
