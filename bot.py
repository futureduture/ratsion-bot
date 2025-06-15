import logging
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from utils.menu_utils import (
    get_today_menu_text, get_week_menu_text, get_day_menu_text,
    get_week_grocery_list, get_day_grocery_list,
    get_tomorrow_menu_text, get_tomorrow_grocery_list
)
from generate_week_menu import generate_week_menu

import os
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_FILE, "w") as f:
            json.dump(users, f)

reply_keyboard = [
    ["📅 Меню на тиждень", "🍽 Сьогоднішній раціон"],
    ["🔁 Перегенерувати меню", "🔂 Перегенерувати день"],
    ["🛒 Продукти на тиждень", "📆 Продукти на день"],
    ["📅 Раціон на завтра", "🛒 Продукти на завтра"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_chat.id)
    await update.message.reply_text("Привіт! Я бот раціону 🥗", reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📅 Меню на тиждень":
        await update.message.reply_text(get_week_menu_text())
    elif text == "🍽 Сьогоднішній раціон":
        await update.message.reply_text(get_today_menu_text())
    elif text == "🔁 Перегенерувати меню":
        generate_week_menu()
        await update.message.reply_text("Меню на тиждень оновлено ✅\n\n" + get_week_menu_text())
    elif text == "🔂 Перегенерувати день":
        generate_week_menu(replace_only_one=True)
        await update.message.reply_text("Сьогоднішній день оновлено ✅\n\n" + get_today_menu_text())
    elif text == "🛒 Продукти на тиждень":
        await update.message.reply_text(get_week_grocery_list())
    elif text == "📆 Продукти на день":
        await update.message.reply_text(get_day_grocery_list())
    elif text == "📅 Раціон на завтра":
        await update.message.reply_text(get_tomorrow_menu_text())
    elif text == "🛒 Продукти на завтра":
        await update.message.reply_text(get_tomorrow_grocery_list())
    else:
        await update.message.reply_text("Не зрозумів команду 🧐")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
