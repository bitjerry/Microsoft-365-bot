# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:59
@Author: Mr.lin
@Version: v1
@File: app
"""

from core import *
from lang import Text


class AppSession:

    def __init__(self):
        self.__app_id: str = ""

    @property
    def app_id(self):
        return self.__app_id

    @app_id.setter
    def app_id(self, value):
        session_util.reset()
        self.__app_id = value


session: AppSession = session_util.register(AppSession)


@bot.cmd("myapp")
def my_app_cmd(msg: Message):
    keyboard = gen_apps_keyboard(info_app)
    if keyboard:
        bot.send_msg(msg, Text.app_choose, keyboard)
    else:
        bot.send_msg(msg, Text.app_no)


@bot.cmd("newapp")
def add_app_cmd(msg: Message):
    bot.send_msg(msg, Text.app_add)
    bot.register_next_step(msg, add_app)


@bot.cmd("clearapp")
def clear_app_cmd(msg: Message):
    app_pool.clear()
    bot.send_msg(msg, Text.app_clear_s)


@bot.callback(check=False)
def info_app(msg: CallbackQuery):
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
    session.app_id = callback.text_parse(msg)
    app = app_pool.get(session.app_id)
    bot.edit_msg(msg.message,
                 Format(app.get_data()),
                 Keyboard(buttons))


@bot.callback(check=False)
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
    app_pool.remove(session.app_id)
    session.app_id = ""
    bot.edit_msg(msg, Text.app_del_s)


def rename_app(msg: Message):
    app_pool.get(session.app_id).name = msg.text
    bot.send_msg(msg, Text.app_rename_s)


def edit_app(msg: Message):
    app_data = msg.text.split('\n')
    if len(app_data) == 3:
        app_pool.get(session.app_id).edit_info(*app_data)
        bot.send_msg(msg, Text.app_edit_s)
    else:
        bot.send_msg(msg, Text.app_info_f)
        bot.register_next_step(msg, edit_app)


def back_to_apps(msg: Message):
    bot.edit_msg(msg,
                 Text.app_choose,
                 gen_apps_keyboard(info_app))


def add_app(msg: Message):
    app_data = msg.text.split('\n')
    if len(app_data) == 4:
        app_pool.add(*app_data)
        bot.send_msg(msg, Text.app_add_s)
    else:
        bot.send_msg(msg, Text.app_info_f)
        bot.register_next_step(msg, add_app)


def gen_apps_keyboard(callback_func):
    if app_data := app_pool.get_names():
        buttons = [
            [Btn(text=app_name,
                 callback_data=app_id,
                 callback_func=callback_func)]
            for app_id, app_name in app_data]
        return Keyboard(buttons)
    else:
        return None
