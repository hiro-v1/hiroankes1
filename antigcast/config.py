
import os
import logging
from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8005136685:AAHkkFMmMIJpN_B-ejg-VUYQhCkRXpFCRvE")
BOT_WORKERS = int(os.environ.get("BOT_WORKERS", "4"))

APP_ID = int(os.environ.get("APP_ID", "25802693"))
API_HASH = os.environ.get("API_HASH", "803393e9f1b6ea523853ce2126208c17")

LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", ""))

MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://kensay:Kentos123$@cluster0.gm457.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "ankeshiro")
BROADCAST_AS_COPY = True

PLUG = dict(root="BocilAnti/plugins")

OWNER_ID = [int(x) for x in (os.environ.get("OWNER_ID", "5634309575").split())]
OWNER_NAME = os.environ.get("OWNER_NAME", "@hiro_v1")


LOG_FILE_NAME = "BocilAnti_logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

CREATOR = [
    5634309575, 
]

OWNER_ID.append(5634309575)
