# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:59
@Author: Mr.lin
@Version: v1
@File: app
"""
import telebot

from core import *
from lang import Text


class AppSession:

    def __init__(self):
        self.__app_id: int = -1

    @property
    def app_id(self):
        return self.__app_id

    @app_id.setter
    def app_id(self, value):
        session_util.reset()
        self.__app_id = value


session: AppSession = session_util.register(AppSession)


@bot.cmd("token")
def token_app_cmd(msg: Message):
    token = app_pool.show_key()
    if token:
        text = f"<pre>{token}</pre>"
        Text.key_op = Text.key_op[-1:]
    else:
        text = Text.key_empty
    keyboard = Keyboard([
        [Btn(text=key_op,
             callback_data=key_op,
             callback_func=operation_app)
         for key_op in Text.key_op]])
    bot.send_msg(msg, text, keyboard)


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
    app_pool.remove()
    bot.send_msg(msg, Text.app_clear_s)


@bot.callback(check_msg=False)
def info_app(msg: CallbackQuery):
    session.app_id = int(callback.text_parse(msg))
    app_data = app_pool.get_data(session.app_id)
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
                 Format(app_data),
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
        case "Unlock":
            unlock(msg.message)
        case "New":
            new_token(msg.message)


@bot.lock
def new_token(msg: Message):
    bot.edit_msg(msg,
                 f"<pre>{app_pool.new_key()}</pre>",
                 msg.reply_markup)


def unlock(msg: Message):
    bot.send_msg(msg, Text.key_input)
    bot.register_next_step(msg, read_token)


def read_token(msg: Message):
    app_pool.unlock(msg.text)
    Text.key_op.pop(0)
    bot.send_msg(msg, Text.db_unlock_s)


def delete_app(msg: Message):
    app_pool.remove(session.app_id)
    session.app_id = -1
    bot.edit_msg(msg, Text.app_del_s)


def rename_app(msg: Message):
    app_pool.rename(session.app_id, msg.text)
    bot.send_msg(msg, Text.app_rename_s)


def edit_app(msg: Message):
    app_data = msg.text.split('\n')
    if len(app_data) == 3:
        app_pool.edit_info(session.app_id, app_data)
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
        app_pool.add(*app_data)
        bot.send_msg(msg, Text.app_add_s)
    else:
        raise ModuleError(Text.app_info_f)


def gen_apps_keyboard(callback_func):
    app_data = app_pool.get_names()
    if app_data:
        buttons = [
            [Btn(text=app_name,
                 callback_data=str(app_id),
                 callback_func=callback_func)]
            for app_id, app_name in app_data]
        return Keyboard(buttons)
    else:
        return None
