from telegram import Update
from telegram.ext import (
    CallbackContext,
)

import common
import db


def users_cmd(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    users = db.get_all_users()
    msg = common.format_users_list(users, ["name", "username", "reg_time"])

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )
