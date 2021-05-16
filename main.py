# Enable logging
import logging
from telegram.ext import (
    CallbackContext,
)
from telegram import ReplyKeyboardMarkup, Update

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

msgs_keyboard = [['Регистрация'], ['Сайт', 'Инст', 'Телеграм', 'ВК'],  ['Ошибка / Вопрос']]


def start(update: Update, _: CallbackContext) -> int:
    user_id, first_name = update.effective_user.id, update.effective_user.first_name
    logger.info("User %s %s run a start cmd", user_id, first_name)

    update.message.reply_text(
        '🚴 Во время регистрации Вы сможете выбрать один из вариантов участия: офлайн или онлайн. Давайте немного расскажем Вам о каждом из из них:\n\n'
        '1️⃣При офлайн варианте Вы получите карту с пикетами и будете стартовать из общей точки с другими участниками. Когда все задания выполнены, а время марафона подходит к концу, участники направляются на финиш. ❗️Такой вариант прохождения будет доступен только 12 июня. \n\n'
        '2️⃣А при онлайн варианте сможете  выбрать любой из районов с уже заготовленными точками и начать свой маршрут прямиком из дома. ❗️Такой вариант прохождения будет доступен только 13 июня.\n\n'
        'Позже все участники будут приглашены на торжественное закрытие, где состоится просмотр всех фотографий и награждение победителей 🏆 Дата будет объявлена позже\n\n'
        'Для того, чтобы <i>остановить процесс регистрации</i>, можно воспользоваться командой /cancel.\n\n'
        '<b>Нажмите на кнопку Регистрация для начала регистрации</b>',
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(msgs_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )


def contacts_cmd(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        '1. Наш руководитель @marikachek <b>Марика</b>: +375293889970'
        '2. Мой создатель @aadereiko <b>Саша</b>: +375292304825',
        parse_mode="HTML"
    )


def info_cmd(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        '🚴Во время регистрации Вы сможете выбрать один из вариантов участия: офлайн или онлайн. Давайте немного расскажем Вам о каждом из из них:\n\n'
        '1️⃣При офлайн варианте Вы получите карту с пикетами и будете стартовать из общей точки с другими участниками. Когда все задания выполнены, а время марафона подходит к концу, участники направляются на финиш. ❗️Такой вариант прохождения будет доступен только 12 июня. \n\n'
        '2️⃣А при онлайн варианте сможете  выбрать любой из районов с уже заготовленными точками и начать свой маршрут прямиком из дома. ❗️Такой вариант прохождения будет доступен только 13 июня.\n\n'
        'Позже все участники будут приглашены на торжественное закрытие, где состоится просмотр всех фотографий и награждение победителей 🏆 Дата будет объявлена позже\n\n',
        parse_mode="HTML"
    )


def unknown_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, я не понял эту команду.\n\nЕсли у Вас возникли вопросы, Вы можете написать моему создателю @aadereiko")


def web_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ссылка на наш сайт:\n\n http://fvm.by")


def tg_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ссылка на наш телеграм:\n\n https://t.me/fotovelomarafon")


def inst_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ссылка на наш инст:\n\n https://www.instagram.com/fotovelomarafon/")


def vk_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ссылка на наш вк:\n\n https://vk.com/fotovelomarafon")


def err_cmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="По всем вопросам можно написать сюда:\n\n @aadereiko")
