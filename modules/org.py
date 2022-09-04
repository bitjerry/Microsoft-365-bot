# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 12:28
@Author: Mr.lin
@Version: v1
@File: org
"""
import telebot.util

from office import App
from res import *
from core import *


@bot.cmd("getorg")
@app_check
def get_org_cmd(msg: Message, app: App):
    org_info = app.Org.get_infos()
    if org_info:
        org_info = [format_html(info) for info in org_info]
        bot.send_msg(msg, "\n============\n".join(org_info))
    else:
        bot.send_msg(msg, Text.org_no)
