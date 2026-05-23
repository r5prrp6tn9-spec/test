import random
import os
from datetime import datetime, timedelta
from texts import LOCATIONS

def scan_chibis(collection_path):
    chibis = {}
    if os.path.exists(collection_path):
        for file in os.listdir(collection_path):
            if file.endswith('.png'):
                name = file.replace('.png', '').replace('#U', '')
                chibis[name] = f"{collection_path}/{file}"
    return chibis

def get_random_chibi(rarity='common'):
    if rarity == 'common':
        path = 'chibis/common'
    elif rarity == 'secret':
        path = 'chibis/secret'
    else:
        path = 'chibis/prize'
    
    chibis = scan_chibis(path)
    if chibis:
        name = random.choice(list(chibis.keys()))
        return name, chibis[name]
    return None, None

def format_time_remaining(seconds):
    if seconds <= 0:
        return "0м"
    minutes = seconds // 60
    secs = seconds % 60
    if minutes == 0:
        return f"{secs}с"
    return f"{minutes}м {secs}с"

def generate_chibi_stats():
    health = random.randint(67, 100)
    stamina = random.randint(67, 100)
    damage = random.randint(13, 36)
    return {
        'health': health,
        'stamina': stamina,
        'damage': damage,
    }

def calculate_raid_time(difficulty):
    base_times = {'easy': 8 * 60, 'medium': 10 * 60, 'hard': 15 * 60}
    base = base_times.get(difficulty, 10 * 60)
    variance = random.choice([0, 15, 30, 45])
    additional = random.randint(0, 13) * 60
    return base + variance + additional

def get_random_location():
    easy = random.choice(LOCATIONS['easy'])
    medium = random.choice(LOCATIONS['medium'])
    hard = random.choice(LOCATIONS['hard'])
    return [easy, medium, hard]

def generate_raid_loot(location_name, difficulty):
    loot_templates = {
        'Таскенское поселение': [
            ('🔩', 2, 6, 0.67), ('🗜️', 1, 2, 0.13), ('🎚️', 1, 2, 0.47),
            ('⚙️', 3, 5, 0.52), ('⛓️', 1, 2, 0.15), ('🪵', 1, 4, 0.12),
            ('📯', 1, 1, 0.04),
        ],
        'Кантина Мос Эйсли': [
            ('🔩', 2, 3, 0.67), ('🗜️', 1, 2, 0.13), ('🎚️', 1, 2, 0.47),
            ('⚙️', 2, 5, 0.52), ('⛓️', 1, 3, 0.15), ('🍸', 1, 4, 0.12),
            ('🪈', 1, 1, 0.03),
        ],
    }
    
    if location_name not in loot_templates:
        return [('🔩', random.randint(2, 3), 0.5)]
    
    loot = []
    items = loot_templates[location_name]
    for _ in range(random.randint(1, 3)):
        item_info = random.choice(items)
        emoji, min_qty, max_qty, chance = item_info
        if random.random() < chance:
            qty = random.randint(min_qty, max_qty)
            loot.append((emoji, qty))
    
    return loot

def check_injury_chance(health, damage):
    injury_threshold = 70
    if health < injury_threshold:
        base_chance = (injury_threshold - health) / 100
        return random.random() < base_chance
    return random.random() < 0.15

def format_loot_string(loot):
    if not loot:
        return "Ничего"
    return ", ".join([f"{emoji} ×{qty}" for emoji, qty in loot])

def validate_password(password):
    from texts import ADMIN_PASSWORD
    return password == ADMIN_PASSWORD

def get_injury_message():
    messages = [
        "К сожалению, во время боя он пострадал и нуждается в помощи. Посмотри его состояние на складе",
        "Боец получил ранения, но морально готов вернуться снова!",
        "Он нуждается в медикаментах. Присмотри за ним внимательнее!",
    ]
    return random.choice(messages)

def get_success_message():
    messages = [
        "Рейд прошел успешно! Теперь ему понадобится долгий отдых",
        "Боец вернулся в отличной форме с богатой добычей!",
        "Невероятно удачный рейд! Твой чибик явно везун!",
    ]
    return random.choice(messages)

def create_pagination_buttons(items, page, per_page=8):
    total_pages = (len(items) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'page': page,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
    }

def get_chibi_status(health_current, health_max):
    if health_current == 0:
        return "🩹 Ранен"
    elif health_current < health_max * 0.3:
        return "⚠️ Критичное"
    elif health_current < health_max * 0.6:
        return "🟡 Поврежден"
    return "✅ Здоров"

def calculate_collection_rarity():
    rand = random.random()
    if rand < 0.7:
        return 'common'
    elif rand < 0.95:
        return 'secret'
    return 'prize'

def format_location_difficulty(difficulty):
    difficulty_map = {
        'easy': '🟢',
        'medium': '🟡',
        'hard': '🔴'
    }
    return difficulty_map.get(difficulty, '🟢')
