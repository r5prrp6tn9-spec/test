from telebot import types
from texts import MESSAGES, BUTTONS, CRAFTING_ITEMS

class WarehouseHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def show_warehouse(self, chat_id, user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⚡️ Чибики", callback_data="warehouse_chibis"))
        markup.add(types.InlineKeyboardButton("🧧 Предметы", callback_data="warehouse_items"))
        markup.add(types.InlineKeyboardButton("📦 Ресурсы", callback_data="warehouse_resources"))
        
        self.bot.send_message(
            chat_id,
            MESSAGES['warehouse'],
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def show_resources(self, chat_id, user_id):
        resources = self.db.get_resources(user_id)
        
        resource_text = ""
        if resources:
            res_dict = resources.get('resources', {})
            for emoji in ['🔩', '🗜️', '🎚️', '⚙️', '⛓️', '🪵', '📯', '🍸', '🪈']:
                qty = res_dict.get(emoji, 0)
                resource_text += f"{emoji} ×{qty}\n"
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="warehouse_back"))
        
        message = MESSAGES['warehouse_resources'].format(resources=resource_text or "Пусто")
        self.bot.send_message(chat_id, message, parse_mode='Markdown', reply_markup=markup)
    
    def show_chibis(self, chat_id, user_id, page=1):
        user = self.db.get_user(user_id)
        chibis = user.get('chibis', [])
        
        per_page = 8
        total_pages = (len(chibis) + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        
        markup = types.InlineKeyboardMarkup()
        for i, chibi in enumerate(chibis[start:end]):
            health = chibi.get('health', 100)
            stamina = chibi.get('stamina', 100)
            damage = chibi.get('damage', 20)
            status = "🩹" if health == 0 else "✅"
            button_text = f"{status} {chibi.get('name', 'Чибик')} ({health}❤️ {stamina}⚡️ {damage}🗡️)"
            callback_data = f"chibi_detail_{start + i}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        if total_pages > 1:
            nav_buttons = []
            if page > 1:
                nav_buttons.append(types.InlineKeyboardButton("◀", callback_data=f"warehouse_chibis_page_{page-1}"))
            nav_buttons.append(types.InlineKeyboardButton(f"{page}/{total_pages}", callback_data="noop"))
            if page < total_pages:
                nav_buttons.append(types.InlineKeyboardButton("▶", callback_data=f"warehouse_chibis_page_{page+1}"))
            markup.add(*nav_buttons)
        
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="warehouse_back"))
        
        message = f"*📦 Твои чибики*\nСтраница {page}/{total_pages}"
        self.bot.send_message(chat_id, message, parse_mode='Markdown', reply_markup=markup)
    
    def show_items(self, chat_id, user_id):
        equipment = self.db.equipment.find({"user_id": user_id, "chibi_id": None})
        items = list(equipment)
        
        markup = types.InlineKeyboardMarkup()
        if items:
            for item in items:
                button_text = f"{item.get('item_name', 'Предмет')}"
                callback_data = f"equip_item_{item.get('item_name', 'unknown')}"
                markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        else:
            self.bot.send_message(chat_id, "❌ Предметов нет", reply_markup=markup)
            return
        
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="warehouse_back"))
        
        message = "*🧧 Твои предметы*\nВыбери предмет для экипировки"
        self.bot.send_message(chat_id, message, parse_mode='Markdown', reply_markup=markup)
    
    def show_equip_chibi_selection(self, chat_id, user_id, item_name):
        user = self.db.get_user(user_id)
        chibis = user.get('chibis', [])
        
        item_data = self._get_item_by_name(item_name)
        if not item_data:
            return
        
        markup = types.InlineKeyboardMarkup()
        for i, chibi in enumerate(chibis[:8]):
            health = chibi.get('health', 100)
            stamina = chibi.get('stamina', 100)
            damage = chibi.get('damage', 20)
            h_boost = item_data.get('health_boost', 0)
            s_boost = item_data.get('stamina_boost', 0)
            d_boost = item_data.get('damage_boost', 0)
            
            stats_text = f"({health}❤️[+{h_boost}] {stamina}⚡️[+{s_boost}] {damage}🗡️[+{d_boost}])"
            button_text = f"{chibi.get('name', 'Чибик')} {stats_text}"
            callback_data = f"equip_do_{i}_{item_name}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="warehouse_items"))
        
        message = MESSAGES['equip_item'].format(
            emoji=item_data.get('emoji', ''),
            item_name=item_name
        )
        
        self.bot.send_message(chat_id, message, parse_mode='Markdown', reply_markup=markup)
    
    def equip_item(self, chat_id, user_id, chibi_idx, item_name):
        item_data = self._get_item_by_name(item_name)
        if not item_data:
            return False
        
        self.db.add_equipment(user_id, chibi_idx, {
            'name': item_name,
            'health_boost': item_data.get('health_boost', 0),
            'stamina_boost': item_data.get('stamina_boost', 0),
            'damage_boost': item_data.get('damage_boost', 0),
        })
        
        user = self.db.get_user(user_id)
        chibi = user['chibis'][chibi_idx]
        
        message = MESSAGES['equip_success'].format(chibi_name=chibi.get('name', 'Чибик'))
        self.bot.send_message(chat_id, message, parse_mode='Markdown')
        return True
    
    def _get_item_by_name(self, item_name):
        for item in CRAFTING_ITEMS.values():
            if item['name'] == item_name:
                return item
        return None
