import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# Загружаем токен бота из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# База данных воспоминаний
MEMORIES = {
    "memory_1": {
        "text": """Я подумал и захотел создать наш с тобой маленький уголок для воспоминаний, где мы будем хранить всё, что захотим. Надеюсь, тебе понравится. 💙

Мы были вместе ещё один год. Казалось бы, простой поход в магазин, но с тобой даже такие моменты были особенными. Мне всегда было важно знать твоё мнение, поэтому выбирать обувь с тобой — не просто покупка, а настоящее удовольствие.

Тогда мы искали мне кроссовки перед моим вторым длительным отъездом на сборы в Казань. И, конечно, ты была рядом – моя верная декабристка, которая всегда поддерживает меня, куда бы я ни отправился.

P.s А ещё именно в тот день мы окончательно поняли: ты — настоящий окушок! 🐟💙""",
        "files": [
            "https://drive.google.com/uc?id=13HSjkqBBSOQwTJWdTj7ZK5gRHbKDFDqi",
            "https://drive.google.com/uc?id=1e9kr5B89m98I-o93GcZ4RlzLYnJP_9Qi"
        ]
    },
    "memory_2": {
        "text": "Текст воспоминания для QR-кода 2...",
        "files": [
            "https://drive.google.com/uc?id=YOUR_FILE_ID_3",
            "https://drive.google.com/uc?id=YOUR_FILE_ID_4",
        ]
    },
    # Добавь остальные воспоминания (memory_3 - memory_12)
}

# Обработчик команды /start с параметрами (из QR-кода)
@dp.message(CommandStart())
async def start_cmd(message: Message, command: CommandStart.Command):
    param = command.args  # Получаем аргумент команды (/start memory_1)

    if param in MEMORIES:
        memory = MEMORIES[param]

        # Отправляем текст воспоминания
        await message.answer(memory["text"])

        # Отправляем все фото/видео по порядку
        for file_url in memory["files"]:
            if file_url.endswith(".mp4"):
                await message.answer_video(file_url)
            else:
                await message.answer_photo(file_url)

    else:
        await message.answer("Привет! Отправь мне QR-код или число (1-12), и я покажу тебе воспоминание. 💙")

# Логирование
logging.basicConfig(level=logging.INFO)

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
