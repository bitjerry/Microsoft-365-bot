# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/7/31 15:21
@Author: Mr.lin
@File: setup
"""
import os
import config
import logging
import traceback
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
    from core import *
    from modules import *

except Exception:
    traceback.print_exc()

app = Flask(__name__)


@app.get(config.WEBHOOK_URL)
def start():
    return '!', 200


@app.get(config.SET_WEBHOOK_URL)
def set_webhook():
    url = "https://" + request.host + config.WEBHOOK_URL
    return str(bot.set_webhook(url)), 200


@app.get(config.STOP_WEBHOOK_URL)
def stop_webhook():
    return str(bot.remove_webhook()), 200


@app.post(config.WEBHOOK_URL)
def get_message():
    request_body_dict = request.get_data().decode('utf-8')
    bot.update_message(request_body_dict)
    return '', 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(config.PORT))
    # bot.polling()
