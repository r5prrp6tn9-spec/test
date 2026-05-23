from telebot import types
from texts import MESSAGES, BUTTONS, LOCATIONS, STICKERS
from utils import format_time_remaining, calculate_raid_time, get_random_location, generate_raid_loot, check_injury_chance, format_loot_string, get_injury_message, get_success_message, format_location_difficulty
from datetime import datetime, timedelta
import random

class RaidsHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.current_locations = {}
        self.active_raids = {}
    
    def show_cantina_menu(self, chat_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTONS['cantina_raids'], callback_data="cantina_raids"))
        markup.add(types.InlineKeyboardButton(BUTTONS['cantina_info'], callback_data="cantina_info"))
        
        self.bot.send_message(
            chat_id,
            MESSAGES['cantina_menu'],
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def show_raids_menu(self, chat_id, user_id):
        time_left = format_time_remaining(random.randint(0, 5400))
        
        markup = types.InlineKeyboardMarkup()
        locations = get_random_location()
        
        for i, location in enumerate(locations):
            active_count = random.randint(1, 15)
            button_text = f"{location['emoji']} {location['name']} ({active_count})"
            callback_data = f"select_location_{i}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="cantina_back"))
        
        message_text = MESSAGES['cantina_raids'].format(time_left=time_left)
        self.bot.send_message(
            chat_id,
            message_text,
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def show_location_info(self, chat_id, location_data):
        difficulty_emoji = format_location_difficulty(location_data['difficulty'])
        difficulty_text = f"{difficulty_emoji} " + ('Легко' if location_data['difficulty'] == 'easy' else 'Средне' if location_data['difficulty'] == 'medium' else 'Трудно')
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTONS['raid_button'], callback_data=f"raid_select_chibi_{location_data['name']}"))
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="cantina_raids_back"))
        
        message_text = MESSAGES['cantina_location_info'].format(
            emoji=location_data['emoji'],
            location=location_data['name'],
            stamina=location_data['stamina'],
            difficulty=difficulty_text,
            loot_type=location_data['loot_type']
        )
        
        self.bot.send_message(
            chat_id,
            message_text,
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def show_chibi_selection(self, chat_id, user_id, location_name):
        user = self.db.get_user(user_id)
        chibis = user.get('chibis', [])
        
        if not chibis:
            self.bot.send_message(chat_id, "❌ У тебя нет чибиков!")
            return
        
        markup = types.InlineKeyboardMarkup()
        for i, chibi in enumerate(chibis[:8]):
            health = chibi.get('health', 100)
            stamina = chibi.get('stamina', 100)
            damage = chibi.get('damage', 20)
            stats_text = f"({health}❤️ {stamina}⚡️ {damage}🗡️)"
            button_text = f"{chibi.get('name', 'Чибик')} {stats_text}"
            callback_data = f"raid_start_{i}_{location_name}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="cantina_raids_back"))
        
        message_text = MESSAGES['cantina_select_chibi'].format(
            emoji='🪎',
            location=location_name
        )
        
        self.bot.send_message(
            chat_id,
            message_text,
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def start_raid(self, chat_id, user_id, chibi_idx, location_name):
        user = self.db.get_user(user_id)
        chibis = user.get('chibis', [])
        
        if chibi_idx >= len(chibis):
            return
        
        chibi = chibis[chibi_idx]
        location_data = None
        
        for diff in ['easy', 'medium', 'hard']:
            for loc in LOCATIONS[diff]:
                if loc['name'] == location_name:
                    location_data = loc
                    break
        
        if not location_data:
            return
        
        raid_time = calculate_raid_time(location_data['difficulty'])
        return_at = datetime.utcnow() + timedelta(seconds=raid_time)
        
        raid = self.db.create_raid(
            user_id,
            chibi_idx,
            location_name,
            location_data['difficulty'],
            return_at
        )
        
        try:
            self.bot.delete_message(chat_id, chat_id)
        except:
            pass
        
        self.bot.send_sticker(chat_id, STICKERS['raid_start'])
        
        timer_text = f"{raid_time // 60}м {raid_time % 60}с"
        message = MESSAGES['cantina_raid_started'].format(
            chibi_name=chibi.get('name', 'Чибик'),
            emoji=location_data['emoji'],
            location=location_data['name'],
            timer=timer_text
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"🔒 {timer_text}", callback_data=f"raid_wait_{raid['_id']}"))
        
        self.bot.send_message(chat_id, message, parse_mode='Markdown', reply_markup=markup)
    
    def complete_raid(self, chat_id, user_id, raid_id):
        raid = self.db.get_raid(raid_id)
        if not raid:
            return
        
        user = self.db.get_user(user_id)
        chibis = user.get('chibis', [])
        chibi = chibis[raid['chibi_id']] if raid['chibi_id'] < len(chibis) else None
        
        if not chibi:
            return
        
        loot = generate_raid_loot(raid['location'], raid['difficulty'])
        is_injured = check_injury_chance(chibi.get('health', 80), chibi.get('damage', 20))
        
        self.db.complete_raid(raid_id, loot, is_injured)
        
        try:
            self.bot.delete_message(chat_id, chat_id)
        except:
            pass
        
        if is_injured:
            self.bot.send_sticker(chat_id, STICKERS['raid_injured'])
            event = get_injury_message()
            chibi['health'] = random.randint(5, 15)
        else:
            self.bot.send_sticker(chat_id, STICKERS['raid_success'])
            event = get_success_message()
        
        loot_str = format_loot_string(loot)
        message = MESSAGES['cantina_raid_ready'].format(
            chibi_name=chibi.get('name', 'Чибик'),
            event=event,
            loot=loot_str
        )
        
        self.bot.send_message(chat_id, message, parse_mode='Markdown')
