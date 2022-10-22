# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:47
@Author: Mr.lin
@Version: v1
@File: __init__
"""
import os
import config
from core import *
from util.helper import task
from resource import Text

__all__ = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and f != '__init__.py']


@bot.cmd("start")
def start(msg: Message):
    bot.send_msg(msg, Text.about)


@bot.cmd("log")
def get_log(msg: Message):
    with open("bot.log", "r", encoding='utf-8') as doc:
        if doc.read(1):
            bot.send_doc(msg, doc)


@bot.on_startup
@task.delay(config.EXPIRE_LOGS, True)
def auto_send_log():
    with open("bot.log", "r+", encoding='utf-8') as doc:
        if doc.read(1):
            bot.send_document(bot.ADMIN_ID, doc)
            doc.seek(0)
            doc.truncate()
