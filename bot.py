"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging

import settings
from settings import fvm_token
import main
import reg
import users

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Очень жаль! Надеюсь, что Вы к нам вернетесь.',
        reply_markup=ReplyKeyboardMarkup(main.msgs_keyboard, one_time_keyboard=True, resize_keyboard=True),

    )

    return ConversationHandler.END


def run_bot() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(fvm_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', main.start)
    contacts_handler = CommandHandler('contacts', main.contacts_cmd)
    info_handler = CommandHandler('info', main.info_cmd)
    unknown_handler = MessageHandler(Filters.command, main.unknown_cmd)

    inst_handler_msg = MessageHandler(Filters.regex('Инст'), main.inst_cmd)
    inst_handler_cmd = CommandHandler('inst', main.inst_cmd)

    vk_handler_msg = MessageHandler(Filters.regex('ВК'), main.vk_cmd)
    vk_handler_cmd = CommandHandler('vk', main.vk_cmd)

    web_handler_msg = MessageHandler(Filters.regex('Сайт'), main.web_cmd)
    web_handler_cmd = CommandHandler('web', main.web_cmd)

    tg_handler_msg = MessageHandler(Filters.regex('Телеграм'), main.tg_cmd)
    tg_handler_cmd = CommandHandler('tg', main.tg_cmd)

    error_handler_msg = MessageHandler(Filters.regex('Ошибка / Вопрос'), main.err_cmd)
    error_handler_cmd = CommandHandler('error', main.err_cmd)

    users_handler_cmd = CommandHandler('users', users.users_cmd)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^Регистрация$'), reg.register)],
        states={
            reg.NAME: [MessageHandler(Filters.text & ~Filters.command, reg.name)],
            reg.IS_ONLINE: [MessageHandler(Filters.regex('^(Онлайн|Оффлайн)$'), reg.is_online)],
            reg.TRANSPORT: [MessageHandler(Filters.regex('^(Велосипед|Самокат|Электросамокат|Ролики|Скейтборд|Бег)$'), reg.transport)],
            reg.PHONE: [
                MessageHandler(Filters.text & ~Filters.command, reg.phone),
                # CommandHandler('skip', skip_location),
            ],
            reg.AGE: [MessageHandler(Filters.text & ~Filters.command, reg.age)],
            reg.HAS_PARTICIPATED: [MessageHandler(Filters.regex('^(Да|Нет)$'), reg.has_participated)],
            reg.IS_PHONE: [MessageHandler(Filters.regex('^(Телефон|Фотоаппарат)$'), reg.is_phone)],
            reg.OCCUPATION: [MessageHandler(Filters.text & ~Filters.command, reg.occupation)],
            reg.HOW_MET: [MessageHandler(Filters.text & ~Filters.command, reg.how_met)],
            reg.IS_PAPER: [MessageHandler(Filters.regex('^(Да|Нет)$'), reg.is_paper)],
            reg.TOWN: [MessageHandler(Filters.text & ~Filters.command, reg.town)],
            reg.RIGHTS: [MessageHandler(Filters.regex('^(Да|Нет)$'), reg.rights)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(inst_handler_msg)
    dispatcher.add_handler(inst_handler_cmd)
    dispatcher.add_handler(vk_handler_msg)
    dispatcher.add_handler(vk_handler_cmd)
    dispatcher.add_handler(web_handler_msg)
    dispatcher.add_handler(web_handler_cmd)
    dispatcher.add_handler(tg_handler_msg)
    dispatcher.add_handler(tg_handler_cmd)
    dispatcher.add_handler(error_handler_msg)
    dispatcher.add_handler(error_handler_cmd)

    dispatcher.add_handler(users_handler_cmd)

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(contacts_handler)
    dispatcher.add_handler(info_handler)

    # should be last one
    dispatcher.add_handler(unknown_handler)


    # Start the Bot

    if settings.is_local:
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                              port=settings.PORT,
                              url_path=settings.fvm_token,
                              webhook_url="https://fvmbotv2.herokuapp.com/" + settings.fvm_token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    run_bot()