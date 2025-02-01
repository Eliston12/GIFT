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
    "1": {
        "text": """Я подумал и захотел создать наш с тобой маленький уголок для воспоминаний, где мы будем хранить всё, что захотим. Надеюсь, тебе понравится. 💙

Мы были вместе ещё один год. Казалось бы, простой поход в магазин, но с тобой даже такие моменты были особенными. Мне всегда было важно знать твоё мнение, поэтому выбирать обувь с тобой — не просто покупка, а настоящее удовольствие.

Тогда мы искали мне кроссовки перед моим вторым длительным отъездом на сборы в Казань. И, конечно, ты была рядом – моя верная декабристка, которая всегда поддерживает меня, куда бы я ни отправился.

P.s А ещё именно в тот день мы окончательно поняли: ты — настоящий окушок! 🐟💙""",
        "files": [
            "https://drive.google.com/file/d/13HSjkqBBSOQwTJWdTj7ZK5gRHbKDFDqi/view?usp=sharing",
            "https://drive.google.com/file/d/1e9kr5B89m98I-o93GcZ4RlzLYnJP_9Qi/view?usp=sharing",
        ]
    },
    "2": {
        "text": "Текст воспоминания для QR-кода 2...",
        "files": [
            "https://drive.google.com/uc?id=YOUR_FILE_ID_3",
            "https://drive.google.com/uc?id=YOUR_FILE_ID_4",
        ]
    },
    "3": {
        "text": "Текст воспоминания для QR-кода 3...",
        "files": [
            "https://drive.google.com/uc?id=YOUR_FILE_ID_5",
            "https://drive.google.com/uc?id=YOUR_FILE_ID_6",
        ]
    },
    # Добавь остальные воспоминания (4-12)
}

# Обработчик команды /start
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Привет! Отправь мне число (1-12) из QR-кода, и я покажу тебе воспоминание. 💙")

# Обработчик сообщений с номерами QR-кодов
@dp.message(F.text)
async def send_memory(message: Message):
    code = message.text.strip()

    if code in MEMORIES:
        memory = MEMORIES[code]

        # Отправляем текст воспоминания
        await message.answer(memory["text"])

        # Отправляем все фото/видео
        for file_url in memory["files"]:
            if file_url.endswith(".mp4"):
                await message.answer_video(file_url)
            else:
                await message.answer_photo(file_url)

    else:
        await message.answer("Я не нашёл воспоминание для этого QR-кода. Попробуй другой!")

# Логирование
logging.basicConfig(level=logging.INFO)

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
