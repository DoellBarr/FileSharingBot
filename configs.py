import re
import logging
from typing import Dict
from dotenv import load_dotenv
from os import environ
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
fsubs_dict: Dict[str, int] = {}
btn_re = re.compile(r"(GROUP|CHANNEL)_(\d)")
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
markup = InlineKeyboardMarkup
btn = InlineKeyboardButton


def logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


class Config:
    api_id = environ.get('API_ID')
    api_hash = environ.get('API_HASH')
    bot_token = environ.get('BOT_TOKEN')
    owner = int(environ.get('OWNER'))
    if admins := environ.get("ADMINS", []):
        admins = list(map(int, environ.get('ADMINS').split(' ')))
    for key, val in environ.items():
        if match := btn_re.search(key):
            name = f"{match[1]}_{match[2]}"
            print(f"Menemukan tombol, {name}, Chat Id: {val}")
            fsubs_dict[name] = int(val)
    if logger_group := environ.get("LOGGER_GROUP_ID", None):
        logger_group_id = int(logger_group)
    else:
        logger_group_id = None
    db_channel = environ.get("DB_CHANNEL")
    start_msg = environ.get("START_MSG")
    fsub_msg = environ.get("FSUB_MSG")


config = Config()
