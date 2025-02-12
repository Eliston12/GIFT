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

 },

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

 },
  "memory_6": {
    "text": """Поездка в Великий Новгород с Егором и Лизой

На весенних радостях я решил позвать Егора и Лизу к нам в гости — в наш уютный, тёплый и, конечно же, самый лучший город. Хотелось показать им всё самое красивое, все уголки, которыми мы сами восхищались... но очень быстро мы поняли, что даже не знаем, что именно показать.

Но это не имело значения. Мы просто классно тусили дома, бродили по улицам, смеялись и наслаждались моментом. Это было то самое время, когда не нужно ничего особенного — просто хорошая компания и атмосфера.

Именно с этой поездки наша беседа с ними получила своё название — майские жуки. Смешное, случайное... и немного забытое. 💛""",

    "files": [
        {"url": "https://drive.google.com/uc?export=view&id=18ngR0fHBmGTqP7CJZzGaHVWgpj4Z643O", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=18dC8kfmw0mgLjz_mPOaQlIAgz0sTWDk7", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=18riW4OWBVB0s2ZTb3X4W6zLfxpBBQp3-", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=18msYXuQFI7NVRZiYcebRNINDSwxJ-U3_", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19-apOcxfJA5hrBwzREo93PWg8jPNozvg", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19IM0Jf7Cv9kXyMjkmsj4G_e_aMq1ho2j", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19IH1DkjCw1hGK_XxwMX1ouL16ycAvGp9", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19J8Hv-xUn_4eqAjJ_Mn422hd6BYsdw5J", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19E6JCAvUrvR4FG6cmRWbTJRZScQBD882", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19Bkvx8olEM1lYyMH78ewOCTL9QXBXGL0", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1965_-1NRU2H8vcH9IlUa3cpNJouA3Ogf", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=194XI1bPQ3avtA008A9wVsKdzGVs7iGaB", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=18fV6dCwerGtcElTDfBz3BGHfza5bG03x", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=18dp5CHELEyp15qHGNdIT_ruARkcxx62q", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=18eKndsWXPqjeu6rNVjkZPXmUgCt2FOVI", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=18uYdM3Nhhzex-WIGw-Odz-L2nq3PPoHd", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=18sPDSPKqNmt_6UgWXdOrxr_SgnDQDNvS", "type": "photo"}
    ]
  },
  "memory_7": {
    "text": """Твой 21-й день рождения  

Этот день был особенным, потому что он был твоим. Я хотел подарить тебе не просто праздник, а живые и тёплые воспоминания. Тогда моя девочка поняла, какое это счастье — держать в своих ручках кучу маленьких комочков.  

Я помню, как загорелись твои глаза в тот момент, когда ты впервые взяла в руки этих маленьких, тёплых щенят. Ты поняла, какое это счастье — чувствовать их крошечные лапки.  

Это был день, наполненный радостью, улыбками. День, когда я снова убедился, что самые простые вещи делают тебя по-настоящему счастливой. ❤️""",

    "files": [
        {"url": "https://drive.google.com/uc?export=view&id=1AC3gGfCeGDdErQLPUjGWdAksDcFJkBnm", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1AFqaJnz3hlgwp32NyDOfNXnHrFtvLVsL", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1AIuoahLMkPpaboH_n_TvHDorILOBeWak", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1AAcBhkTQQu7uWgelbqklWmseENhhA-65", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19hQqsyGRjHyeL3jnhrYE5Tq2zICZGuul", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1ACDPegogVXnaDfaRxLNvHsqa8aNM3T28", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1ABeXSkiepLClHW8hozI_lpWbXlf9tKKV", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1A3BzMjIy0MbY9Q9niBqjvPwZTVKzRDgX", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=19y47ewDgNB3f7QyELCGxGUIW4emy92eb", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19s2P4cCS0JKw44ET5XtBG1tT6tk2g0Za", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=19kJM9VfbZfU1Js7rr5PJJdtH7XxqNQwJ", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=19c6dZz93LmytlFtoQM_3TilJ-7xJBv79", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=19f29HM8MPtdIQyuqWLP2JPWc4wANvU26", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=19aQMErbPt4LH2dES_onT4FC6RMn6aIeS", "type": "video"}
    ]
 },

     "memory_8" : {
    "text": """Поездка в Карелию

  Наша первая самостоятельная поездка. Мы долго планировали и ждали — и всё это было не зря. Да, не обошлось без сложностей.
  Для меня это была, наверное, лучшее путешествие за последние 5 лет. Каждый момент, проведённый рядом с тобой, делал её особенной. Эти дороги, природа, уютные вечера, разговоры — всё сложилось в одно большое и тёплое воспоминание.

  Я очень хочу повторить это снова. И, конечно, только с тобой. Может, в другом месте, но с тем же ощущением свободы, счастья и нашего с тобой маленького приключения. ❤️""",

    "files": [
        {"url": "https://drive.google.com/uc?export=view&id=1EeOKJAvFq5OWao15uqdK24FeozOpGC0n", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1E_eG8B_S7qsKhrYebqgAZVNyO32lpGEK", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1EXth8Tp92Tsuruqo6rOHLYu7HusFYeJ6", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1ETkvzwLWSp6GBoHuYXqiPD8M-9E5v7YT", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1EI7LEOyy1is9NqKjRGMBRNRKGcGU8zDS", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1EDzGLuKL53zzib2CW-RCKMwE8eLSHWwM", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1Dlsrn9rKQZuY1HLbEXtXC8iu-sUXdwgS", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1DlewaOwoMgE3cB5txaQXOOGsFjif6kNf", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1D_OTEAa28zcIcqboFWzaT1YhQtlNe-cp", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1EP_Ro4waBnWFER0RMZLR0TyMlpQbLQKr", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1E5tQ3Gmg02slU5HhFW2kjGlBJ28-ZvCt", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1E2Zmmyr4V4I5o3w0SQXBwFbeQeHsZKnf", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1DzF4hrITEO9ADPw7Otj64bIrbbzmpcdM", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1DwZeScevM6Gvvu-uT0r9zfQLkz38aCx8", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1CVeXLYzmM2JO4-wXbcBalVNRVUP_hPmr", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1CU-X1C1zH9hqtKkW3Y0QXhLQCyJpJFVi", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1CV_EIogeTb01KM1ca3RkEx12GCbPhPMU", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1DdpkAoITJUHl1F9o5zEWih9EOBTo-b3N", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1CSI_tW-KTnkNbwJ25nb8Bb0cMT4b-p8o", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1CIg6VHedJ3DbWTtvKzXhiheL9QTb-UlB", "type": "video"}
    ]
  },
 "memory_9" : {
    "text": """**Мой 19-й день рождения**  

Этот день запомнился мне не только как ещё один год жизни, но и как момент, когда ты открыла для меня новую страсть — машинки и скорость. Причём сделала это идеально: адреналин, азарт, но при этом всё в полной безопасности. Это было настоящее удовольствие, которое я, возможно, никогда бы не попробовал без тебя.  

Но на этом ты, конечно, не остановилась. Ты снова превратила мой день в праздник, где всё было именно так, как я люблю: лучшая компания (ты), крутая музыка и баллончик — маленькая, но важная деталь этого вечера.  

Каждый год ты даришь мне не просто подарки, а эмоции, которые остаются со мной надолго. И этот день — не исключение. ❤️""",

    "files": [
        {"url": "https://drive.google.com/uc?export=view&id=1GfQZTjM-yYNmWF4MzZcDDMuY2jvuY_hd", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1GpEcPM5iTXCiEp8wVtIMMdapcRheFmVl", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1GcdtORvk-fdpDNjvbUx0IrlnyiNMjjQF", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1GX0wUMBa8ofsN0NrGMkTwcnyub9-xDYl", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1GQ8qA2NrpFGfOgFSpCaKJgTtv2zvpeZE", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1G9dO82cxO2rgkDWJXM4BznqiVcZyjaH2", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1GO68xkKCSzNTXJ_7oEbuhR6ooMZxtv3L", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1GLqhnXOZLBcG5NFXWIHeru2UBTCQZhLr", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1HHawbibvyiJ_UigtMDMFE-RQfTbxv11p", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1qzhu2T7TUSPiRzuH8hn3vH9b-Xg5cd1N", "type": "photo"}
    ]
 },
 "memory_10" : {
    "text": """**Наш выпускной**  

Наш долгожданный выпускной... Такой чудесный и радостный, но в то же время тревожный. Мы были в ожидании новых возможностей и результатов экзаменов, не зная, что ждёт впереди.  

Это был не просто вечер, а символ завершения целой эпохи — детства. Мы прощались со школой, с привычной жизнью, с той лёгкостью, когда всё кажется понятным и предсказуемым. Впереди нас ждала новая, взрослая жизнь — впервые по-настоящему самостоятельная, вдвоём, в большом и неизведанном мире.  

Но в тот момент всё это уходило на второй план. Для меня самым важным было быть рядом с тобой – первой красавицей выпускного. Сопровождать тебя, видеть твои сияющие глаза, танцевать с тобой вальс… Это было по-настоящему особенное чувство.  

А впереди нас ждало лето — прекрасное, наполненное ожиданиями, планами, новыми горизонтами. Мы ещё не знали, что именно оно принесёт, но точно знали одно — это было только начало. ❤️""",

    "files": [
        {"url": "https://drive.google.com/uc?export=view&id=1KXnLc5M-uQTasheMNpjR4nko72VmPBNm", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KV6mAIygpJQYlHQOFr5SgqhCRG9cNVbl", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KUwc5yumPPlX_jkX9TtENAKxLt551D5J", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KF94wY9HuKat1s8nYBDM0mxi4gYCLrSq", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KM_6UXWFnjTPU6FI9L9qBiAqGp8F8hkh", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KIHED0uLmwU56NZJkO99-_nusrvrGFLm", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KRBSwE13owYqezZ68gYF5gMmJ3PpfWXl", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KGL0kZqxTC-5ixKoW243ytiOfqgEkX09", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1K8csHPFEOo8U4c4CvzWPUDElJhKPT10M", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1K3uAz9yRNH0Viz6AgfrMDtJNIRFmMqod", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KhQCSzSF3LFp4Z5qmG0kNwD0b_7o24Q_", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KZknUXnJybDSN7LS-yal3nCUofznWo4z", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KXoQALpe1KYZ0hGxYg2nL7jV0AHUx6Eh", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1K8gLsHpQF1l9GXzqUOeTnDQzefOYrqhc", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1K6GwmO3zja1K0MAEzTAIcxSxwHdETPK2", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1Kikj3-lPhWN_hmOv4AH4KD8UjFg7Y0gW", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1JrxNFkweE8aPN67wRN6YCIZP2TRVoFkr", "type": "video"},
        {"url": "https://drive.google.com/uc?export=view&id=1JtuLHUQ2OgmlbYgiD7IblzUHId-B8UmK", "type": "video"}
    ]
 },
    "memory_11" : {
    "text": """**Наш опыт «родителей»**  

Тогда мы почувствовали себя родителями маленького существа на две недели. Это было прекрасно и одновременно непросто.  

Нам попалась девочка с характером – и её можно понять, ведь впервые остаться без мамы с чужими людьми непросто. Но, несмотря на это, она нас полюбила и хорошо проводила с нами время.  

Мне понравилось жить с таким чудным товарищем, который выключает мне компьютер в самый неподходящий момент. Даже если это было не всегда удобно, я бы точно повторил. ❤️""",

    "files": [
        {"url": "https://drive.google.com/uc?export=view&id=1KXnLc5M-uQTasheMNpjR4nko72VmPBNm", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KV6mAIygpJQYlHQOFr5SgqhCRG9cNVbl", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KUwc5yumPPlX_jkX9TtENAKxLt551D5J", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KF94wY9HuKat1s8nYBDM0mxi4gYCLrSq", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KM_6UXWFnjTPU6FI9L9qBiAqGp8F8hkh", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KIHED0uLmwU56NZJkO99-_nusrvrGFLm", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KRBSwE13owYqezZ68gYF5gMmJ3PpfWXl", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KGL0kZqxTC-5ixKoW243ytiOfqgEkX09", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1K8csHPFEOo8U4c4CvzWPUDElJhKPT10M", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1K3uAz9yRNH0Viz6AgfrMDtJNIRFmMqod", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1K8gLsHpQF1l9GXzqUOeTnDQzefOYrqhc", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1K6GwmO3zja1K0MAEzTAIcxSxwHdETPK2", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KhQCSzSF3LFp4Z5qmG0kNwD0b_7o24Q_", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KZknUXnJybDSN7LS-yal3nCUofznWo4z", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1KXoQALpe1KYZ0hGxYg2nL7jV0AHUx6Eh", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1Kikj3-lPhWN_hmOv4AH4KD8UjFg7Y0gW", "type": "photo"},
        {"url": "https://drive.google.com/uc?export=view&id=1JrxNFkweE8aPN67wRN6YCIZP2TRVoFkr", "type": "photo"}
    ]
 },
 "memory_12" : {
    "text": """**Мы**  

Вот и настало время последней записочки, но далеко не последнего воспоминания. На самом деле, все моменты были отсортированы не по значимости, а по количеству найденных весточек и фотографий.  

Но мы ведь можем продолжать, правда? Предлагаю хотя бы иногда делать парочку милых снимков, чтобы запечатлеть наше время вместе, ведь его ценность с каждым годом только растёт.  

Это были прекрасные 5 лет, и, оглядываясь назад, я бы ничего не менял. Всё идёт так, как должно, потому что мы сами строим своё будущее. Мы вправе делать всё, что захотим, главное — вместе.  

Ты всегда рядом, всегда поддерживаешь меня, даже когда думаешь, что это бесполезно. Но это не так, моя муза.  

На конец остались фотографии из разных периодов, но мимо них я просто не смог пройти. Они — о тебе, о твоей красоте, о твоём творчестве. Давай насладимся ими напоследок. ❤️""",

    "files": [
    {"url": "https://drive.google.com/uc?export=view&id=1MRiAVcSHH8PHKhqbbzi1S4KYvimGXYl0", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NQLdLAKgq7OMVsG_MYyco-uleDw83w__", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NwiqdcjwLVWLHQdTJg513kr1D38bz2-y", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1Lf5yurvQiLHway4_9hNRkhQlHyXBqoO0", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1Ld5s7jp-J4-yaEVWJc9fl2wjqn5l1r-R", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MPMewgzcazqWseZy7Yk_AAmiYPAnpxDC", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1OPq87OYmCzFQs5E9fU6o4eK8OswYFHcp", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1M306T7PjhqPC7-930SE0BWqUYnzWt6zd", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NKBwggueBJ62H2c00iR29lzeOmYTzc-n", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NC6FOAOQwdCrW6hdIbpXDMektU2E-xon", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NL803vOg11wWZZkwr-UE3BWqk2aZ-CdZ", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MCtUavE5qq7FHPRt4UzS8m2hK308dy1z", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MMkwlAWHlN9EPU4uzcGeoTLcFFwCzTDf", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1LxjWqbeJgNBHwXVd3-Ex29qxaHlGCC1a", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MxQoYQPaVVUy0cdJELCdTNNy01bA0bq1", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1M_M5hA6Xs7OdfhRElrFUGAxReXu5zUkR", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MV2bErwfWkZh7U9IQ-plhKNPJOFG0JJS", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NrmsURJJFQU2Wk8cohonl35tKozozIk7", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MHsylpbdSBw1DKSQqF4BO4u9BzLzTnol", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1LZYYm4ZcnN7GevzydG1zo74iSLEVCPdj", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1LSTl8P6G1rzC0_CFOFBjWDRLqTT-jZ_8", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1LP2yvlqba2SW2_EYzFZM6ItUKsmm2vdj", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MQ8eafNapzxw5AiTbgzp9GYAI4NxbdcD", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MP6RaUnEuQOhzp37FC2o2RyYzPbZf5Ig", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1N-rZf3t1iyyf_QYLLc5dSc423k5szdZc", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NcjrunC42mGfwq1Tyrj9Zvw6aSnnYIMh", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NxrXItFo9PamIeeYF1gxzupi5VsAe_bQ", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NTr8Kw_7JnEH_WyJMY3eCLFNh4UDOtBW", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1M32WwpiCa0KdZThFeUf_85D561sQECj8", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1NuAXnTGYhCe2ePMaIwv0Kf231r4t72k5", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1O3-5vJU-fhOzZEgn-Cm2_xJS8eEdL4ps", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1M1RmIz5LWT-qL1Q_uNs3whJOkMsweydB", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1LaobupDdmDKxbj5nsNavfD1KG6jMXA5X", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1M5BmHeIwsJOYl4o4R7GphTS64MOQlZjQ", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1MdHiieor0IiYYP83ZTEL0I-IPzvXhCvy", "type": "photo"},
    {"url": "https://drive.google.com/uc?export=view&id=1OQJjZDd3LDAs3BbeTTGpWxHSYwnY6IR4", "type": "video"},
    {"url": "https://drive.google.com/uc?export=view&id=1OQj8F3uN2l0xSJjqGzwAGKEjUxIXr9Bq", "type": "video"}
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
