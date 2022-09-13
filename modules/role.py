# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 12:28
@Author: Mr.lin
@Version: v1
@File: role
"""
from core import *
from lang import Text


class RoleSession:

    def __init__(self):
        self.__role_id = None

    @property
    def role_id(self):
        return self.__role_id

    @role_id.setter
    def role_id(self, value):
        bot.clear_msg()
        self.__role_id = value


session: RoleSession = session_util.register(RoleSession)


@bot.cmd("getrole")
def get_role_cmd(msg: Message):
    app = app_pool.get(session.get("app_id"))
    if app:
        bot.send_msg(msg,
                     Text.role_choose,
                     gen_roles_keyboard(app, get_role))
    else:
        bot.send_msg(msg, Text.app_no)


@bot.callback
def get_role(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        session.__role_id = callback.text_parse(msg)
        role_data = app.Role.get_info(session.__role_id)
        buttons = [[Btn(text=text,
                        callback_data=text,
                        callback_func=operation_role)
                    for text in ["Get member", "Back to roles list"]]]
        bot.edit_msg(msg.message,
                     Format(role_data),
                     Keyboard(buttons))
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback
def operation_role(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        match callback.text_parse(msg):
            case "Get member":
                get_member(msg.message, app)
            case "Back to roles list":
                back_to_roles(msg.message, app)
    else:
        bot.edit_msg(msg.message, Text.app_no)


def get_member(msg: Message, app: App):
    members = app.Role.get_member(session.__role_id)
    text = '\n'.join([member['userPrincipalName'] for member in members])
    if text:
        keyboard = Keyboard(
            [[Btn(text="Beck to role",
                  callback_data=session.__role_id,
                  callback_func=get_role)]])
        bot.edit_msg(msg, text, keyboard)
    else:
        bot.send_msg(msg, Text.role_no_user)


def back_to_roles(msg: Message, app: App):
    bot.edit_msg(msg,
                 Text.role_choose,
                 gen_roles_keyboard(app, get_role))


def gen_roles_keyboard(app: App, callback_func):
    role_list: list = app.Role.get_all()
    if role_list:
        buttons = [
            [Btn(text=role["displayName"],
                 callback_data=role['id'],
                 callback_func=callback_func)]
            for role in role_list]
        return Keyboard(buttons)
    else:
        return None
