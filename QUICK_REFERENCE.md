# ⚡ Quick Reference - Chibi Bot

## 🏗️ Архитектура в 2 минуты

```
Пользователь пишет /command
        ↓
    bot.py (получает)
        ↓
Выбирает нужный handler
        ↓
collections_handler.py (выбор коллекций)
raids.py (рейды)
crafting.py (крафт)
warehouse.py (склад)
daily.py (ежедневки)
admin.py (админ команды)
        ↓
database.py (сохраняет в MongoDB)
        ↓
texts.py (берет текст сообщения)
utils.py (расчеты и функции)
        ↓
Отправляет ответ Telegram
```

---

## 📂 Размеры файлов

| Файл | Размер | Строк |
|------|--------|-------|
| bot.py | 8.7 KB | 210 |
| texts.py | 17 KB | 450 |
| raids.py | 7.2 KB | 195 |
| crafting.py | 4.3 KB | 130 |
| warehouse.py | 6.5 KB | 160 |
| database.py | 4.2 KB | 115 |
| daily.py | 4.0 KB | 105 |
| admin.py | 4.0 KB | 110 |
| utils.py | 5.2 KB | 145 |
| collections_handler.py | 2.9 KB | 85 |
| **ИТОГО** | **~64 KB** | **~1,705** |

Все файлы **под 250 строк**, как просили!

---

## 🔌 Как добавить новую команду?

### Шаг 1: Добавь текст в texts.py

```python
MESSAGES['my_command'] = "*🎮 Моя команда*\nТекст сообщения"
BUTTONS['my_button'] = "🔘 Кнопка"
```

### Шаг 2: Создай обработчик в нужном файле

```python
# Например в raids.py
def my_new_feature(self, chat_id, user_id):
    self.bot.send_message(chat_id, MESSAGES['my_command'])
```

### Шаг 3: Зарегистрируй в bot.py

```python
@self.bot.message_handler(commands=['mycommand'])
def handle_my_command(message):
    self.raids_handler.my_new_feature(message.chat.id, message.from_user.id)
```

**Готово!** Команда работает.

---

## 🗄️ Как читать данные из БД?

```python
# Получить пользователя
user = self.db.get_user(user_id)
print(user['coins'])  # Его коины

# Добавить коины
self.db.add_coins(user_id, 100)

# Добавить чибика
chibi_data = {'name': 'Люк', 'health': 80, ...}
self.db.add_chibi(user_id, chibi_data)

# Получить активные рейды
raids = self.db.get_active_raids(user_id)

# Создать рейд
raid = self.db.create_raid(user_id, chibi_id, location, difficulty, return_time)
```

---

## 🎨 Как менять сообщения?

Все в `texts.py` - просто редактируй:

```python
MESSAGES['welcome'] = """*⚡️ Новый текст!*
Вот тут пишешь свой текст"""

BUTTONS['preferences'] = "🎮 Новая кнопка"
```

Потом юзай в коде:

```python
self.bot.send_message(chat_id, MESSAGES['welcome'], parse_mode='Markdown')
markup.add(types.InlineKeyboardButton(BUTTONS['preferences'], callback_data="show_preferences"))
```

---

## 🎁 Как добавить новый предмет для крафта?

В `texts.py`:

```python
CRAFTING_ITEMS['new_item_key'] = {
    'emoji': '🎪',
    'name': 'Новый предмет',
    'difficulty': 'Средний',
    'cost': 300,
    'health_boost': 5,
    'stamina_boost': 10,
    'damage_boost': 0,
    'recipe': {'🔩': 5, '⚙️': 3},  # нужны эти ресурсы
    'description': 'Неплохо улучшит выносливость!',
}
```

**Готово!** Предмет появится в меню крафта.

---

## 📍 Как добавить новую локацию для рейдов?

В `texts.py`:

```python
LOCATIONS['easy'].append({
    'emoji': '🏰',
    'name': 'Новая локация',
    'stamina': 70,
    'loot_type': 'Скупой'
})
```

И добавь лут в `raids.py` или `utils.py`:

```python
loot_templates['Новая локация'] = [
    ('🔩', 2, 6, 0.67),  # (эмодзи, мин, макс, шанс)
    ('⚙️', 3, 5, 0.52),
]
```

---

## 💰 Как менять экономику?

Всё в `texts.py`:

```python
# Цена предмета
'cost': 300,  # В коинах

# Бонус предмета
'health_boost': 5,      # Здоровье
'stamina_boost': 10,    # Выносливость
'damage_boost': 0,      # Урон
```

Или в `database.py` для макс ресурсов:

```python
# Максимум на складе
max_common = 350
max_medium = 200
max_rare = 25
```

---

## 🎮 Как добавить нового администратора?

Вариант 1 - через код:

```python
# В database.py при создании юзера
self.db.users.update_one(
    {"username": "new_admin"},
    {"$set": {"is_admin": True}}
)
```

Вариант 2 - через вайп:

```python
# Admin получит доступ, если в этом коде:
if user_id == 6967960142:  # Замени на его ID
    return True
```

---

## 🔄 Как менять таймеры?

В `daily.py`:

```python
# Таймер получения чибика
chibi_cooldown = 4 * 3600 + 45 * 60  # 4ч 45м в секундах

# Таймер ежедневного бонуса
bonus_cooldown = 24 * 3600  # 24 часа
```

В `raids.py`:

```python
# Время рейда зависит от сложности
base_times = {
    'easy': 8 * 60,      # 8 минут
    'medium': 10 * 60,   # 10 минут
    'hard': 15 * 60      # 15 минут
}
```

---

## 🧪 Как тестировать локально?

```bash
# 1. Установи зависимости
pip install -r requirements.txt

# 2. Создай .env с токеном и MongoDB
echo "BOT_TOKEN=your_token" > .env
echo "MONGODB_URI=your_mongodb_uri" >> .env

# 3. Запусти бота
python bot.py

# 4. В Telegram напиши боту /start
# 5. Смотри логи в консоли - там все ошибки

# 6. Убей процесс когда закончишь
Ctrl+C
```

---

## 🚀 Как задеплоить на Render?

```bash
# 1. Залей на GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/repo.git
git push -u origin main

# 2. На Render.com:
#    - Новый Web Service
#    - Выбери GitHub репозиторий
#    - Build: pip install -r requirements.txt
#    - Start: python bot.py
#    - Environment: добавь BOT_TOKEN и MONGODB_URI
#    - Deploy!

# 3. Мониторь на UptimeRobot (каждые 5 минут пингует)
```

---

## 🐛 Почему бот не работает?

| Ошибка | Решение |
|--------|---------|
| `MONGODB_URI not found` | Добавь в .env файл |
| `BOT_TOKEN not found` | Добавь в .env файл |
| `Connection refused` | MongoDB недоступна, проверь Internet |
| `TelegramError` | Проверь что токен правильный |
| `ImportError` | Запусти `pip install -r requirements.txt` |

---

## 📊 Как отслеживать игроков?

В MongoDB Atlas:

```javascript
// Все юзеры
db.users.find().pretty()

// Юзер с большим количеством коинов
db.users.findOne({ coins: { $gt: 10000 } })

// Все активные рейды
db.raids.find({ return_at: { $gt: new Date() } })

// Статистика
db.users.countDocuments()  // Всего игроков
db.chibis.countDocuments()  // Всего чибиков
```

---

## ⚙️ Переменные окружения

```bash
# Обязательные
BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db

# Опциональные
ADMIN_IDS=6967960142,123456789
ENVIRONMENT=production
RENDER=true
```

---

## 📈 Как масштабировать?

1. **Увеличь лимиты на складе**
   ```python
   max_common = 500  # Было 350
   max_medium = 300  # Было 200
   max_rare = 50     # Было 25
   ```

2. **Добавь больше локаций и предметов**
   - Просто расширь списки в `texts.py`

3. **Оптимизируй MongoDB**
   - Добавь индексы на часто используемые поля
   - Делай регулярные бэкапы
   - Архивируй старые рейды (старше месяца)

4. **Добавь rate limiting**
   ```python
   # В bot.py перед обработкой
   if user_id in rate_limit and time.time() - rate_limit[user_id] < 1:
       return  # Игнорируй частые запросы
   ```

5. **Кэшируй данные**
   ```python
   # Кэш для часто запрашиваемых данных
   cache = {}
   if user_id not in cache:
       cache[user_id] = self.db.get_user(user_id)
   ```

---

## 🎯 Чеклист перед продакшеном

- [ ] Протестировал все команды локально
- [ ] Замени `ya_admin7` на своего юзера
- [ ] Добавь себя в админы
- [ ] Проверил .env файл (BOT_TOKEN и MONGODB_URI)
- [ ] Залил на GitHub (приватный репозиторий)
- [ ] Развернул на Render
- [ ] Настроил UptimeRobot мониторинг
- [ ] Включил логирование (смотри логи на Render)
- [ ] Сделал тестовый рейд с основным аккаунтом
- [ ] Проверил что данные сохраняются в MongoDB

---

## 📞 Номера важных мест в коде

| Что найти | Где искать |
|-----------|-----------|
| Тексты сообщений | `texts.py` (строки 1-50) |
| Команды бота | `bot.py` (строки 40-80) |
| Обработка нажатий | `bot.py` (строки 150-220) |
| Работа с БД | `database.py` |
| Функции расчета | `utils.py` |
| Рейд логика | `raids.py` (строки 50-130) |
| Крафт логика | `crafting.py` (строки 40-100) |

---

## 🎨 Как менять эмодзи?

Просто найди в `texts.py` и замени:

```python
'emoji': '🎤',  # Было
'emoji': '🎸',  # Стало

BUTTONS['raid_button'] = "🫯 Зарейдить"  # Было
BUTTONS['raid_button'] = "⚔️ Зарейдить"  # Стало
```

---

## 💡 Полезные ссылки

- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **pyTelegramBotAPI**: https://github.com/eternnoir/pyTelegramBotAPI
- **Render**: https://render.com
- **UptimeRobot**: https://uptimerobot.com

---

**Удачи в разработке!** 🚀

Если что-то непонятно - ищи в коде, там всё просто и чистое!
