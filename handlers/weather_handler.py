import os
import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from utils.logger import log_event
import pytz

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

TIMEZONE = "Asia/Almaty"

async def handle_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Если пользователь не указал город — по умолчанию Астана
    if not context.args:
        city = "Астана"
    else:
        city = " ".join(context.args)

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    await update.message.reply_text("❌ Не удалось получить погоду. Проверьте название города.")
                    log_event("WEATHER_ERROR", f"{city} — HTTP {resp.status}")
                    return

                data = await resp.json()

                name = data["name"]
                if name == "Нур-Султан":
                    name = "Астана"
                weather_desc = data["weather"][0]["description"].capitalize()
                temp = round(data["main"]["temp"], 1)
                feels_like = round(data["main"]["feels_like"], 1)
                wind = round(data["wind"]["speed"])
                humidity = data["main"]["humidity"]

                # Время и восход/закат
                tz = pytz.timezone(TIMEZONE)
                now = datetime.now(tz)
                time_str = now.strftime("%H:%M (%d.%m.%Y)")

                sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz).strftime("%H:%M")
                sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz).strftime("%H:%M")

                msg = (
                    f"🏙 Погода в городе {name}:\n"
                    f"🌡 Сейчас: {temp}°C ({weather_desc})\n"
                    f"🫂 Ощущается как: {feels_like}°C\n"
                    f"🌬 Ветер: {wind} м/с\n"
                    f"💦 Влажность: {humidity}%\n"
                    f"⏰ Время: {time_str}\n"
                    f"🌅 Восход: {sunrise} | 🌇 Закат: {sunset}"
                )

                await update.message.reply_text(msg)
                log_event("WEATHER", f"{name}: {temp}°C, {weather_desc}")

    except Exception as e:
        await update.message.reply_text("⚠️ Произошла ошибка при получении погоды.")
        log_event("WEATHER_ERROR", f"{city} — {str(e)}")
