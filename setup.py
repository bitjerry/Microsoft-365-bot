# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/7/31 15:21
@Author: Mr.lin
@File: setup
"""
import config
import logging
import traceback
from urllib.parse import urlparse
from flask import Flask, request

__author__ = "Mr.lin"
__status__ = "production"
__version__ = "1.4"

logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='bot.log',
    filemode='a',
    encoding='utf-8'
)

# noinspection PyBroadException
try:
    from core import bot
    from service import *

except Exception:
    traceback.print_exc()

if not (update_url := urlparse(config.WEBHOOK_URL).path):
    update_url = '/'

app = Flask(__name__)


@app.get(config.WELCOME_URL)
def start():
    return '!', 200


@app.post(update_url)
def get_message():
    request_body_dict = request.get_data().decode('utf-8')
    bot.update_message(request_body_dict)
    return '', 200


if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        if config.WEBHOOK_URL and config.WEBHOOK_URL.startswith("https://"):
            bot.webhook(config.WEBHOOK_URL)
            app.run(host="0.0.0.0", port=int(config.PORT))
        else:
            bot.polling(non_stop=True)
    except Exception:
        traceback.print_exc()
