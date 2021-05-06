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
from settings import fvm_token
import main
import reg

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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
        'Bye! I hope we can talk again some day.'
    )

    return ConversationHandler.END


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, я не понял эту команду.")


def run_bot() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(fvm_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    start_handler = CommandHandler('start', main.start)
    unknown_handler = MessageHandler(Filters.command, unknown)

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
            reg.TOWN: [MessageHandler(Filters.regex('^(Да|Нет)$'), reg.town)],
            reg.RIGHTS: [MessageHandler(Filters.regex('^(Да|Нет)$'), reg.rights)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(unknown_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    run_bot()