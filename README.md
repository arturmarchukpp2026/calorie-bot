# SnapCal — калорійний Telegram-бот

Telegram-бот, який рахує КБЖВ (калорії, білки, жири, вуглеводи) за фото їжі.
Користувач надсилає фото страви — бот визначає, що на ньому, оцінює вагу порції
та повертає калорійність. Розпізнавання працює через Gemini API від Google.

## Можливості

| Функція | Статус |
| --- | --- |
| Команди `/start` і `/help` | ✅ готово |
| Розпізнавання страви й КБЖВ за фото (Gemini) | ✅ готово |
| Перемикання на запасну модель, якщо основна перевантажена | ✅ готово |
| Прийом фото в боті й збереження в базу | 🔄 у роботі |
| `/today` — підсумок КБЖВ за день | 🔄 у роботі |
| Меню з кнопками, нагадування, `/week`, трекер води | 📋 заплановано |

## Стек

- Python 3.11+ (перевірено на 3.14)
- [aiogram 3](https://docs.aiogram.dev/) — Telegram-бот
- [Gemini API](https://ai.google.dev/) (`google-genai`) — розпізнавання їжі
- SQLite — збереження прийомів їжі
- python-dotenv — секрети з файлу `.env`

## Структура проєкту

```
calorie-bot/
├── bot/
│   ├── main.py        # запуск бота
│   ├── handlers.py    # команди та обробка повідомлень
│   ├── vision.py      # запит до Gemini, розбір відповіді
│   └── db.py          # база даних
├── test_vision.py     # перевірка розпізнавання на своїх фото
├── requirements.txt
├── .env.example       # шаблон для ключів
└── README.md
```

## Як запустити

### 1. Що потрібно встановити

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- Токен Telegram-бота — створіть бота в [@BotFather](https://t.me/BotFather) командою `/newbot`
- Ключ Gemini API — [Google AI Studio](https://aistudio.google.com) → Get API key

### 2. Клонувати репозиторій

```bash
git clone https://github.com/arturmarchukpp2026/calorie-bot.git
cd calorie-bot
```

### 3. Створити віртуальне середовище і встановити бібліотеки

Windows (Git Bash):
```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Додати ключі

Скопіюйте шаблон і впишіть свої значення:
```bash
cp .env.example .env
```
```
BOT_TOKEN=токен_від_BotFather
GEMINI_API_KEY=ключ_з_AI_Studio
```
⚠️ Файл `.env` не можна комітити — він уже доданий у `.gitignore`.

### 5. Запустити бота

```bash
python -m bot.main
```
Відкрийте свого бота в Telegram і надішліть `/start`.

### Перевірити розпізнавання без бота

Покладіть фото їжі в корінь проєкту як `test.jpg` (або кілька фото в папку `test_photos/`):
```bash
python -u test_vision.py test.jpg
python -u test_vision.py test_photos/*
```
Приклад результату:
```
{'is_food': True, 'dish': 'Шаурма з куркою та овочами', 'weight_g': 350, 'calories': 595, 'protein': 32, 'fat': 25, 'carbs': 60}
```

## Можливі проблеми

| Проблема | Рішення |
| --- | --- |
| `ModuleNotFoundError: No module named 'bot'` | Запускайте з кореня проєкту: `python -m bot.main` |
| `Permission denied` для `pip` або `DLL load failed … Application Control policy` (Windows) | Windows Smart App Control блокує файли бібліотек. Використовуйте `python -m pip` і за потреби вимкніть Smart App Control у «Безпеці Windows» |
| `503 UNAVAILABLE` від Gemini | Модель перевантажена — бот сам пробує наступну модель зі списку `MODELS` у `bot/vision.py` |
| `404 NOT_FOUND` для моделі | Назва моделі застаріла — оновіть список `MODELS` у `bot/vision.py` |
| `Conflict: terminated by other getUpdates` | Бот з тим самим токеном уже запущений в іншому місці |

> Оцінки КБЖВ — це приблизний розрахунок моделі за фото, а не точне зважування.

## Команда

| Учасник | GitHub | Роль |
| --- | --- | --- |
| Артур | [@arturmarchukpp2026](https://github.com/arturmarchukpp2026) | Telegram-бот, структура проєкту |
| Андрій Цимбалістий | [@andriy181-1](https://github.com/andriy181-1) | Розпізнавання їжі (Gemini), README |
| Назарій | [@nazariikondiukpp2026-cyber](https://github.com/nazariikondiukpp2026-cyber) | База даних і статистика |

Задачі ведемо в Jira за Scrum, кожна задача — окрема гілка `feature/SCRUM-<номер>-...` і Pull Request з рев'ю.  Daily проводимо щодня в чаті команди.
