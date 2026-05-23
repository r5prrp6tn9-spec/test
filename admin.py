from telebot import types
from texts import MESSAGES, BUTTONS, ADMIN_PASSWORD
from utils import validate_password

class AdminHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.wipe_attempts = {}
    
    def is_admin(self, user_id):
        user = self.db.get_user(user_id)
        return user and user.get('is_admin', False)
    
    def show_wipe_menu(self, chat_id, user_id):
        if not self.is_admin(user_id):
            self.bot.send_message(chat_id, "🙊 *Недостаточно прав!*", parse_mode='Markdown')
            return
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTONS['wipe_confirm'], callback_data="wipe_confirm"))
        
        self.bot.send_message(
            chat_id,
            MESSAGES['wipe_confirmation'],
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def request_wipe_password(self, chat_id, user_id):
        if not self.is_admin(user_id):
            return
        
        self.wipe_attempts[user_id] = True
        msg = self.bot.send_message(chat_id, "🔒 Введи пароль для подтверждения вайпа:")
        self.bot.register_next_step_handler(msg, self.process_wipe_password, chat_id, user_id)
    
    def process_wipe_password(self, message, chat_id, user_id):
        if not self.is_admin(user_id):
            return
        
        password = message.text.strip()
        
        if password == ADMIN_PASSWORD:
            self.execute_wipe()
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(BUTTONS['wipe_authorized'], callback_data="wipe_execute"))
            
            self.bot.send_message(
                chat_id,
                "✅ *Пароль верен!* Нажми кнопку для окончательного вайпа.",
                parse_mode='Markdown',
                reply_markup=markup
            )
        else:
            self.bot.send_message(chat_id, "❌ Неверный пароль! Попытка не засчитана.")
    
    def execute_wipe(self):
        self.db.users.update_many(
            {},
            {"$set": {
                "coins": 1000,
                "experience": 0,
                "level": 1,
                "chibis": [],
                "selected_collections": ["star_wars"],
                "chibi_last_claim": None,
            }}
        )
        
        self.db.raids.delete_many({})
        self.db.equipment.delete_many({})
        self.db.resources.delete_many({})
    
    def admin_get_infinite_resources(self, user_id):
        return {
            'coins': float('inf'),
            'chibis': float('inf'),
        }
    
    def ban_user(self, chat_id, user_id, target_username):
        if not self.is_admin(user_id):
            self.bot.send_message(chat_id, "🙊 *Недостаточно прав!*", parse_mode='Markdown')
            return
        
        from datetime import datetime, timedelta
        ban_until = datetime.utcnow() + timedelta(days=7)
        
        self.db.users.update_one(
            {"username": target_username},
            {"$set": {"is_banned": True, "ban_until": ban_until}}
        )
        
        self.bot.send_message(
            chat_id,
            f"✅ *{target_username} забанен на 7 дней!*",
            parse_mode='Markdown'
        )
    
    def unban_user(self, chat_id, user_id, target_username):
        if not self.is_admin(user_id):
            self.bot.send_message(chat_id, "🙊 *Недостаточно прав!*", parse_mode='Markdown')
            return
        
        self.db.users.update_one(
            {"username": target_username},
            {"$set": {"is_banned": False, "ban_until": None}}
        )
        
        self.bot.send_message(
            chat_id,
            f"✅ *{target_username} разбанен!*",
            parse_mode='Markdown'
        )
