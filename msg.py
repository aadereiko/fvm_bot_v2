import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)
import db
import common

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

WHOM, MSG = range(2)
CALLBACK_QUERY_PATTERN = "msg-to:"


def msg_cmd(update: Update, context: CallbackContext):
    first_name, user_id = update.effective_user.first_name, update.effective_user.id
    logger.info("[MSG]: User %s %s used /msg command", user_id, first_name)

    users_to_write = db.get_users({"lead_id": str(user_id)})

    reply_markup = InlineKeyboardMarkup(common.generate_inline_keyboard_from_users(
        users_to_write,
        ["name", "lead_id"],
        CALLBACK_QUERY_PATTERN
    ))

    update.message.reply_text("Кому будешь писать?\n", reply_markup=reply_markup)

    return WHOM


def whom_state(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    first_name, user_id = update.effective_user.first_name, update.effective_user.id
    logger.info("[MSG]: User %s decided to write to %s", first_name, query.data)

    return MSG


def msg_state(update: Update, context: CallbackContext):
    first_name, user_id = update.effective_user.first_name, update.effective_user.id
    logger.info("[MSG]: User %s decided to write to %s the msg", user_id, first_name)

    return ConversationHandler.END


msg_states = {
  WHOM: [CallbackQueryHandler(whom_state, pattern=f"^{CALLBACK_QUERY_PATTERN}")],
  MSG: [MessageHandler(Filters.text & ~Filters.command, msg_state)],
}
