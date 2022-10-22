# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/18 20:39
@Author: Mr.lin
@Version: v1
@File: domain
"""

from core import *
from resource import Text
from util.helper import *


class DomainSession:

    def __init__(self):
        self.__domain_name = ""

    @property
    def domain_name(self):
        return self.__domain_name

    @domain_name.setter
    def domain_name(self, value):
        bot.expire_mod_msg()
        self.__domain_name = value


session = DomainSession()
session_util.register(session)
control_keyboard_verify = gen_control_keyboard(Text.domain_control_verify)
control_keyboard_verify_back = gen_control_keyboard(Text.domain_control_verify_back)
control_keyboard_back = gen_control_keyboard(Text.domain_control_back)
control_keyboard = gen_control_keyboard(Text.domain_control)
control_keyboard_back_only = gen_control_keyboard(Text.domain_control_back_only)


@bot.cmd("listdomain")
@app_autowired
def list_domain_cmd(msg: Message, app: App):
    if keyboard := gen_domain_keyboard(app):
        bot.send_msg(msg, Text.domain_select, keyboard)
    else:
        bot.send_msg(msg, Text.domain_no)


@bot.cmd("adddomain")
@app_autowired
def add_domain_cmd(msg: Message, app: App):
    bot.send_msg(msg, Text.domain_add)
    bot.register_next_step(add, app)


@bot.callback
@app_autowired
def show_info(msg: CallbackQuery, app: App):
    if not (domain_info := app.Domain.get(msg.data)):
        return bot.edit_msg(msg.message, Text.domain_no)
    session.domain_name = domain_info["id"]
    if domain_info["isVerified"]:
        bot.edit_msg(msg.message, Format(domain_info), control_keyboard_back)
    else:
        domain_info = app.Domain.get_dns(session.domain_name)
        bot.edit_msg(msg.message, Text.domain_dns + str(Format(domain_info)), control_keyboard_verify_back)


@bot.callback('delete')
@app_autowired
def delete(msg: CallbackQuery, app: App):
    app.Domain.delete(session.domain_name)
    bot.edit_msg(msg.message, Text.domain_del_s,
                 control_keyboard_back_only)


@bot.callback('verify')
@app_autowired
def verify(msg: CallbackQuery, app: App):
    if not app.Domain.verify(session.domain_name):
        return bot.send_msg(msg.message, Text.domain_verify_f)
    if not (domain_info := app.Domain.get(msg.data)):
        return bot.edit_msg(msg.message, Text.domain_no)
    bot.edit_msg(msg.message, Format(domain_info), control_keyboard_back)


@bot.callback('back')
@app_autowired
def back(msg: CallbackQuery, app: App):
    if keyboard := gen_domain_keyboard(app):
        bot.edit_msg(msg.message, Text.domain_select, keyboard)
    else:
        bot.edit_msg(msg.message, Text.domain_no)


def add(msg: Message, app: App):
    domain_info = app.Domain.add(msg.text)
    session.domain_name = msg.text
    if domain_info["isVerified"]:
        bot.send_msg(msg, Format(domain_info), control_keyboard)
    else:
        domain_info = app.Domain.get_dns(msg.text)
        bot.send_msg(msg, Text.domain_dns + str(Format(domain_info)),
                     control_keyboard_verify)


def gen_domain_keyboard(app: App):
    if not (domain_list := app.Domain.list()):
        return None
    keyboard = [[Btn(text=domain["id"],
                     callback_data=domain["id"],
                     callback_func=show_info)]
                for domain in domain_list]
    return Keyboard(keyboard)
