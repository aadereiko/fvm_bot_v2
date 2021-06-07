import logging
from telegram import InlineKeyboardButton
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_fields_from_dict(some_dict, fields):
    result = ""
    for field in fields:
        result += f'{some_dict[field] if some_dict[field] else "-"} '
    return result


def format_users_list(users, fields):
    result = ""
    i = 0

    try:
        for user in users:
            i += 1
            result += f'{i}. '
            for field in fields:
                result += f'{user[field] if user[field] else "-"} '
            result += "\n"
        return result
    except Exception as e:
        logging.error(e)

    return ""


def generate_inline_keyboard_from_users(users, label_fields, callback_data_start):
    keyboard = []
    for user in users:
        label = get_fields_from_dict(user, label_fields)

        keyboard.append([
            InlineKeyboardButton(label, callback_data=f"{callback_data_start} {user['user_id']}")
        ])

    return keyboard
