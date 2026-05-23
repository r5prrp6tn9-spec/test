MESSAGES = {
    'welcome': """*⚡️ Хей, {first_name}!*
Вижу, ты новичок у нас? Что ж, вероятно ты здесь, потому что любишь ЧИБИКОВ, да?
Будем считать, что я угадал. У нас тут, к слову, царский чибиздец: в одном ряду стоят джедаи, варщики синего мета и поехавшие супергерои. Полное безумие, согласись!
В любом случае, раз ты тут впервые, я тебя задобрю, и это ни в коем случае не чтобы ты тут подольше остался, даже не думай! Я очень щедр, и начислю тебе аж целый *🧧 ЧИБИ-ПАК!* Ты можешь найти и открыть его в меню, чтобы получить своего первого бойца. Также советую ознакомиться с остальными командами бота, ты тут надолго и они тебе точно пригодятся! Удачного пути, Дружище!""",
    
    'collections': """*📚 Твои коллекции*
_Те коллекции, которые тебе интересно собирать, и которые падают тебе в дейликах. Можешь нажимать на названия, чтобы включать и отключать дроп различных из них_""",
    
    'collections_minimum_alert': "🤔 Эй, друг! Минимум выбранных коллекций - одна штука!",
    
    'cantina_menu': """*🕍 Кантина*
_Отличное местечко, где можно залутать много интересного хлама и проверить своих чибиков на прочность_""",
    
    'cantina_raids': """*🪎 Рейды*
_Самые смелые могут отправить команду своих чибиков рейдить доступные зоны, чтобы они принесли полезный лут. Но у всего есть своя цена…_

До обновления локаций: *{time_left}*""",
    
    'cantina_location_info': """*{emoji} {location}*
_Во время рейда локаций можно найти много ценного! Чем сложнее — тем лучше лут. Кстати, рейд этой локации потратит {stamina}⚡️ выносливости у твоего чибика_

Сложность: *{difficulty}*
Лут: *{loot_type}*""",
    
    'cantina_select_chibi': """*{emoji} {location}*
_Выбери чибика, которого хочешь отправить рейдить эту локацию_""",
    
    'cantina_chibi_stats': """*🪎 {chibi_name}*
_Тут можно глянуть всю инфу о твоем чибике. Смотри внимательно, каждая характеристика важна!_

Его статы:
> {health} ❤️ ({health_current}/{health_max})
> {stamina} ⚡️ ({stamina_current}/{stamina_max})
> {damage} 🗡️ ({damage_current}/{damage_max})""",
    
    'cantina_raid_started': """*🪎 Ты отправил {chibi_name} рейдить {emoji} {location}*
_Удачи ему! Когда твой чибик закончит, ты сможешь забрать его вместе с наградой. Возвращайся сюда позже через:_ *{timer}*""",
    
    'cantina_raid_ready': """*🪎 Твой {chibi_name} вернулся!*
_{event}

+ {loot}*""",
    
    'cantina_raid_injured': "К сожалению, во время боя он пострадал и нуждается в помощи. Посмотри его состояние на складе",
    'cantina_raid_success': "Рейд прошел успешно! Теперь ему понадобится долгий отдых",
    
    'craft_menu': """*🛠️ Крафт*
_Здесь создаются бомбезные штуки, улучшающие показатели твоих чибиков_""",
    
    'craft_select': """*🛠️ Что крафтим?*
_Выбери, какой предмет хочешь создать_""",
    
    'craft_item_detail': """*{emoji} {item_name}*
_{description}_
_Улучшит: {boost_stats}_""",
    
    'craft_success': """*🔥 Хей, {name}*
только что скрафтил {item_name}!

+ {emoji} {item_name}""",
    
    'warehouse': """*📦 Твой склад*
Смотрри внимательно, каждая вещь на вес золота!""",
    
    'warehouse_resources': """*📦 Ресурсы*
_Максимум за рядиком: Обычные (350), Средние (200), Редкие (25)_

{resources}""",
    
    'equip_item': """*{emoji} {item_name}*
_Выбери, на кого хочешь надеть этот элемент снаряжения? Учти, что снять его уже не выйдет!_""",
    
    'equip_chibi_stats': """*{emoji} {chibi_name}*
_Выбери, на кого хочешь надеть этот элемент снаряжения?_

> {health} ❤️ [+{health_boost}]
> {stamina} ⚡️ [+{stamina_boost}]
> {damage} 🗡️ [+{damage_boost}]""",
    
    'equip_success': """*✅ Экипировано!*
{chibi_name} теперь на 100% вооружен и готов к боям!""",
    
    'wipe_confirmation': """*😱 Вайп задумал?*
_Ты вообще В СВОЕМ УМЕ?! Подумай о бедняжках-игроках… ДЛЯ ТЕБЯ ВООБЩЕ НИЧЕГГ СВЯТОГО НЕТ?! Введи пароль, если все же решишься…_""",
    
    'wipe_wrong_password': "❌ Неверный пароль! Попытка не засчитана.",
    
    'wipe_success': """*✅ ВАЙ-ПП! 🌪️*
Все данные успешно обнулены! Мир начинается заново для каждого игрока!""",
    
    'daily_chibi': "⚡️ *Тебе выпал — {chibi_name}!*\nНадеюсь, он тебе понравился!\n\nРедкость: {emoji} {rarity}\nУ тебя: {count}",
    
    'chibi_cooldown': "⚡️ *Ты уже залутал чибика в последнее время!* Возвращайся за новеньким через *{time_left}*!",
    
    'shop_thread': "Приватная ссылка на покупку",
    
    'not_yours': "🙈 *Не твое!*",
    'insufficient_coins': "💰 *Недостаточно коинов! У тебя {coins}💰",
    'injury_alert': "Твой чибик неважно выглядит! Подлатай его, пока не стало хуже. Это можно сделать при помощи 🧵 Нити из магазина",
}

BUTTONS = {
    'back': "Назад",
    'preferences': "📚 Предпочтения",
    'our_channel': "📢 Наш тгк",
    'cantina_raids': "🪎 Рейды",
    'cantina_info': "ℹ️ Инфо",
    'craft_create': "🔥 Создать",
    'craft_info': "ℹ️ Инфо",
    'select_chibi': "❇️ Выбрать чибика",
    'raid_button': "🫯 Зарейдить",
    'select_action': "✅ Выбрать",
    'lock': "🔒 {timer}",
    'unlock': "✅ Забрать чибика",
    'wipe_confirm': "🔒 Учинить расправу",
    'wipe_authorized': "✅ Учинить расправу",
    'warehouse_check': "📦 Глянуть на складе",
    'thread_link': "🧵 Нить",
}

LOCATIONS = {
    'easy': [
        {'emoji': '🛖', 'name': 'Таскенское поселение', 'stamina': 65, 'loot_type': 'Скупой'},
        {'emoji': '🍷', 'name': 'Кантина Мос Эйсли', 'stamina': 65, 'loot_type': 'Скупой'},
        {'emoji': '🏜️', 'name': 'Свалка', 'stamina': 65, 'loot_type': 'Скупой'},
        {'emoji': '🧱', 'name': 'Стройка', 'stamina': 65, 'loot_type': 'Скупой'},
        {'emoji': '🏚️', 'name': 'Притон Джесси', 'stamina': 65, 'loot_type': 'Скупой'},
        {'emoji': '🚌', 'name': 'МетЛаба на колесах', 'stamina': 65, 'loot_type': 'Скупой'},
        {'emoji': '🏪', 'name': 'Магазин электроники', 'stamina': 65, 'loot_type': 'Скупой'},
        {'emoji': '🦝', 'name': 'Подвал комикс-шопа', 'stamina': 65, 'loot_type': 'Скупой'},
    ],
    'medium': [
        {'emoji': '🗼', 'name': 'Имперский аванпост', 'stamina': 75, 'loot_type': 'Среднячок'},
        {'emoji': '🦅', 'name': 'Гнездо Синдиката', 'stamina': 75, 'loot_type': 'Среднячок'},
        {'emoji': '🏭', 'name': 'Фабрика дроидов', 'stamina': 75, 'loot_type': 'Среднячок'},
        {'emoji': '🍗', 'name': 'Фастфуд Los Pollos', 'stamina': 75, 'loot_type': 'Среднячок'},
        {'emoji': '🧺', 'name': 'Прачечная', 'stamina': 75, 'loot_type': 'Среднячок'},
        {'emoji': '⚖️', 'name': 'Офис Сола Гудмана', 'stamina': 75, 'loot_type': 'Среднячок'},
        {'emoji': '🏥', 'name': 'Сейдж Гроув', 'stamina': 75, 'loot_type': 'Среднячок'},
        {'emoji': '⚓️', 'name': 'Пирс', 'stamina': 75, 'loot_type': 'Среднячок'},
    ],
    'hard': [
        {'emoji': '🏛️', 'name': 'Храм Джедаев', 'stamina': 85, 'loot_type': 'Разнообразный'},
        {'emoji': '🌆', 'name': 'Небоскреб Корусанта', 'stamina': 85, 'loot_type': 'Разнообразный'},
        {'emoji': '🪩', 'name': 'Звезда Смерти', 'stamina': 85, 'loot_type': 'Разнообразный'},
        {'emoji': '📦', 'name': 'Охраняемый Склад', 'stamina': 85, 'loot_type': 'Разнообразный'},
        {'emoji': '🌵', 'name': 'Пустыня Картеля', 'stamina': 85, 'loot_type': 'Разнообразный'},
        {'emoji': '🏢', 'name': 'Башня Vought', 'stamina': 85, 'loot_type': 'Разнообразный'},
        {'emoji': '🏰', 'name': 'Особняк Суперов', 'stamina': 85, 'loot_type': 'Разнообразный'},
        {'emoji': '🗽', 'name': 'Статуя Свободы', 'stamina': 85, 'loot_type': 'Разнообразный'},
    ]
}

CRAFTING_ITEMS = {
    'lightaber': {
        'emoji': '🎤',
        'name': 'Самодельный световой меч',
        'difficulty': 'Легкий',
        'cost': 150,
        'health_boost': 5,
        'stamina_boost': 0,
        'damage_boost': 15,
        'recipe': {'🔩': 5, '🎚️': 2, '🗜️': 1, '⚙️': 3},
        'description': 'Неплохо так улучшит урон твоего чибика!',
    },
    'tusken_cloak': {
        'emoji': '👘',
        'name': 'Маскировка Тускена',
        'difficulty': 'Средний',
        'cost': 300,
        'health_boost': 10,
        'stamina_boost': 5,
        'damage_boost': 0,
        'recipe': {'📯': 1, '🪵': 4, '⛓️': 2},
        'description': 'Средненько улучшит здоровье и выносливость!',
    },
    'musician_trumpet': {
        'emoji': '🎺',
        'name': 'Труба Бит музыканта',
        'difficulty': 'Средний',
        'cost': 280,
        'health_boost': 0,
        'stamina_boost': 12,
        'damage_boost': 3,
        'recipe': {'🪈': 1, '🔌': 2, '🔩': 3},
        'description': 'Хорошо прокачает выносливость!',
    },
    'junk_shield': {
        'emoji': '🛡️',
        'name': 'Щит из хлама',
        'difficulty': 'Средний',
        'cost': 320,
        'health_boost': 18,
        'stamina_boost': 0,
        'damage_boost': 0,
        'recipe': {'⛓️‍💥': 6, '⚙️': 5, '⛓️': 3},
        'description': 'Отличная защита - немного улучшит здоровье!',
    },
    'death_star_plans': {
        'emoji': '💾',
        'name': 'Чертежи с планами Звезды Смерти',
        'difficulty': 'Тяжелый',
        'cost': 500,
        'health_boost': 15,
        'stamina_boost': 10,
        'damage_boost': 20,
        'recipe': {'💾': 1, '📀': 1, '💻': 1, '🎛️': 4},
        'description': 'Легендарный артефакт! Всё улучшит!',
    },
    'cook_bucket': {
        'emoji': '🧼',
        'name': 'Ведро для варки',
        'difficulty': 'Легкий',
        'cost': 160,
        'health_boost': 3,
        'stamina_boost': 8,
        'damage_boost': 0,
        'recipe': {'🔩': 4, '⛓️': 2, '🫗': 3},
        'description': 'Немного улучшит выносливость!',
    },
    'hazmat_suit': {
        'emoji': '🦺',
        'name': 'Костюм химзащиты',
        'difficulty': 'Средний',
        'cost': 350,
        'health_boost': 12,
        'stamina_boost': 8,
        'damage_boost': 0,
        'recipe': {'👔': 2, '🗜️': 2, '🔌': 2, '🧱': 2},
        'description': 'Средненько улучшит защиту и выносливость!',
    },
    'lab_setup': {
        'emoji': '⚗️',
        'name': 'Настольная лаборатория Хайзенберга',
        'difficulty': 'Средний',
        'cost': 330,
        'health_boost': 5,
        'stamina_boost': 10,
        'damage_boost': 5,
        'recipe': {'⚗️': 2, '🧰': 1, '🎚️': 2},
        'description': 'Неплохо так сбалансирует статы!',
    },
    'syndicate_briefcase': {
        'emoji': '🧳',
        'name': 'Чемодан синдиката',
        'difficulty': 'Средний',
        'cost': 310,
        'health_boost': 8,
        'stamina_boost': 0,
        'damage_boost': 8,
        'recipe': {'💰': 3, '📑': 4, '📦': 2},
        'description': 'Неплохо так улучшит боевые характеристики!',
    },
    'heisenberg_outfit': {
        'emoji': '🕶️',
        'name': 'Классный прикид Хайзенберга',
        'difficulty': 'Тяжелый',
        'cost': 480,
        'health_boost': 12,
        'stamina_boost': 8,
        'damage_boost': 18,
        'recipe': {'🕶️': 1, '🫐': 1, '🚬': 1, '👔': 2},
        'description': 'Крутой образ даст серьезные бонусы!',
    },
    'butchers_crowbar': {
        'emoji': '🔧',
        'name': 'Лом Бутчера',
        'difficulty': 'Легкий',
        'cost': 140,
        'health_boost': 0,
        'stamina_boost': 0,
        'damage_boost': 12,
        'recipe': {'🪵': 3, '🔩': 4, '⛓️': 1},
        'description': 'Хорошо улучшит урон!',
    },
    'heuy_collection': {
        'emoji': '📓',
        'name': 'Коллекция Хьюи',
        'difficulty': 'Средний',
        'cost': 290,
        'health_boost': 6,
        'stamina_boost': 4,
        'damage_boost': 6,
        'recipe': {'📓': 1, '🗞️': 4, '💡': 2},
        'description': 'Средненько улучшит все характеристики!',
    },
    'infiltration_tools': {
        'emoji': '🔑',
        'name': 'Херовина для проникновения',
        'difficulty': 'Средний',
        'cost': 270,
        'health_boost': 4,
        'stamina_boost': 6,
        'damage_boost': 10,
        'recipe': {'🧱': 2, '⛓️‍💥': 4, '🎚️': 2},
        'description': 'Хорошо поднимет урон и выносливость!',
    },
    'heavy_knuckles': {
        'emoji': '⚓',
        'name': 'Тяжелый кастет',
        'difficulty': 'Средний',
        'cost': 300,
        'health_boost': 5,
        'stamina_boost': 0,
        'damage_boost': 14,
        'recipe': {'⚓': 1, '🔐': 2, '🔩': 5},
        'description': 'Отлично улучшит урон!',
    },
    'charged_syringe': {
        'emoji': '🧪',
        'name': 'Заряженный шприц',
        'difficulty': 'Тяжелый',
        'cost': 520,
        'health_boost': 20,
        'stamina_boost': 15,
        'damage_boost': 12,
        'recipe': {'💉': 1, '🪡': 1, '🗿': 1, '🩼': 1},
        'description': 'Мощный артефакт с огромными бонусами!',
    },
}

STICKERS = {
    'raid_start': 'CAACAgIAAxkBAAFKPVhqDusTdQfg6iLvENdug9g3EwwpcAACQEgAAlZVEUqWc8vDGvLqWTsE',
    'raid_success': 'CAACAgIAAxkBAAFKPVxqDusuq9PPviPPFtAek8Ndz7MD9gAC20cAAunMEErsFsWU1iRXLDsE',
    'raid_injured': 'CAACAgIAAxkBAAFKPV9qDus7PKyeK3G6nKQSfr4zAyoQSQACKkQAAswhEUr8FXfmVOeZtDsE',
}

ADMIN_PASSWORD = 'parol_ot_waypa'
