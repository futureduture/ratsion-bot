import json
from datetime import datetime, timedelta, date

_menu_cache = None
MENU_OFFSET = None

def clear_menu_cache():
    global _menu_cache
    _menu_cache = None

def get_menu_data():
    global _menu_cache
    if _menu_cache is None:
        with open("menu_data.json", "r", encoding="utf-8") as f:
            _menu_cache = json.load(f)
    return _menu_cache

def detect_menu_offset():
    """Визначає зсув, щоб день тижня відповідав першому дню в menu_data"""
    today_weekday = datetime.today().weekday()  # 0 — понеділок
    menu = get_menu_data()
    today_date = date.today()
    first_menu_date = today_date - timedelta(days=today_weekday)
    return (today_date - first_menu_date).days % len(menu)

MENU_OFFSET = detect_menu_offset()

def get_today_index():
    return (datetime.today().weekday() - MENU_OFFSET) % len(get_menu_data())

def get_tomorrow_index():
    return (get_today_index() + 1) % len(get_menu_data())

def format_meal(meal, number):
    return f"{number}. {meal['name']}\nІнгредієнти: {', '.join(meal['ingredients'])}\nРецепт: {meal['recipe']}"

def get_today_menu_text():
    index = get_today_index()
    data = get_menu_data()[index]
    today_str = (date.today()).strftime("📅 %A, %d.%m.%Y")
    return "\n\n".join([
        today_str,
        "🥣 Сніданок:\n" + format_meal(data['breakfast'], "1"),
        "🍛 Обід:\n" + format_meal(data['lunch'], "2"),
        "🍽 Вечеря:\n" + format_meal(data['dinner'], "3")
    ])

def get_tomorrow_menu_text():
    index = get_tomorrow_index()
    data = get_menu_data()[index]
    tomorrow_str = (date.today() + timedelta(days=1)).strftime("📅 %A, %d.%m.%Y")
    return "\n\n".join([
        tomorrow_str,
        "🥣 Сніданок:\n" + format_meal(data['breakfast'], "1"),
        "🍛 Обід:\n" + format_meal(data['lunch'], "2"),
        "🍽 Вечеря:\n" + format_meal(data['dinner'], "3")
    ])

def get_week_menu_text():
    data = get_menu_data()
    result = []
    today = date.today()
    for i, day in enumerate(data):
        day_date = today + timedelta(days=i - get_today_index())
        result.append(f"📅 {day_date.strftime('%A, %d.%m.%Y')}")
        result.append("🥣 Сніданок:\n" + format_meal(day['breakfast'], "1"))
        result.append("")
        result.append("🍛 Обід:\n" + format_meal(day['lunch'], "2"))
        result.append("")
        result.append("🍽 Вечеря:\n" + format_meal(day['dinner'], "3"))
        result.append("-" * 30)
    return "\n".join(result)

def get_day_menu_text(day):
    data = get_menu_data()[day]
    return "\n\n".join([
        "🥣 Сніданок:\n" + format_meal(data['breakfast'], "1"),
        "🍛 Обід:\n" + format_meal(data['lunch'], "2"),
        "🍽 Вечеря:\n" + format_meal(data['dinner'], "3")
    ])

def get_week_grocery_list():
    data = get_menu_data()
    items = set()
    for day in data:
        for meal in day.values():
            items.update(meal['ingredients'])
    return "🛒 Продукти на тиждень:\n" + "\n".join(f"• {item}" for item in sorted(items))

def get_day_grocery_list():
    data = get_menu_data()[get_today_index()]
    items = set()
    for meal in data.values():
        items.update(meal['ingredients'])
    return "🛒 Продукти на сьогодні:\n" + "\n".join(f"• {item}" for item in sorted(items))

def get_tomorrow_grocery_list():
    data = get_menu_data()[get_tomorrow_index()]
    items = set()
    for meal in data.values():
        items.update(meal['ingredients'])
    return "🛒 Продукти на завтра:\n" + "\n".join(f"• {item}" for item in sorted(items))
