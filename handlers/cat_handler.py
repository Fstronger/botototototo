import os
import json
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

CATS_FOLDER = "assets/cats"
DATA_FILE = "cat_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def handle_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    now = datetime.utcnow()

    user_entry = data.get(user_id)

    if user_entry:
        last_time = datetime.fromisoformat(user_entry["timestamp"])
        file_name = user_entry["file"]
        if now - last_time >= timedelta(hours=24):
            file_name = random.choice(os.listdir(CATS_FOLDER))
            data[user_id] = {"timestamp": now.isoformat(), "file": file_name}
            save_data(data)
    else:
        file_name = random.choice(os.listdir(CATS_FOLDER))
        data[user_id] = {"timestamp": now.isoformat(), "file": file_name}
        save_data(data)

    file_path = os.path.join(CATS_FOLDER, file_name)
    with open(file_path, "rb") as cat:
        await update.message.reply_photo(cat, caption="**Твой котик дня**", parse_mode="Markdown")
