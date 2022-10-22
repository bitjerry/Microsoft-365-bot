# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 11:01
@Author: Mr.lin
@Version: v1
@File: sub
"""
from core import *
from resource import *
from util.helper import *

control_keyboard = gen_control_keyboard(Text.sub_control)


@bot.cmd("getsub")
@app_autowired
def get_cmd(msg: Message, app: App):
    if keyboard := gen_subs_keyboard(app):
        bot.send_msg(msg, Text.sub_select, keyboard)
    else:
        bot.send_msg(msg, Text.sub_no)


@bot.callback
@app_autowired
def show_info(msg: CallbackQuery, app: App):
    bot.expire_mod_msg()
    sub_data = app.Sub.get_info(msg.data)
    bot.edit_msg(msg.message, Format(sub_data), control_keyboard)


@bot.callback("back_to_subs_list")
@app_autowired
def control(msg: CallbackQuery, app: App):
    if keyboard := gen_subs_keyboard(app):
        bot.edit_msg(msg.message, Text.sub_select, keyboard)
    else:
        bot.edit_msg(msg.message, Text.sub_no)


def gen_subs_keyboard(app: App):
    if not (sub_list := app.Sub.get_all()):
        return None
    buttons = [
        [Btn(text=get_pretty_sku_name(sub["skuPartNumber"]),
             callback_data=sub["id"],
             callback_func=show_info)]
        for sub in sub_list]
    return Keyboard(buttons)
