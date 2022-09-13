# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 12:28
@Author: Mr.lin
@Version: v1
@File: org
"""
from core import *
from lang import Text


@bot.cmd("getorg")
def get_org_cmd(msg: Message):
    app = app_pool.get(session.get("app_id"))
    if app:
        if org_info:
            bot.send_msg(msg, Format(app.Org.get_infos()))
        else:
            bot.send_msg(msg, Text.org_no)
    else:
        bot.send_msg(msg, Text.app_no)
