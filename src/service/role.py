# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 12:28
@Author: Mr.lin
@Version: v1
@File: role
"""
from core import *
from resource import Text
from util.helper import *


class RoleSession:

    def __init__(self):
        self.role_id: str = ""


session = RoleSession()
session_util.register(session)
control_keyboard = gen_control_keyboard(Text.role_control)


@bot.cmd("getrole")
@app_autowired
def get_cmd(msg: Message, app: App):
    if keyboard := gen_roles_keyboard(app):
        bot.send_msg(msg, Text.role_select, keyboard)
    else:
        bot.send_msg(msg, Text.role_no)


@bot.callback
@app_autowired
def show_info(msg: CallbackQuery, app: App):
    bot.expire_mod_msg()
    session.role_id = msg.data
    role_data = app.Role.get_info(session.role_id)
    bot.edit_msg(msg.message, Format(role_data), control_keyboard)


@bot.callback("get_member")
@app_autowired
def get_member(msg: CallbackQuery, app: App):
    members = app.Role.get_member(session.role_id)
    text = '\n'.join([member['userPrincipalName'] for member in members])
    if not text:
        return bot.send_msg(msg.message, Text.role_no_user)
    buttons = [[Btn(text=Text.role_back_btn,
                    callback_data=session.role_id,
                    callback_func=show_info)]]
    bot.edit_msg(msg.message, text, Keyboard(buttons))


@bot.callback("back_to_roles_list")
@app_autowired
def back_to_roles(msg: CallbackQuery, app: App):
    if keyboard := gen_roles_keyboard(app):
        bot.edit_msg(msg.message, Text.role_select, keyboard)
    else:
        bot.edit_msg(msg.message, Text.role_no)


def gen_roles_keyboard(app: App):
    if not (role_list := app.Role.get_all()):
        return None
    buttons = [
        [Btn(text=role["displayName"],
             callback_data=role['id'],
             callback_func=show_info)]
        for role in role_list]
    return Keyboard(buttons)
