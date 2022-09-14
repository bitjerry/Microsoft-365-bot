# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/13 20:43
@Author: Mr.lin
@Version: v1
@File: token
"""
from core import *
from db import *
from lang import Text


@bot.cmd("token")
def token_app_cmd(msg: Message):
    global exist_data
    if exist_data:
        if crypt.key:
            bot.send_msg(msg, Text.key_hidden.format(crypt.key), keyboard_op)
        else:
            bot.send_msg(msg, Text.key_decrypt, keyboard_ops)
    else:
        exist_data = True
        new_msg = bot.send_msg(msg, Text.key.format(crypt.new()), keyboard_op)
        hidden_token(new_msg)


@bot.delay(10.0)
def hidden_token(msg: Message):
    bot.edit_msg(msg, Text.key_hidden.format(crypt.key), keyboard_op)


@bot.lock
@bot.callback
def new_token(msg: CallbackQuery):
    if crypt.key:
        apps = get_all_apps()
        token = crypt.new()
        clear_all_apps()
        add_apps(apps)
    else:
        token = crypt.new()
        clear_all_apps()
    new_msg = bot.edit_msg(msg.message, Text.key.format(token), keyboard_op)
    hidden_token(new_msg)


@bot.callback
def unlock(msg: CallbackQuery):
    bot.send_msg(msg.message, Text.key_input)
    bot.register_next_step(msg, read_token)


def read_token(msg: Message):
    crypt.key = msg.text
    try_decode()
    bot.send_msg(msg, Text.db_unlock_s)


exist_data = bool(check_empty())

keyboard_op = Keyboard([[
    Btn(text=Text.key_op,
        callback_func=new_token)]])
keyboard_ops = Keyboard([[
    Btn(text=Text.key_ops[0],
        callback_func=unlock),
    Btn(text=Text.key_ops[1],
        callback_func=new_token)]])
