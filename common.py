import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def format_user_name_reg_time(users):
    result = ""
    i = 0

    fields = ["name", "username", "reg_time"]
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
