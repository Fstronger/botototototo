from telegram import Update
from telegram.ext import ContextTypes
from services.image_generator import generate_quote_image
from utils.logger import log_event

async def handle_q(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Ответьте на сообщение, чтобы создать цитату.")
        return

    image = await generate_quote_image(update, context)
    if image:
        await update.message.reply_photo(photo=image)

    img = await generate_quote_image(update, context)
    text = update.message.reply_to_message.text or "<медиа>"
    user = update.message.reply_to_message.from_user
    log_event("QUOTE", f"Создана картинка по тексту: “{text}” от {user.full_name}")

