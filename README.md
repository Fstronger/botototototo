# Totobot — Telegram bot для цитат с размытой аватаркой

## Что делает
- При ответе на сообщение бот генерирует картинку: фон — размытка аватарки автора, текст — его сообщение.

## Запуск локально
1. Склонируй репо.
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Установи токен: `export BOT_TOKEN=...`
5. `python bot.py`

## Деплой на Render.com
- Подключи репо, установи среду `Python 3`, команду запуска `python bot.py`, переменную `BOT_TOKEN`.
