from telebot import types
from texts import MESSAGES, BUTTONS, CRAFTING_ITEMS
import math

class CraftingHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def show_craft_menu(self, chat_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTONS['craft_create'], callback_data="craft_create"))
        markup.add(types.InlineKeyboardButton(BUTTONS['craft_info'], callback_data="craft_info"))
        
        self.bot.send_message(
            chat_id,
            MESSAGES['craft_menu'],
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def show_craft_items(self, chat_id):
        items = list(CRAFTING_ITEMS.values())
        markup = types.InlineKeyboardMarkup()
        
        for i, item in enumerate(items):
            button_text = f"{item['emoji']} {item['name']}"
            callback_data = f"craft_item_{i}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="craft_back"))
        
        self.bot.send_message(
            chat_id,
            MESSAGES['craft_select'],
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def show_craft_item_detail(self, chat_id, item_idx):
        items = list(CRAFTING_ITEMS.values())
        if item_idx >= len(items):
            return
        
        item = items[item_idx]
        boost_stats = []
        if item['health_boost'] > 0:
            boost_stats.append(f"❤️ +{item['health_boost']}")
        if item['stamina_boost'] > 0:
            boost_stats.append(f"⚡️ +{item['stamina_boost']}")
        if item['damage_boost'] > 0:
            boost_stats.append(f"🗡️ +{item['damage_boost']}")
        
        boost_text = ", ".join(boost_stats) if boost_stats else "Нет улучшений"
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTONS['craft_create'], callback_data=f"craft_do_{item_idx}"))
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="craft_items_back"))
        
        message = MESSAGES['craft_item_detail'].format(
            emoji=item['emoji'],
            item_name=item['name'],
            description=item['description'],
            boost_stats=boost_text
        )
        
        self.bot.send_message(
            chat_id,
            message,
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def craft_item(self, chat_id, user_id, item_idx):
        items = list(CRAFTING_ITEMS.values())
        if item_idx >= len(items):
            return False, "❌ Предмет не найден"
        
        item = items[item_idx]
        user = self.db.get_user(user_id)
        
        if user['coins'] < item['cost']:
            return False, f"❌ Недостаточно коинов! Нужно {item['cost']}, а у тебя {user['coins']}"
        
        self.db.add_coins(user_id, -item['cost'])
        self.db.add_equipment(user_id, None, item)
        
        message = MESSAGES['craft_success'].format(
            name=user['first_name'],
            item_name=item['name'],
            emoji=item['emoji']
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTONS['warehouse_check'], callback_data="warehouse_items"))
        
        self.bot.send_message(chat_id, message, parse_mode='Markdown', reply_markup=markup)
        return True, None
    
    def check_recipe_ingredients(self, user_id, item_idx):
        items = list(CRAFTING_ITEMS.values())
        if item_idx >= len(items):
            return False, []
        
        item = items[item_idx]
        resources = self.db.get_resources(user_id)
        
        missing = []
        if resources:
            for ingredient, needed_qty in item['recipe'].items():
                current_qty = resources.get('resources', {}).get(ingredient, 0)
                if current_qty < needed_qty:
                    missing.append((ingredient, needed_qty - current_qty))
        else:
            missing = list(item['recipe'].items())
        
        return len(missing) == 0, missing
