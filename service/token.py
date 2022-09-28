# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/13 20:43
@Author: Mr.lin
@Version: v1
@File: token
"""
from db import *
from core import *
from util.helper import *
from resource import Text

keyboard_op = gen_control_keyboard(Text.key_op)
keyboard_ops = gen_control_keyboard(Text.key_ops)


@bot.on_startup
def init():
    if is_empty():
        hidden(bot.send_message(bot.ADMIN_ID, Text.key.format(crypt.new()), reply_markup=keyboard_op))
    else:
        bot.send_message(bot.ADMIN_ID, Text.key_decrypt, reply_markup=keyboard_ops)


@bot.cmd("token")
def show_token_cmd(msg: Message):
    if crypt.key:
        bot.send_msg(msg, Text.key_hidden.format(crypt.key), keyboard_op)
    else:
        bot.send_msg(msg, Text.key_decrypt, keyboard_ops)


@bot.callback(check=False)
def control(msg: CallbackQuery):
    match int(msg.data):
        case 0:
            bot.send_msg(msg.message, Text.key_input)
            bot.register_next_step(unlock, msg.message)
        case 1:
            new(msg.message)


@task.delay(300)
def hidden(msg: Message):
    bot.edit_msg(msg, Text.key_hidden.format(crypt.key), keyboard_op)


@lock
def new(msg: Message):
    if crypt.key:
        apps = get_all_apps()
        token = crypt.new()
        clear_all_apps()
        add_apps(apps)
    else:
        token = crypt.new()
        clear_all_apps()
    hidden(bot.edit_msg(msg, Text.key.format(token), keyboard_op))


def unlock(msg: Message, old_mag: Message):
    crypt.key = msg.text
    try_decode()
    bot.send_msg(msg, Text.key_unlock_s)
    bot.edit_msg(old_mag, Text.key_hidden.format(crypt.key), keyboard_op)
