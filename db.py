import ssl

import pymongo
import logging

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
            "is_online": user["is_online"],
            "phone": user["phone"],
            "age": user["age"],
            "transport": user["transport"],
            "has_participated": user["has_participated"],
            "way": user["way"],
            "occupation": user["occupation"],
            "how_met": user["how_met"],
            "is_paper": user["is_paper"],
            "town": user["town"],
            "user_id": user["user_id"],
            "username": user["username"],
            "tg_name": user["tg_name"]
        })
    except Exception as e:
        logging.error(e)
        return False
    return True
