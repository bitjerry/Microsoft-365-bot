# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/7/31 15:21
@Author: Mr.lin
@Version: v1
@File: setup
"""
import os
import config
from core import *
from modules import *
from flask import Flask, request

app = Flask(__name__)


@app.get('/')
def start():
    return '!', 200


@app.get("/set_webhook")
def set_webhook():
    url = "https://" + request.host
    return str(bot.set_webhook(url)), 200


@app.get("/stop_webhook")
def stop_webhook():
    return str(bot.remove_webhook()), 200


@app.post('/')
def get_message():
    request_body_dict = request.get_data().decode('utf-8')
    bot.get_message_call_back(request_body_dict)
    return '', 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(config.PORT))
