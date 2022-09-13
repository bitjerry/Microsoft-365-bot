# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 11:01
@Author: Mr.lin
@Version: v1
@File: sub
"""
from core import *
from lang import Text
from .res import get_pretty_sku_name


@bot.cmd("getsub")
def my_sub_cmd(msg: Message):
    app = app_pool.get(session.get("app_id"))
    if app:
        keyboard = gen_subs_keyboard(app, info_sub)
        if keyboard:
            bot.send_msg(msg, Text.sub_choose, keyboard)
        else:
            bot.send_msg(msg, Text.sub_no)
    else:
        bot.send_msg(msg, Text.app_no)


@bot.callback
def info_sub(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        sub_id = callback.text_parse(msg)
        sub_data = app.Sub.get_info(sub_id)
        buttons = [
            [Btn(text="Back To Subs list",
                 callback_func=operation_sub)]]
        bot.edit_msg(msg.message,
                     Format(sub_data),
                     Keyboard(buttons))
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback
def operation_sub(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        bot.edit_msg(msg.message,
                     Text.sub_choose,
                     gen_subs_keyboard(app, info_sub))
    else:
        bot.edit_msg(msg.message, Text.app_no)


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
