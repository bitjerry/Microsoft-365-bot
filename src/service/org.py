# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 12:28
@Author: Mr.lin
@Version: v1
@File: org
"""
from core import *
from resource import Text
from util.helper import *


@bot.cmd("getorg")
@app_autowired
def get_cmd(msg: Message, app: App):
    if org_info := app.Org.get_infos():
        bot.send_msg(msg, Format(org_info))
    else:
        bot.send_msg(msg, Text.org_no)
