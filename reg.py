# Enable logging
import logging
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
import db
import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

NAME, IS_ONLINE, TRANSPORT, PHONE, AGE, HAS_PARTICIPATED, IS_PHONE, OCCUPATION, HOW_MET, IS_PAPER, TOWN, RIGHTS = range(12)

options_msg = "\n\n" \
              "<i>На данный вопрос Вы должны <b>выбрать</b> ответ из ниже перечисленных вариантов. " \
              "Если Вы не видите возможные варианты, просто нажмите на кнопку их отображения" \
              " (она находится справа в поле ввода)</i>"

stop_msg = "\n\n" \
           "<i>Для того, чтобы остановить процесс регистрации, можно воспользоваться командой /cancel " \
           "(достаточно просто кликнуть).</i>"

def register(update: Update, context: CallbackContext) -> int:
    first_name, user_id = update.effective_user.first_name, update.effective_user.id
    logger.info("User %s %s started registration", user_id, first_name)

    context.user_data['user_id'] = str(user_id)
    context.user_data['username'] = str(update.effective_user.username)
    context.user_data['tg_name'] = str(update.effective_user.first_name) + " " + str(update.effective_user.last_name)

    update.message.reply_text(
        'Привет, меня зовут ФотоВело Бот 🤖.\n'
        'Рад приветствовать Вас в этом сезоне! '
        'Надеюсь, что мы подружимся!\n'
        'Для начала представьтесь (фамилия, имя) \n\n'
        '<b>Например:</b>\n'
        'Иванович Иван' + stop_msg,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )

    return NAME


def name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['Онлайн', 'Оффлайн']]
    logger.info("Name of %s: %s", user.first_name, update.message.text)

    context.user_data['name'] = update.message.text

    update.message.reply_text(
        'Приятно познакомиться! Теперь, пожалуйста, выберите в каком формате Вы планируете участвовать?' + options_msg + stop_msg,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         resize_keyboard=True),
        parse_mode = "HTML"
    )

    return IS_ONLINE


def is_online(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Is online of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [['Велосипед', 'Самокат', 'Электросамокат'], ['Ролики', 'Скейтборд', 'Бег']]

    context.user_data['is_online'] = update.message.text == "Онлайн"

    update.message.reply_text(
        'Прекрасно!\n'
        'А сейчас можете выбрать транспорт, на котором Вы планируете принимать участие' + options_msg + stop_msg,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return TRANSPORT


def transport(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Is online of %s: %s", user.first_name, update.message.text)

    context.user_data['transport'] = update.message.text

    update.message.reply_text(
        'Прекрасно! А сейчас можете написать номер мобильного телефона, '
        'по которому можно будет выйти с Вами на связь?\n\n'
        '<b>Например:</b>\n'
        '+375292304825' + stop_msg,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHONE


def phone(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Phone of %s: %s", user.first_name, update.message.text)

    context.user_data['phone'] = update.message.text

    update.message.reply_text('Спасибо!\n'
                              'Можете написать количество полных лет на момент участия в мероприятии?\n\n'
                              '<b>Например:</b>\n'
                              '18' + stop_msg,
                              parse_mode="HTML")

    return AGE


def age(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Age of %s: %s", user.first_name, update.message.text)

    context.user_data['age'] = update.message.text

    reply_keyboard = [['Да', 'Нет']]
    update.message.reply_text('Участвовали ли Вы ранее в фотовело?' + options_msg + stop_msg,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               resize_keyboard=True),
                              parse_mode="HTML"
                              )

    return HAS_PARTICIPATED


def has_participated(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s participation is %s", user.first_name, update.message.text)

    context.user_data['has_participated'] = update.message.text == "Да"

    reply_keyboard = [['Телефон', 'Фотоаппарат']]
    update.message.reply_text('Вы планируете делать фото с помощью телефона или камеры?' + options_msg + stop_msg,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                               one_time_keyboard=True,
                                                               resize_keyboard=True),
                              parse_mode="HTML"
                              )

    return IS_PHONE


def is_phone(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Way of taking photos of %s is %s", user.first_name, update.message.text)

    context.user_data['way'] = "phone" if update.message.text == "Телефон" else "camera"

    update.message.reply_text('Скажите, кем Вы работаете и/или на кого учитесь?\n\n'
                              '<b>Например:</b>\n'
                              'Учитель математики, студент 3-го курса ФПМИ' + stop_msg,
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode="HTML"
                              )

    return OCCUPATION


def occupation(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Occupation of %s is %s", user.first_name, update.message.text)

    context.user_data['occupation'] = update.message.text

    update.message.reply_text('А как Вы узнали о фотовело?\n\n'
                              '<b>Например:</b>\n'
                              'Подсказали друзья, вк, инстаграм' + stop_msg,
                              parse_mode="HTML")

    return HOW_MET


def how_met(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user

    logger.info("how_met of %s is %s", user.first_name, update.message.text)
    context.user_data['how_met'] = update.message.text

    reply_keyboard = [['Да', 'Нет']]
    update.message.reply_text('Стоит ли печатать Вам продукцию на бумаге?' + options_msg + stop_msg,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               resize_keyboard=True),
                              parse_mode="HTML")

    return IS_PAPER


def is_paper(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("is paper of %s is %s", user.first_name, update.message.text)

    context.user_data['is_paper'] = update.message.text == "Да"

    reply_keyboard = [['Да', 'Нет']]
    update.message.reply_text('Знаете ли Вы, что в мероприятии можно принимать участие только в Минске?' + options_msg + stop_msg,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               resize_keyboard=True),
                              parse_mode="HTML")

    return TOWN


def town(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("is town ok for %s is %s", user.first_name, update.message.text)

    context.user_data['is_town'] = update.message.text == "Да"

    reply_keyboard = [['Да', 'Нет']]
    update.message.reply_text('Всю написанную здесь информацию Вы можете изменить позже, я дам об этом знать.\n\n'
                              'Нажимая кнопку <b>Да</b>, Вы подтверждаете, что согласны с нашими правилами:\n'
                              '1. Участник обязан знать правила дорожного движения и соблюдать их.\n'
                              '2. Участник сам несет ответственность за себя и свое здоровье.\n\n'
                              'Завершить регистрацию?' + options_msg + stop_msg,
                              parse_mode="HTML",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               resize_keyboard=True))

    return RIGHTS


def rights(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("user %s is agreed with rights %s", user.first_name, update.message.text)

    if update.message.text == "Да":
        update.message.reply_text('Спасибо, регистрация окончена, скоро свяжемся с Вами 🤖',
                                  reply_markup=ReplyKeyboardRemove())
        logger.info("User %s finished registration", user.first_name)

        if db.write_user_to_db(context.user_data):
            settings.bot.send_message(chat_id=settings.ader_id, text=f"💪 Пользователь <b>{context.user_data['name']}</b>"
                                                            f" успешно зарегистрирован!", parse_mode="HTML")
            settings.bot.send_message(chat_id=settings.marika_id, text=f"💪 Пользователь <b>{context.user_data['name']}</b>"
                                                            f" успешно зарегистрирован!", parse_mode="HTML")
    elif update.message.text == "Нет":
        update.message.reply_text('Очень жаль, надеюсь, что Вы еще захотите ко мне вернуться 🤖',
                                  reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
