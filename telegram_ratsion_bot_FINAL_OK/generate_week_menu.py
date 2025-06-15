import json
import random
from datetime import datetime
from utils.menu_utils import clear_menu_cache

def load_meals_base():
    with open("meals_base.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_menu(menu):
    with open("menu_data.json", "w", encoding="utf-8") as f:
        json.dump(menu, f, indent=2, ensure_ascii=False)
    clear_menu_cache()

def load_current_menu():
    with open("menu_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_week_menu(replace_only_one=False):
    base = load_meals_base()
    if replace_only_one:
        index = datetime.today().weekday()
        new_day = {
            "breakfast": random.choice(base["breakfasts"]),
            "lunch": random.choice(base["lunches"]),
            "dinner": random.choice(base["dinners"]),
        }
        current_data = load_current_menu()
        current_data[index] = new_day
        save_menu(current_data)
    else:
        full_menu = []
        for _ in range(7):
            full_menu.append({
                "breakfast": random.choice(base["breakfasts"]),
                "lunch": random.choice(base["lunches"]),
                "dinner": random.choice(base["dinners"]),
            })
        save_menu(full_menu)
