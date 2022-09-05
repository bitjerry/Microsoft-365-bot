# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 11:01
@Author: Mr.lin
@Version: v1
@File: sub
"""
from ms import App
from res import *
from core import *


@bot.cmd("getsub")
@app_check
def my_sub_cmd(msg: Message, app: App):
    keyboard = gen_subs_keyboard(app, info_sub)
    if keyboard:
        bot.send_msg(msg, Text.sub_choose, keyboard)
    else:
        bot.send_msg(msg, Text.sub_no)


@bot.callback
@app_check
def info_sub(msg: CallbackQuery, app: App):
    sub_id = callback.text_parse(msg)
    sub_data = app.Sub.get_info(sub_id)
    buttons = [
        [Btn(text="Back To Subs list",
             callback_func=operation_sub)]]
    bot.edit_msg(msg.message,
                 format_html(sub_data),
                 Keyboard(buttons))


@bot.callback
@app_check
def operation_sub(msg: CallbackQuery, app: App):
    bot.edit_msg(msg.message,
                 Text.sub_choose,
                 gen_subs_keyboard(app, info_sub))


def gen_subs_keyboard(app: App, callback_func):
    sub_list: list = app.Sub.get_all()
    if sub_list:
        buttons = [
            [Btn(text=get_pretty_sku_name(sub["skuPartNumber"]),
                 callback_data=sub["id"],
                 callback_func=callback_func)]
            for sub in sub_list]
        return Keyboard(buttons)
    else:
        return None
