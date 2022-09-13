# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:47
@Author: Mr.lin
@Version: v1
@File: db.py
"""
import glob
from core import *
from modules.res import *
from os.path import dirname, basename, isfile, join


@bot.cmd("start")
def start(msg: Message):
    bot.send_msg(msg, Text.about)


@bot.cmd("log")
def get_log(msg: Message):
    with open("bot.log") as doc:
        bot.send_document(msg.chat.id, doc)


modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('db.py')]




