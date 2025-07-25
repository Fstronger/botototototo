# import random
# from telegram import Update
# from telegram.ext import ContextTypes
# from utils.logger import log_event

# REPLIES = [
#     "Пилит фичу за 500 тг",
#     "На созвоне с клиентом",
#     "Греет плов",
#     "Ищет, где бы отдохнуть на майские",
#     "Читает документацию, а сам не верит",
#     "Добавляет фичу, но с костылями",
#     "В Telegram, но делает вид, что занят",
#     "Ждёт дедлайн, чтобы начать работать",
#     "Объясняет заказчику, почему баг — это фича",
#     "Думает, как назвать переменную"
# ]

# async def handle_volodya(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     reply = random.choice(REPLIES)
#     await update.message.reply_text(reply)
#     log_event("PHRASE", f"/v — {reply}")
