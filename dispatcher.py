import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import ValidationError

from config import TOKEN, MODE

if MODE == 'prod':
    logging.basicConfig(level=logging.INFO)
elif MODE == 'dev':
    logging.basicConfig(level=logging.DEBUG)
else:
    print("Configure MODE in config.py!")
    sys.exit(1)
try:
    bot = Bot(token = TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())
except (ValidationError):
    print("Configure TOKEN in config.py!")
    sys.exit(1)

