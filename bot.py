import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from aiohttp import web  # Фиктивный веб-сервер для Render

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
            {"url": "https://drive.google.com/uc?export=view&id=13HSjkqBBSOQwTJWdTj7ZK5gRHbKDFDqi", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1e9kr5B89m98I-o93GcZ4RlzLYnJP_9Qi", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1Bprh73cvlw8bxMYEs3UksGkfsChgSsrh", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1JKA4jqkA5oY-NEARjFczg2xqucyENPu2", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1OsGYCJvIPTZxlxti21GuLw4s9QvuxMuW", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1IYBODimHVysMnGLIA9koRJ7PKBasv2E2", "type": "video"},
            {"url": "https://drive.google.com/uc?export=view&id=1ebPBe0EBAbuySSwH1hbxA6fdyIZ16lua", "type": "video"},
            {"url": "https://drive.google.com/uc?export=view&id=1u0nhW5IHJlS8UsQsVTWdJfnJjVBnhuzk", "type": "photo"}
        ]
    },

    "memory_2": {
        "text": """Поездка в Тимашевск ✈️

Мой первый полёт на самолёте и, пожалуй, самое сложное испытание для нас, особенно для тебя. Нам было так мало времени вместе, а впереди — целая неизвестность. Мы только начинали узнавать друг друга.

Каждый вечер мы говорили часами, и с каждым словом я чувствовал, как ты становишься всё ближе, несмотря на километры. Разговоры до поздней ночи, тихий голос в динамике, оставлял только нас двоих. Я ловил каждую твою фразу, чтобы снова почувствовать тепло, спрятанное в бесконечных буквах.

С одной стороны — это было тяжело: расстояние, невозможность обнять, взглянуть в глаза. Но в этой сложности было что-то особенное. Это время научило меня чувствовать тебя даже сквозь экран, в каждом слове находить частичку тебя. Я влюблялся в тебя заново с каждым "Доброе утро" и с каждым "Доброй ночи".

Это одно из тех воспоминаний, которое греет душу. Я помню, как сильно скучал, но ещё больше помню, как сильно любил. ❤️""",
        "files": [
            {"url": "https://drive.google.com/uc?export=view&id=13aXgr3E-TT03PhV1dI03B9WI6KBjRoMC", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1nBxQwcCxB2fJ_CSTMzdhRoroiYO7cfe7", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1lxU_jddNLwWEWG78f5Cm5Gd22YqaP_G5", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=17MkezBsyPHGUoM9uEeRCYkaIaRm8q6SD", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1rKn1isNygcCP6Gj6r1R5NV9sAONZ4IyY", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1q6Hu-wSdVkb3WiRC3zQh2YZunp5XIGtF", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=18OwBYIaz8c9eQSqUVMoQckCKzMFRtco5", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1tLF1zf0MI8xaxrcFrgAhaxNzmOvXvlBG", "type": "video"},
            {"url": "https://drive.google.com/uc?export=view&id=1onMKlBlmDxP-ULp4JPkquE3Gdmh8Lejc", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1IwywkkCFLr7nj4NaZLBa0D88xG2Q4rLN", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1mhyRLws0SlMubrVv0tc-Ey_s_9R2rV5y", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1MaSU0w4avmii5Y_eXV-F9AkzocaJPYvZ", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1RDLnL5TMPXlCtD2Qb91CgyBsx0IJZFNx", "type": "photo"}
        ]
    },

    "memory_3": {
        "text": """Наш переезд в Питер

Наш с тобой переезд в Питер стал не просто началом нового, а целой историей о взрослении, поддержке и любви. Это был наш первый опыт отдельной и сразу же совместной жизни. Я помню каждый день, как приходилось успокаивать и поддерживать мою девочку перед таким важным и ответственным моментом. Хотя, если честно, я тоже волновался — но это было не так важно, потому что я безукоризненно верил, что у нас с тобой всё обязательно получится. Мы особенные.

Столько новых эмоций, незнакомых людей, надежд и встреч в то время наполнили нашу жизнь. Мы учились не только справляться с трудностями, но и радоваться самым простым вещам: утреннему чаю, вечерним разговорам и даже шумному городу.

И пусть были небольшие споры — они только делали нашу связь крепче. Совместная жизнь стала для нас чем-то больше, чем просто быт. Она превратилась в пространство, где мы строили наше «мы», где каждый день был маленьким шагом к счастью.

Всё это навсегда останется в сердце — тёплым, светлым и родным воспоминанием. ❤️""",
        "files": [
            {"url": "https://drive.google.com/uc?export=view&id=1N8DPvcaMPTbRZj2dz64Vbu40d8Ud3VcX", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1PY-nNBsbcXtfRgO9p2qavuup0d6TztwE", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=19jR1Py0gLgUv4g1cAtgSB4AtEzt_hlgT", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1lM2O4SQzc-fNfJsdUYWXGzZGDUIGz8qj", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1yFOBRhJg_B1etrKhVR0XqQPI-j-vzkl6", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1PPei5swcd3RIhJghM9Zpz2_OWFaqEPDs", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1_IGvtodv4eqoa22WEor6_nxTYtEm42La", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1XBPG5gArya8GbT2pc5EKuE3WNWyrAMUo", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1xCWSSk3ffxgZEAnSZKtxSuJ9qdj5E6Lv", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1vpj46sDR83LMBx0ermEeBIM8O949KQkn", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1h40sYUikMCPzbnIzvckLqzQK6sIXQSyW", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1AccY0D23q21jVs0iMQ3KF78-dfc_QYJY", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1YpSKtKA3RdNqWh-Tw7FggeJu0pHu4Gm4", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1kQNlSAItMdCkgDoXbGutsHXoW4Y8VS7H", "type": "photo"},
            {"url": "https://drive.google.com/uc?export=view&id=1sByD86vl9BW6apLKV6xbZeyppq9fypzl", "type": "photo"}
        ]
    }
}



# Обработчик команды /start с параметром (из QR-кода)
@dp.message(CommandStart(deep_link=True))
async def start_cmd(message: Message, command: CommandStart):
    param = command.text.split()[-1] if len(command.text.split()) > 1 else None

    if param and param in MEMORIES:
        memory = MEMORIES[param]

        # Отправляем текст воспоминания
        await message.answer(memory["text"])

        # Отправляем фото/видео в зависимости от их типа
        for file in memory["files"]:
            try:
                if file["type"] == "video":
                    await message.answer_video(file["url"])
                else:
                    await message.answer_photo(file["url"])
            except Exception:
                await message.answer(f"🔗 Не удалось загрузить файл, попробуй открыть вручную: {file['url']}")

    else:
        await message.answer("Привет! Отправь мне QR-код, и я покажу тебе воспоминание. 💙")

# Логирование
logging.basicConfig(level=logging.INFO)

# Фиктивный веб-сервер для Render (чтобы не требовал платный тариф)
async def handle(request):
    return web.Response(text="Бот работает!")

async def main():
    # Запуск бота
    bot_task = asyncio.create_task(dp.start_polling(bot))

    # Фиктивный сервер
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 10000)))
    await site.start()

    await bot_task  # Ожидание работы бота

if __name__ == "__main__":
    asyncio.run(main())
