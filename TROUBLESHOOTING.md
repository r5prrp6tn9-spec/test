# 🔧 Troubleshooting Guide - Решение проблем

## 🚨 Критические ошибки

### ❌ MONGODB_URI not found in environment variables

**Симптомы:**
```
ValueError: MONGODB_URI not found in environment variables
Бот не запускается
```

**Решение:**

1. Проверь .env файл в корне проекта:
```bash
cat .env
```

Должно быть:
```
BOT_TOKEN=123456789:ABCDEFGHIJKLMNOP...
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
```

2. Если файла нет, создай:
```bash
cp .env.example .env
```

3. Отредактируй с реальными значениями (не копируй просто примеры!)

4. Перезапусти бот:
```bash
python bot.py
```

---

### ❌ BOT_TOKEN not found

**Симптомы:**
```
ValueError: BOT_TOKEN not found in environment variables
```

**Решение:**

1. Открой .env файл
2. Проверь что там есть строка:
```
BOT_TOKEN=твой_токен_здесь
```

3. Получи новый токен:
   - Напиши @BotFather в Telegram
   - `/newbot` → следуй инструкциям
   - Скопируй полученный токен в .env

4. Убедись что НЕ СКОПИРОВАЛ в одну строку:
```
# ❌ Неправильно
BOT_TOKEN=token,MONGODB_URI=uri

# ✅ Правильно
BOT_TOKEN=token
MONGODB_URI=uri
```

---

### ❌ ConnectionFailure: Не могу подключиться к MongoDB

**Симптомы:**
```
pymongo.errors.ServerSelectionTimeoutError
Не могу подключиться к базе
```

**Решение:**

1. Проверь интернет соединение
2. В MongoDB Atlas добавь IP адрес:
   - На atlas.mongodb.com
   - Проект → Network Access
   - "Add IP Address"
   - Нажми "Allow access from anywhere" (0.0.0.0/0)

3. Убедись что CONNECTION STRING правильный:
   - В Atlas: Databases → Connect
   - "Drivers" → Python
   - Скопируй строку
   - Замени `<username>`, `<password>`, `<dbname>`

4. Перепроверь в .env:
```bash
# Примерно должно быть так (но с твоими данными):
MONGODB_URI=mongodb+srv://admin:MyPassword123@cluster0.mongodb.net/chibibot
```

5. Перезапусти:
```bash
python bot.py
```

---

### ❌ ModuleNotFoundError: No module named 'telebot'

**Симптомы:**
```
ModuleNotFoundError: No module named 'telebot'
```

**Решение:**

1. Установи зависимости:
```bash
pip install -r requirements.txt
```

2. Если не помогло, установи вручную:
```bash
pip install pyTelegramBotAPI==4.14.0
pip install pymongo==4.6.0
pip install python-dotenv==1.0.0
```

3. Проверь что установилось:
```bash
pip list | grep -i telebot
```

Должно быть:
```
pyTelegramBotAPI  4.14.0
```

---

## ⚠️ Проблемы при запуске

### ❌ Бот запустился но не отвечает на команды

**Решение:**

1. Проверь что бот запущен:
```bash
# Должен вывести "ChibiBot initialized successfully"
python bot.py
```

2. В Telegram напиши боту `/start`

3. Если не отвечает:
   - Убедись что используешь **ПРАВИЛЬНЫЙ** BOT_TOKEN
   - Проверь что бот не запущен несколько раз одновременно:
   ```bash
   ps aux | grep bot.py
   ```

4. Если много процессов, убей их:
```bash
killall python
```

5. Запусти заново:
```bash
python bot.py
```

---

### ❌ Ошибка при /start команде

**Симптомы:**
```
Бот молчит или пишет "Ошибка"
```

**Решение:**

1. Посмотри логи в консоли (там будет ошибка):
```bash
python bot.py
# Ищи красные строки с traceback
```

2. Если ошибка с БД:
   - Проверь интернет
   - Проверь MongoDB подключение (см. выше)

3. Если ошибка с правами:
   - Убедись что не запустил `/start` дважды с одного аккаунта
   - Создай нового пользователя в Telegram (или используй бота в другом чате)

---

### ❌ Команда /chibi не дает чибика

**Причины:**
1. Прошло меньше 4ч 45м с последнего получения
2. Чибиков нет в папке `chibis/`

**Решение:**

1. Проверь таймер:
```bash
python bot.py
# Должна быть ошибка типа:
# "⚡️ Ты уже залутал чибика в последнее время! Возвращайся за новеньким через..."
```

2. Проверь папку с чибиками:
```bash
ls -la chibis/common
ls -la chibis/secret
ls -la chibis/prize
```

Должны быть PNG файлы. Если нет - распакуй архив правильно!

3. Если папка пуста:
   - Переместись в папку проекта
   - Распакуй архив еще раз
   - Убедись что папка `chibis/` скопировалась

---

## 🌐 Проблемы на Render

### ❌ "Deployment failed"

**Решение:**

1. Проверь что добавил переменные окружения:
   - Render → Service → Environment
   - Должны быть:
     - `BOT_TOKEN`
     - `MONGODB_URI`

2. Проверь что файлы загружены на GitHub:
```bash
git status
# Должны быть все Python файлы
```

3. Проверь что requirements.txt имеет правильное имя (не .txt.txt!)

4. Посмотри логи на Render:
   - Render → Service → Logs
   - Ищи красные строки ошибок

---

### ❌ Бот на Render падает через 15 минут

**Это нормально!** Render убирает бесплатные сервисы через 15 минут бездействия.

**Решение:**

1. Настрой UptimeRobot:
   - uptimerobot.com → "Add Monitor"
   - Type: HTTP(s) Ping
   - URL: твой Render сервис URL (из Render → About)
   - Check interval: 5 minutes
   - Сохрани

Теперь бот всегда будет "живой" потому что UptimeRobot пингует каждые 5 минут!

---

### ❌ "Cannot GET /"

**Это нормально!** Бот не имеет веб интерфейса.

Render просто выполняет `python bot.py` в фоне. Это правильно работает.

Проверь что бот отвечает в Telegram (напиши `/start`).

---

## 🗄️ Проблемы с MongoDB

### ❌ "database.yaml not found"

**Решение:**

Это не нужно. Игнорируй эту ошибку, она просто предупреждение MongoDB.

---

### ❌ "User is not allowed to access"

**Симптомы:**
```
unauthorized: authentication failed
```

**Решение:**

1. Проверь USERNAME и PASSWORD в MONGODB_URI:
```
mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/db
                ^--------  ^--------
                Проверь эти значения
```

2. Проверь что пароль без спецсимволов или правильно encoded:
   - Если пароль: `MyPass@123!`
   - В URI: `MyPass%40123%21` (@ = %40, ! = %21)

3. В Atlas создай нового пользователя:
   - Database → Database Access
   - "Add Database User"
   - Username: `admin`
   - Password: `SimplePassword123` (без спецсимволов)
   - Сохрани и скопируй новую CONNECTION STRING

---

### ❌ "Command count not supported"

**Решение:**

Это не критично. MongoDB М0 (бесплатный) имеет ограничения.

Бот все еще работает. Просто игнорируй.

---

## 🐛 Странное поведение в игре

### ❌ Чибик не получается в рейде

**Решение:**

1. Проверь что чибик выбран:
```bash
# На складе должны быть чибики
python bot.py
# Напиши /warehouse → выбери "Чибики"
```

2. Если чибиков нет:
   - Получи чибика: `/chibi`
   - Подожди 4ч 45м если прошел таймер
   - Или создай нового пользователя в Telegram

3. Проверь что чибик не ранен (здоровье > 0)

---

### ❌ Крафт не дает предметы

**Решение:**

1. Проверь что хватает коинов:
   - `/warehouse` → "Ресурсы"
   - Смотри сколько коинов

2. Проверь что хватает ресурсов для крафта:
   - `/warehouse` → "Ресурсы"
   - Посмотри рецепт в `/craft`
   - Сравни требуемые ресурсы с имеющимися

3. Если не хватает:
   - Ходи в рейды: `/cantina` → выбери локацию
   - Получишь лут после рейда

---

### ❌ Рейд бесконечно ждет

**Решение:**

1. Проверь таймер на кнопке рейда:
   - Кнопка должна показывать "🔒 15м 30с"
   - Когда время вышло → "✅ Забрать чибика"

2. Если таймер зависает:
   - Перезагрузи бота на Render
   - Или локально: `Ctrl+C` и `python bot.py`

3. Если рейд давно прошел но не видно кнопки:
   - Проверь MongoDB что рейд завершился:
   ```bash
   # В MongoDB Atlas Databases → Browse Collections → raids
   # Ищи свой рейд в истории
   ```

---

## 📊 Проблемы с производительностью

### ⚠️ Бот медленно отвечает

**Решение:**

1. Проверь интернет соединение
2. Проверь что MongoDB онлайн (Atlas → Overview)
3. Если медленно на Render:
   - Это может быть потому что сервер "просыпается"
   - Ждет 5-10 секунд первый раз - это нормально
   - Потом будет быстро

---

### ⚠️ Много ошибок в логах

**Решение:**

1. Посмотри какие конкретно ошибки:
```bash
python bot.py 2>&1 | grep -i error
```

2. Если ошибки про "message not found":
   - Это нормально если пользователь удалил сообщение
   - Бот просто пытался его обновить

3. Если ошибки про MongoDB:
   - Проверь интернет
   - Проверь что кластер активен в Atlas

---

## 🆘 Если ничего не помогло

### Полный перезапуск

1. **Локально:**
```bash
# Убей все Python процессы
killall python

# Удали .env
rm .env

# Создай новый
cp .env.example .env
# Отредактируй с новыми значениями

# Запусти
python bot.py
```

2. **На Render:**
   - Render → Service → Redeploy
   - Дождись "Your service is live"

3. **MongoDB:**
   - Atlas → Database → Collections
   - Удали все коллекции и пересоздай
   - Или просто создай новый кластер

---

### Проверь все еще раз

Чеклист:

- [ ] BOT_TOKEN из @BotFather (не из примера)
- [ ] MONGODB_URI из Atlas (с правильным пользователем и паролем)
- [ ] Интернет соединение работает
- [ ] IP адрес добавлен в MongoDB Network Access (0.0.0.0/0)
- [ ] Папка `chibis/` есть и в ней есть файлы
- [ ] requirements.txt установлены (`pip install -r requirements.txt`)
- [ ] Файлы Python есть: bot.py, database.py, texts.py, etc.
- [ ] Нет опечаток в путях и именах файлов

---

### Самый последний вариант

Если совсем ничего не работает:

1. **Скачай архив заново** и распакуй в чистую папку
2. **Создай новый токен** у @BotFather
3. **Создай новый кластер** в MongoDB Atlas (бесплатный)
4. **Начни с нуля** - часто это быстрее чем искать ошибку

---

## 📞 Где искать помощь

| Проблема | Где найти помощь |
|----------|-----------------|
| Ошибки MongoDB | mongodb.com/docs |
| Ошибки pyTelegramBotAPI | github.com/eternnoir/pyTelegramBotAPI/issues |
| Проблемы на Render | render.com/docs |
| Баги в коде | Смотри логи в консоли (там четкое описание) |

---

**Удачи! 🚀 И помните - в 90% случаев это просто ошибка в .env файле!**
