from telebot import types
from texts import MESSAGES, BUTTONS
from utils import get_random_chibi, generate_chibi_stats, calculate_collection_rarity
from datetime import datetime, timedelta
import random

class DailyHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def claim_daily_chibi(self, chat_id, user_id):
        user = self.db.get_user(user_id)
        
        if not user:
            self.bot.send_message(chat_id, "❌ Пользователь не найден")
            return
        
        last_claim = user.get('chibi_last_claim')
        if last_claim:
            now = datetime.utcnow()
            if (now - last_claim).total_seconds() < 4 * 3600 + 45 * 60:
                time_left = 4 * 3600 + 45 * 60 - (now - last_claim).total_seconds()
                minutes = int(time_left) // 60
                seconds = int(time_left) % 60
                time_str = f"{minutes}ч {seconds}м"
                
                message = MESSAGES['chibi_cooldown'].format(time_left=time_str)
                self.bot.send_message(chat_id, message, parse_mode='Markdown')
                return
        
        selected_collections = user.get('selected_collections', ['star_wars'])
        
        rarity_type = calculate_collection_rarity()
        chibi_name, chibi_path = get_random_chibi(rarity_type)
        
        if not chibi_name:
            self.bot.send_message(chat_id, "🌀 *Чибики сейчас отдыхают!* Загляни позже")
            return
        
        chibi_data = {
            'name': chibi_name,
            'rarity': rarity_type,
            'obtained_at': datetime.utcnow(),
            **generate_chibi_stats()
        }
        
        self.db.add_chibi(user_id, chibi_data)
        self.db.update_user(user_id, {'chibi_last_claim': datetime.utcnow()})
        
        user = self.db.get_user(user_id)
        chibi_count = len([c for c in user.get('chibis', []) if c['name'] == chibi_name])
        
        rarity_emoji = {
            'common': '🔷',
            'secret': '🔶',
            'prize': '♦️'
        }.get(rarity_type, '🔷')
        
        rarity_text = {
            'common': 'Common',
            'secret': 'Secret',
            'prize': 'Prize'
        }.get(rarity_type, 'Unknown')
        
        caption = MESSAGES['daily_chibi'].format(
            chibi_name=chibi_name,
            emoji=rarity_emoji,
            rarity=rarity_text,
            count=chibi_count
        )
        
        try:
            self.bot.send_photo(chat_id, open(chibi_path, 'rb'), caption=caption, parse_mode='Markdown')
        except:
            self.bot.send_message(chat_id, caption, parse_mode='Markdown')
    
    def claim_daily_bonus(self, chat_id, user_id):
        user = self.db.get_user(user_id)
        
        if not user:
            return
        
        last_bonus = user.get('bonus_last_claim')
        if last_bonus:
            now = datetime.utcnow()
            if (now - last_bonus).total_seconds() < 24 * 3600:
                time_left = 24 * 3600 - (now - last_bonus).total_seconds()
                hours = int(time_left) // 3600
                minutes = (int(time_left) % 3600) // 60
                time_str = f"{hours}ч {minutes}м"
                
                message = f"🔒 Бонус будет доступен через {time_str}"
                self.bot.send_message(chat_id, message, parse_mode='Markdown')
                return
        
        bonus_amount = random.randint(50, 150)
        self.db.add_coins(user_id, bonus_amount)
        self.db.update_user(user_id, {'bonus_last_claim': datetime.utcnow()})
        
        user = self.db.get_user(user_id)
        message = f"🎁 *Эй, {user['first_name']}!*\nТы только что получил ежедневный бонус!\n\n+ 💰*{bonus_amount}* коинов"
        
        self.bot.send_message(chat_id, message, parse_mode='Markdown')
