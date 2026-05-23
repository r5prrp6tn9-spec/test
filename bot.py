import telebot
from telebot import types
import os
import logging
from datetime import datetime, timedelta

from database import Database
from texts import MESSAGES, BUTTONS, LOCATIONS, STICKERS
from collections_handler import CollectionsHandler
from raids import RaidsHandler
from crafting import CraftingHandler
from warehouse import WarehouseHandler
from admin import AdminHandler
from daily import DailyHandler
from utils import format_time_remaining

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChibiBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.db = Database()
        
        self.collections_handler = CollectionsHandler(self.bot, self.db)
        self.raids_handler = RaidsHandler(self.bot, self.db)
        self.crafting_handler = CraftingHandler(self.bot, self.db)
        self.warehouse_handler = WarehouseHandler(self.bot, self.db)
        self.admin_handler = AdminHandler(self.bot, self.db)
        self.daily_handler = DailyHandler(self.bot, self.db)
        
        self._register_handlers()
        logger.info("ChibiBot initialized successfully")
    
    def _register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.start_command(message)
        
        @self.bot.message_handler(commands=['collections'])
        def handle_collections(message):
            self.collections_handler.show_collections_menu(message.from_user.id, message.chat.id)
        
        @self.bot.message_handler(commands=['cantina'])
        def handle_cantina(message):
            if message.from_user.id not in [6967960142]:
                self.bot.send_message(message.chat.id, "❌ Команда доступна с 5 уровня!")
                return
            self.raids_handler.show_cantina_menu(message.chat.id)
        
        @self.bot.message_handler(commands=['chibi'])
        def handle_daily_chibi(message):
            self.daily_handler.claim_daily_chibi(message.chat.id, message.from_user.id)
        
        @self.bot.message_handler(commands=['craft'])
        def handle_craft(message):
            self.crafting_handler.show_craft_menu(message.chat.id)
        
        @self.bot.message_handler(commands=['warehouse'])
        def handle_warehouse(message):
            self.warehouse_handler.show_warehouse(message.chat.id, message.from_user.id)
        
        @self.bot.message_handler(commands=['wipe'])
        def handle_wipe(message):
            self.admin_handler.show_wipe_menu(message.chat.id, message.from_user.id)
        
        @self.bot.message_handler(commands=['bonus'])
        def handle_bonus(message):
            self.daily_handler.claim_daily_bonus(message.chat.id, message.from_user.id)
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            self.process_callback(call)
    
    def start_command(self, message):
        user_id = message.from_user.id
        user = self.db.get_user(user_id)
        
        if user:
            self.bot.send_message(
                message.chat.id,
                "ℹ️ Ты уже запустил бота. Кстати за багоюз у нас дают бан",
                parse_mode='Markdown'
            )
            return
        
        self.db.create_user(user_id, message.from_user.first_name, message.from_user.username)
        
        welcome_msg = MESSAGES['welcome'].format(first_name=message.from_user.first_name)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTONS['our_channel'], url="https://t.me/chibeki_official"))
        markup.add(types.InlineKeyboardButton(BUTTONS['preferences'], callback_data="show_preferences"))
        
        self.bot.send_message(
            message.chat.id,
            welcome_msg,
            parse_mode='Markdown',
            reply_markup=markup
        )
        
        self.daily_handler.claim_daily_chibi(message.chat.id, user_id)
    
    def process_callback(self, call):
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        data = call.data
        
        try:
            if data == "show_preferences":
                self.collections_handler.show_collections_menu(user_id, chat_id)
            
            elif data.startswith("toggle_collection_"):
                self.collections_handler.handle_collection_query(call, user_id, chat_id)
            
            elif data == "cantina_raids":
                self.raids_handler.show_raids_menu(chat_id, user_id)
            
            elif data.startswith("select_location_"):
                loc_idx = int(data.split('_')[2])
                locations = [LOCATIONS['easy'], LOCATIONS['medium'], LOCATIONS['hard']]
                if loc_idx < 3:
                    location = locations[loc_idx][0]
                    self.raids_handler.show_location_info(chat_id, location)
            
            elif data.startswith("raid_select_chibi_"):
                location_name = data.replace("raid_select_chibi_", "")
                self.raids_handler.show_chibi_selection(chat_id, user_id, location_name)
            
            elif data.startswith("raid_start_"):
                parts = data.split('_')
                chibi_idx = int(parts[2])
                location_name = parts[3] if len(parts) > 3 else ""
                self.raids_handler.start_raid(chat_id, user_id, chibi_idx, location_name)
            
            elif data.startswith("raid_wait_"):
                raid_id = data.replace("raid_wait_", "")
                raid = self.db.get_raid(raid_id)
                if raid and raid['return_at'] <= datetime.utcnow():
                    self.raids_handler.complete_raid(chat_id, user_id, raid_id)
                else:
                    self.bot.answer_callback_query(call.id, "⏳ Рейд еще в процессе...", show_alert=False)
            
            elif data == "craft_create":
                self.crafting_handler.show_craft_items(chat_id)
            
            elif data.startswith("craft_item_"):
                item_idx = int(data.split('_')[2])
                self.crafting_handler.show_craft_item_detail(chat_id, item_idx)
            
            elif data.startswith("craft_do_"):
                item_idx = int(data.split('_')[2])
                success, error = self.crafting_handler.craft_item(chat_id, user_id, item_idx)
                if not success:
                    self.bot.answer_callback_query(call.id, error, show_alert=True)
            
            elif data == "warehouse_chibis":
                self.warehouse_handler.show_chibis(chat_id, user_id)
            
            elif data == "warehouse_items":
                self.warehouse_handler.show_items(chat_id, user_id)
            
            elif data == "warehouse_resources":
                self.warehouse_handler.show_resources(chat_id, user_id)
            
            elif data.startswith("equip_item_"):
                item_name = data.replace("equip_item_", "")
                self.warehouse_handler.show_equip_chibi_selection(chat_id, user_id, item_name)
            
            elif data.startswith("equip_do_"):
                parts = data.split('_')
                chibi_idx = int(parts[2])
                item_name = parts[3] if len(parts) > 3 else ""
                self.warehouse_handler.equip_item(chat_id, user_id, chibi_idx, item_name)
            
            elif data == "wipe_confirm":
                self.admin_handler.request_wipe_password(chat_id, user_id)
            
            elif data == "wipe_execute":
                self.admin_handler.execute_wipe()
                self.bot.send_message(chat_id, MESSAGES['wipe_success'], parse_mode='Markdown')
            
            elif data in ["preferences_back", "cantina_back", "cantina_raids_back", "craft_back", "craft_items_back", "warehouse_back"]:
                self.bot.delete_message(chat_id, call.message.message_id)
            
            self.bot.answer_callback_query(call.id)
        
        except Exception as e:
            logger.error(f"Callback error: {e}")
            self.bot.answer_callback_query(call.id, "❌ Ошибка!", show_alert=True)
    
    def start(self):
        logger.info("Starting bot polling...")
        self.bot.infinity_polling()

def main():
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError("BOT_TOKEN not found in environment variables")
    
    bot = ChibiBot(token)
    bot.start()

if __name__ == "__main__":
    main()
