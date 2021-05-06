# Enable logging
import logging
from telegram.ext import (
    CallbackContext,
)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> int:
    user_id, first_name = update.effective_user.id, update.effective_user.first_name
    logger.info("User %s %s run a start cmd", user_id, first_name)
    reply_keyboard = [['Регистрация']]
    update.message.reply_text(
        'Какой-то там текст',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
