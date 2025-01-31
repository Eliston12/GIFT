import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# База воспоминаний (Google Drive ссылки)
MEMORIES = {
    "20200214": "https://drive.google.com/uc?id=1abcdefgHIJKLMNOP",
    "20200730": "https://drive.google.com/uc?id=2hijklmnopQRSTUV",
}

# Команда /start
@dp.message(CommandStart())
async def start_cmd(message: Message):
    args = message.text.split()
    if len(args) > 1:
        date = args[1]
        await send_memory(message, date)
    else:
        await message.answer("Привет! Отправь мне дату в формате YYYYMMDD, и я покажу воспоминание.")

# Функция отправки фото/видео
@dp.message()
async def send_memory(message: Message):
    date = message.text.strip()
    if date in MEMORIES:
        file_url = MEMORIES[date]
        if file_url.endswith(".mp4"):
            await message.answer_video(file_url)
        else:
            await message.answer_photo(file_url)
    else:
        await message.answer("Я не нашёл воспоминание на эту дату. Попробуй другую!")

# Логирование
logging.basicConfig(level=logging.INFO)

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
