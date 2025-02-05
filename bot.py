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
            {"url": "https://drive.google.com/uc?export=view&id=1h40sYUikMCPzbnIzvckLqzQK6sIXQSyW", "type": "photo"}
        ]
    },

    "memory_4": {
        "text": """Поездка в Казань ✈️

Поездка в Казань, сборы перед важным этапом — поездкой на Европу. Мы провели прекрасное время вместе тем летом, и в этот раз уезжать было гораздо сложнее. Мы уже знали, каково это — быть на расстоянии. Мы ощутили все его тяготы и пустоту, которая остаётся, когда не можешь обнять любимого человека. Но именно поэтому я ценил каждое мгновение рядом с тобой ещё сильнее.

Ты всегда была рядом, даже когда я был далеко. Ты помогала мне договариваться с преподавателями, поддерживала, когда становилось тяжело. Я упорно готовился к соревнованиям, надеясь оправдать не только твои надежды, но и свои ожидания. Мы пытались быть ближе хотя бы виртуально — в твоей любимой игре. Каждый раз, когда наши персонажи встречались, я чувствовал, что несмотря на все километры между нами, мы немного ближе. Это были не просто пиксели на экране, а ещё один способ сказать друг другу: "Я рядом".

Но самое важное — я знал, что каждый вечер ты ждёшь меня. Ждёшь моего звонка, моей весточки. Эта мысль давала мне силы и уверенность, что мы всё равно рядом. ❤️""",
        "files": [
        {"url": "https://drive.google.com/uc?export=view&id=1Iunch-gMNLQpRNc55EOc6ADsA5CN4GN6", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1MnyGkrQz9U08Yjk9Dw1xsyETKNLF5Q9I", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1Sf7sF_s4FGchJwIyYV8aPYp4pEzrFHzQ", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1fPLyKgMvwQp6IwDYMVSwfbdA22MhOzsC", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1M_GsvqquLmG3M6xdXBoNra7HGUc8_AKc", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1aYLIolAovdAni56aHByCs9ML6XdX-5uk", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1LvR4MzLYGGRmCH9w1SnIqSi6jucTkBIC", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1f6q5HIH22bil7OWPz5DHy5v6aPAYd7U1", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1bDW1CpO1sJ6o7ioiuq04u-G5Braq1CkF", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1O472pCBGwCKAZFcLnEhF1t7ZMX03AMUO", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1K9RmNUp3zB04PGbKD3qQv6xlElxsvAhn", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1XWoY-vvr_FPnfZLmJvtXwa6eUcXVQNMG", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1yBmEnLYj08-UP3zAPP-fBRgx6Ut2v3qZ", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1B_g8jzujuDb6FzFg74UiGOtV9E-RebRX", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1kEPU_j77-DfeMQdCVkUO1fqNg3pCfeC-", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=158aHaCq_SVTvKYrW688N1GU1z1FbtVUM", "type": "video"}
    ]

 }

 "memory_5": {
        "text": """Поездка в Шанти Хоум с Егором и Лизой

Поездка в Шанти Хоум с Егором и Лизой — это время, когда всё сложилось удивительно легко и просто. Мы отлично проводили время вместе, и, наверное, это была самая удачная поездка за город. Приятная компания, вкусная еда, интересные игры и, конечно, котики с лисами, которые добавляли уюта и особого настроения. Атмосферное и красивое место, где каждый момент казался чуть теплее и ближе к сердцу. ❤️""",
         "files": [
        {"url": "https://drive.google.com/uc?export=view&id=177gbfYd2XnG0piKPJ1laRmfmlqFEz-FI", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=17QH1T4LbV8fmBnkFpB5ILRiai7S-7F9b", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=16QM45RQnWErcnRl4UQkFkesM8TI_I38n", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=17Y7RULb8tO40gXsJxLykfdFAvdeuvihM", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=16cY6idCt_eL1Er4_0FOoZbKIAQcJtlUw", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=17DnIHQ168cwl60FXi4Myil4GnfsLKofw", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=171QgLM3tekqVbvOseJdvVzOmVVqJOL-F", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=179F31Fzh5O-jV6DLKT9DPqyH_gU2obnn", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=17LHpzHDPZoGuRrKT9nTaGlkomspw6i3r", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=172gUNJ6xQ17NhiUKPgbGUpcuOM-KTPZX", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=16Qny0FWWRMPtLEZcQDwI8MnjVspbRGqn", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=174h0wKxgSIbmLd4siDDteP2asRU5a_4Y", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=17SXLwCNj4ofiynOqRLMYxWqcOGTBgUN-", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=16u9cozSpB2jcHJuzZjGZp3pWqcts2F2R", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=16zAgW9gl04DJKXOMY00gQ6PTLI9FNYTT", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=16s3RYg3zUXl7UUKs3AH_PHNZCJWjGRpq", "type": "video"}
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
