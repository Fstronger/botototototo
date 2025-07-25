import re
import random
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import log_event

RESPONSES = [
    "Пилит фичу за 500 тг",
    "На созвоне с клиентом",
    "Греет плов",
    "Читает документацию, а сам не верит",
    "Добавляет фичу, но с костылями",
    "Ждёт дедлайн, чтобы начать работать",
    "Объясняет заказчику, почему баг — это фича",
    "Смотрит туториалы и страдает",
    "Сидит тихо — значит делает вид, что работает",
    "Пилит фичу за 500 тг",
    "На созвоне с клиентом",
    "Греет плов",
    "Ищет, где бы отдохнуть на майские",
    "Читает документацию, а сам не верит",
    "Добавляет фичу, но с костылями",
    "В Telegram, но делает вид, что занят",
    "Ждёт дедлайн, чтобы начать работать",
    "Объясняет заказчику, почему баг — это фича",
    "Думает, как назвать переменную",
    "Садится на бутылку. А чего добился ты?"
]

TRIGGER_RESPONSES = {
    "котя котя": "Ися Ися",
    "котя, котя": "Ися, Ися",
    "алишка": "в красных штанишках",
    "антон": "эрондондон",
    "ибрагим": "хорошее имя",
    "гаф гаф": "может еще хрюкнешь?",
    "тетя гуля": "не тетягулькайте мне тут"
}

QUESTION_KEYWORDS = ["где", "что делает", "занят", "чем", "спит", "куда"]

async def handle_phrases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()

    # ✅ Триггер: имя + вопрос
    lowered = user_text.lower()
    if any(keyword in lowered for keyword in QUESTION_KEYWORDS):
        capitalized_words = re.findall(r'\b[А-ЯA-Z][а-яa-z]+\b', user_text)
        if capitalized_words:
            reply = random.choice(RESPONSES)
            await update.message.reply_text(reply)
            log_event("PHRASE", f"Вопрос про имя «{capitalized_words[0]}»: {reply}")
            return

    # ✅ Триггер: слово заканчивается на "тошка"
    if any(word.endswith("тошка") for word in lowered.split()):
        await update.message.reply_text("картошка")
        log_event("PHRASE", f"Ответ 'картошка' на слово с окончанием 'тошка': {lowered}")
        return

    # ✅ Точные фразы
    for trigger, response in TRIGGER_RESPONSES.items():
        if trigger in lowered:
            await update.message.reply_text(response)
            log_event("PHRASE", f"Триггер «{trigger}» сработал на сообщение: {lowered}")
            break



    # Отдельно проверка по ключевым словам
    # for word in KEYWORDS:
    #     if word in user_text:
    #         await update.message.reply_text("тағы не істейн?")
    #         log_event("PHRASE", f"Фраза с ключевым словом «{word}»: {user_text}")
    #         return