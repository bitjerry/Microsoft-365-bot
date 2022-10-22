# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/13 20:43
@Author: Mr.lin
@Version: v1
@File: key
"""
import config
from db import *
from core import *
from util.helper import *
from resource import Text

keyboard_op = gen_control_keyboard(Text.key_op)
keyboard_ops = gen_control_keyboard(Text.key_ops)


@bot.on_startup
def init():
    if is_empty():
        hidden(
            bot.send_message(
                bot.ADMIN_ID,
                Text.key.format(config.EXPIRE_KEY, crypt.new()),
                reply_markup=keyboard_op)
        )
    else:
        bot.send_message(bot.ADMIN_ID, Text.key_decrypt, reply_markup=keyboard_ops)


@bot.cmd("key")
def show_key_cmd(msg: Message):
    if crypt.key:
        bot.send_msg(msg, Text.key_hidden.format(crypt.key), keyboard_op)
    else:
        bot.send_msg(msg, Text.key_decrypt, keyboard_ops)


@bot.callback("unlock", False)
def read_key(msg: CallbackQuery):
    bot.send_msg(msg.message, Text.key_input)
    bot.register_next_step(unlock, msg.message)


@bot.callback("new", False)
@lock
def new(msg: CallbackQuery):
    if crypt.key:
        apps = get_all_apps()
        key = crypt.new()
        clear_all_apps()
        add_apps(apps)
    else:
        key = crypt.new()
        clear_all_apps()
    hidden(bot.edit_msg(msg.message, Text.key.format(config.EXPIRE_KEY, key), keyboard_op))


@task.delay(config.EXPIRE_KEY)
def hidden(msg: Message):
    bot.edit_msg(msg, Text.key_hidden.format(crypt.key), keyboard_op)


def unlock(msg: Message, old_mag: Message):
    crypt.key = msg.text
    try_decode()
    bot.send_msg(msg, Text.key_unlock_s)
    bot.edit_msg(old_mag, Text.key_hidden.format(crypt.key), keyboard_op)
