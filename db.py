import ssl

import pymongo
import logging
from datetime import datetime

import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

client = pymongo.MongoClient(
    "mongodb+srv://aadereiko:90a12345@cluster0.r2ych.mongodb.net/fvm?retryWrites=true&w=majority",
    ssl_cert_reqs=ssl.CERT_NONE)
db = client.users_fvm


def write_user_to_db(user):
    # check all fields

    try:
        db.users.insert_one({
            "name": user["name"],
            "phone": user["phone"],
            "age": user["age"],
            "transport": user["transport"],
            "has_participated": user["has_participated"],
            "way": user["way"],
            "occupation": user["occupation"],
            "how_met": user["how_met"],
            "is_paper": user["is_paper"],
            # "town": user["town"],
            "user_id": user["user_id"],
            "username": user["username"],
            "tg_name": user["tg_name"],
            "lead_id": settings.ader_id,
            "reg_time": datetime.now(),
        })
    except Exception as e:
        logging.error(e)
        return False
    return True


def get_all_users():
    try:
        users = db.users.find({})
        return users
    except Exception as e:
        logging.error(e)
        return False


def get_users(filters):
    try:
        users = db.users.find(filters if filters else {})
        return users
    except Exception as e:
        logging.error(e)
        return []


def get_user(filters):
    try:
        print(filters)
        user = db.users.find_one(filters if filters else {})
        return user
    except Exception as e:
        logging.error(e)
        return {}
