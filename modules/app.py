# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:59
@Author: Mr.lin
@Version: v1
@File: app
"""
from ms import App
from res import *
from core import *


@bot.cmd("myapp")
def my_app_cmd(msg: Message):
    apps_keyboard = gen_apps_keyboard(info_app)
    if apps_keyboard:
        bot.send_msg(msg, Text.app_choose, apps_keyboard)
    else:
        bot.send_msg(msg, Text.app_no)


@bot.cmd("newapp")
def add_app_cmd(msg: Message):
    bot.send_msg(msg, Text.app_add)
    bot.register_next_step(msg, add_app)


@bot.callback(check_msg=False)
def info_app(msg: CallbackQuery):
    session.app_id = int(callback.text_parse(msg))
    app_data = app_pool.get_app_data(session.app_id)
    keyboard_data = ["Delete App",
                     "Edit Auth Info",
                     "Rename App",
                     "Back To Apps list"]
    buttons = [
        [Btn(text=data,
             callback_data=data,
             callback_func=operation_app)
         for data in keyboard_data[i:i + 2]]
        for i in range(0, len(keyboard_data), 2)]
    bot.edit_msg(msg.message,
                 format_html(app_data),
                 Keyboard(buttons))


@bot.callback(check_msg=False)
def operation_app(msg: CallbackQuery):
    match callback.text_parse(msg):
        case "Delete App":
            delete_app(msg.message)
        case "Edit Auth Info":
            bot.send_msg(msg.message, Text.app_edit)
            bot.register_next_step(msg.message, edit_app)
        case "Rename App":
            bot.send_msg(msg.message, Text.app_rename)
            bot.register_next_step(msg.message, rename_app)
        case "Back To Apps list":
            back_to_apps(msg.message)


def delete_app(msg: Message):
    app_pool.remove_app(session.app_id)
    session.app_id = None
    bot.edit_msg(msg, Text.app_del_s)


def rename_app(msg: Message):
    app_pool.rename_app(session.app_id, msg.text)
    bot.send_msg(msg, Text.app_rename_s)


def edit_app(msg: Message):
    app_data = msg.text.split('\n')
    if len(app_data) == 3:
        app_pool.edit_app_infos(session.app_id, app_data)
        bot.send_msg(msg, Text.app_edit_s)
    else:
        raise ModuleError(Text.app_info_f)


def back_to_apps(msg: Message):
    bot.edit_msg(msg,
                 Text.app_choose,
                 gen_apps_keyboard(info_app))


def add_app(msg: Message):
    app_data = msg.text.split('\n')
    if len(app_data) == 4:
        app_pool.add_app(app_data)
        bot.send_msg(msg, Text.app_add_s)
    else:
        raise ModuleError(Text.app_info_f)


def gen_apps_keyboard(callback_func):
    app_names = app_pool.get_apps_name()
    if app_names:
        buttons = [
            [Btn(text=app_name,
                 callback_data=str(app_id),
                 callback_func=callback_func)]
            for app_id, app_name in enumerate(app_names)]
        return Keyboard(buttons)
    else:
        return None
