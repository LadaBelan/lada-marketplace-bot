
import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Берём токен из переменной окружения BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Обо мне", callback_data="about"),
            InlineKeyboardButton("Портфолио", callback_data="portfolio"),
        ],
        [
            InlineKeyboardButton("Услуги и цены", callback_data="services"),
        ],
        [
            InlineKeyboardButton("Связаться со мной", callback_data="contact"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Бот-визитка Лады, дизайнера карточек и инфографики для маркетплейсов "
        "(Wildberries и Ozon).\n\n"
        "Нажмите кнопку ниже, чтобы узнать подробнее."
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=get_main_keyboard())
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            text, reply_markup=get_main_keyboard()
        )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "about":
        text = (
            "Меня зовут Лада. Я дизайнер инфографики и карточек товара для "
            "маркетплейсов (Wildberries и Ozon).\n\n"
            "Оформляю обложки и слайды с инфографикой так, чтобы покупатель за "
            "несколько секунд понял выгоды товара и добавил его в корзину.\n\n"
            "Опыт — 30+ оформленных карточек. Особенно люблю работать с "
            "косметикой и товарами для дома."
        )
    elif data == "portfolio":
        text = (
            "Мои работы:\n"
            "Pinterest — https://ru.pinterest.com/ladacotnik/\n\n"
            "По запросу могу выслать дополнительные примеры в вашей нише."
        )
    elif data == "services":
        text = (
            "Оформляю карточки товара для маркетплейсов.\n\n"
            "БАЗОВОЕ ОФОРМЛЕНИЕ\n"
            "• Обложка + 4–6 слайдов с инфографикой\n"
            "• Адаптация под Wildberries / Ozon\n\n"
            "СТАНДАРТ\n"
            "• Всё из базового\n"
            "• Помощь с текстами: заголовки, выгоды, структура слайдов\n"
            "• Лёгкий анализ конкурентов\n\n"
            "РАСШИРЕННЫЙ ПАКЕТ\n"
            "• Оформление линейки товаров\n"
            "• Разбор текущих карточек + предложения по улучшению\n\n"
            "Стоимость зависит от количества слайдов и сложности. "
            "Напишите мне, и я предложу вариант под вашу задачу."
        )
    elif data == "contact":
        text = (
            "Чтобы обсудить оформление карточек для вашего товара, "
            "напишите мне в личные сообщения:\n\n"
            "@LadaBelan\n\n"
            "Можно сразу прислать:\n"
            "• ссылку на товар / карточку,\n"
            "• маркетплейс (Wildberries или Ozon),\n"
            "• кратко — что хотите улучшить."
        )
    else:
        text = "Пожалуйста, используйте кнопки ниже."

    await query.message.edit_text(text, reply_markup=get_main_keyboard())


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN в переменных окружения")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button))

    logger.info("Bot started")

    await application.run_polling()


if name == "main":
    import asyncio

    asyncio.run(main())
