import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


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
