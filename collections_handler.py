from telebot import types
from texts import MESSAGES, BUTTONS, LOCATIONS
import os

class CollectionsHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def get_available_collections(self):
        collections = []
        chibis_path = 'chibis'
        if os.path.exists(chibis_path):
            for folder in os.listdir(chibis_path):
                if os.path.isdir(os.path.join(chibis_path, folder)):
                    collections.append({
                        'id': folder.lower(),
                        'name': self._get_collection_name(folder)
                    })
        return collections
    
    def _get_collection_name(self, folder_name):
        names = {
            'common': 'Звездные войны',
            'secret': 'Во все тяжкие',
            'prize': 'Суперы'
        }
        return names.get(folder_name.lower(), folder_name)
    
    def show_collections_menu(self, user_id, chat_id):
        user = self.db.get_user(user_id)
        if not user:
            return
        
        collections = self.get_available_collections()
        selected = user.get('selected_collections', [])
        
        markup = types.InlineKeyboardMarkup()
        for collection in collections:
            emoji = "✅" if collection['id'] in selected else "❌"
            callback_data = f"toggle_collection_{collection['id']}"
            markup.add(types.InlineKeyboardButton(
                f"{emoji} {collection['name']}",
                callback_data=callback_data
            ))
        
        markup.add(types.InlineKeyboardButton(BUTTONS['back'], callback_data="preferences_back"))
        
        self.bot.send_message(
            chat_id,
            MESSAGES['collections'],
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    def toggle_collection(self, user_id, collection_id):
        user = self.db.get_user(user_id)
        selected = user.get('selected_collections', [])
        
        if collection_id in selected:
            selected.remove(collection_id)
        else:
            selected.append(collection_id)
        
        if len(selected) == 0:
            return False, MESSAGES['collections_minimum_alert']
        
        self.db.set_collections(user_id, selected)
        return True, None
    
    def handle_collection_query(self, query, user_id, chat_id):
        collection_id = query.data.split('_')[2]
        success, error = self.toggle_collection(user_id, collection_id)
        
        if not success:
            self.bot.answer_callback_query(query.id, error, show_alert=True)
            return
        
        try:
            self.bot.delete_message(chat_id, query.message.message_id)
        except:
            pass
        
        self.show_collections_menu(user_id, chat_id)
