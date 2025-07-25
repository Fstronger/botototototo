import json
import os
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

AFFIRMATIONS = [
    "💻 Я справляюсь с любыми техническими задачами — шаг за шагом, строка за строкой.",
    "⚙️ Мой код становится лучше с каждым днём.",
    "🌐 Я создаю продукты, которые упрощают жизнь людям.",
    "🧠 Моя логика и мышление — мой сильнейший инструмент.",
    "☕ Даже сложные баги — лишь временные задачи на моём пути.",
    "🚀 Я расту как разработчик с каждым новым проектом.",
    "⏱️ Я умею грамотно распределять время и ресурсы.",
    "🧩 Я нахожу нестандартные решения для нестандартных задач.",
    "🔐 Я создаю безопасный, надёжный и эффективный код.",
    "🖥️ Я ценен(ценна) как специалист, и мои знания востребованы.",
    "📈 Каждый день я становлюсь лучше в своём деле.",
    "🌿 Я сохраняю баланс между работой и отдыхом.",
    "📚 Я легко учусь новому и адаптируюсь к переменам.",
    "🧘 Я спокоен(спокойна) даже в условиях дедлайнов.",
    "💬 Мои идеи важны — я не боюсь ими делиться.",
    "🤝 Я умею работать в команде и ценю вклад других.",
    "🔍 Я замечаю детали, которые другие упускают.",
    "🌟 Моя работа имеет значение.",
    "🔧 Я не боюсь ошибок — я извлекаю из них опыт.",
    "🧭 Я иду по своему пути развития уверенно и с удовольствием."
]

DATA_FILE = "affirmation_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def handle_affirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    now = datetime.utcnow()

    user_entry = data.get(user_id)

    if user_entry:
        last_time = datetime.fromisoformat(user_entry["timestamp"])
        if now - last_time < timedelta(hours=24):
            affirmation = user_entry["text"]
        else:
            affirmation = random.choice(AFFIRMATIONS)
            data[user_id] = {"timestamp": now.isoformat(), "text": affirmation}
            save_data(data)
    else:
        affirmation = random.choice(AFFIRMATIONS)
        data[user_id] = {"timestamp": now.isoformat(), "text": affirmation}
        save_data(data)

    message = (
        "*Твоя аффирмация дня:*\n\n"
        f"_{affirmation}_\n\n"
        "Повторяй её в течение дня. Может, поможет 🙂 А может — нет. Но ты попробуй."
    )

    await update.message.reply_text(message, parse_mode="Markdown")
