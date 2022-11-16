# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:59
@Author: Mr.lin
@Version: v1
@File: app
"""
import json
import os
import io
from core import *
from resource import Text, res_path
from util.helper import *
from db import add_app, add_apps, list_apps, count, get_all_apps


class AppSession:

    def __init__(self):
        self.__app_id: int = 0
        self.total: int = count()

    @property
    def app_id(self):
        return self.__app_id

    @app_id.setter
    def app_id(self, value: int):
        bot.clear_all_msg()
        session_util.reset()
        self.__app_id = value


session = AppSession()
session_util.register(session)
control_keyboard = gen_control_keyboard(Text.app_control)


@bot.cmd("myapp")
def get_cmd(msg: Message):
    if keyboard := gen_apps_keyboard(0):
        bot.send_msg(msg, Text.app_select, keyboard)
    else:
        bot.send_msg(msg, Text.app_empty)


@bot.cmd("newapp")
def add_cmd(msg: Message):
    bot.send_msg(msg, Text.app_add)
    bot.register_next_step(add)


@bot.cmd("clearapp")
def clear_cmd(msg: Message):
    app_pool.clear()
    session.total = 0
    bot.send_msg(msg, Text.app_clear_s)


@bot.cmd("addapps")
def add_more_cmd(msg: Message):
    with open(os.path.join(res_path, "app_template.json"), 'r', encoding="utf-8") as app_template:
        bot.send_doc(msg, app_template, caption=Text.app_add_more)
    bot.register_next_step(add_more)


@bot.cmd("exportapps")
@lock
def get_all_apps_cmd(msg: Message):
    apps = get_all_apps()
    apps_str = io.StringIO(json.dumps(apps, indent=3))
    bot.send_doc(msg, apps_str, visible_file_name="app_template.json")


@bot.callback(check=False)
def show_info(msg: CallbackQuery):
    session.app_id = int(msg.data)
    app = app_pool.get(session.app_id)
    bot.edit_msg(msg.message, Text.app_data + str(Format(app.get_data())), control_keyboard)


@bot.callback
def get_next_page(msg: CallbackQuery):
    if keyboard := gen_apps_keyboard(int(msg.data)):
        bot.edit_msg(msg.message, Text.app_select, keyboard)
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback("delete")
def delete(msg: CallbackQuery):
    app_pool.remove(session.app_id)
    session.app_id = 0
    session.total -= 1
    bot.send_msg(msg.message, Text.app_del_s)
    back_to_apps(msg)


@bot.callback("edit")
def edit(msg: CallbackQuery):
    bot.send_msg(msg.message, Text.app_edit)
    bot.register_next_step(edit_info)


@bot.callback("rename")
def rename(msg: CallbackQuery):
    bot.send_msg(msg.message, Text.app_rename)
    bot.register_next_step(edit_name)


@bot.callback("back_to_apps_list")
def back_to_apps(msg: CallbackQuery):
    if keyboard := gen_apps_keyboard(0):
        bot.edit_msg(msg.message, Text.app_select, keyboard)
    else:
        bot.edit_msg(msg.message, Text.app_empty)


def edit_name(msg: Message):
    app_pool.get(session.app_id).rename(msg.text)
    bot.send_msg(msg, Text.app_rename_s)


def edit_info(msg: Message):
    app_data = msg.text.split('\n')
    if len(app_data) == 3:
        app_pool.get(session.app_id).edit_info(*app_data)
        bot.send_msg(msg, Text.app_edit_s)
    else:
        bot.send_msg(msg, Text.app_info_f)
        bot.register_next_step(edit_info)


def add(msg: Message):
    app_data = msg.text.split('\n')
    if len(app_data) == 4:
        add_app(*app_data)
        session.total += 1
        bot.send_msg(msg, Text.app_add_s)
    else:
        bot.send_msg(msg, Text.app_info_f)
        bot.register_next_step(add)


def add_more(msg: Message):
    file_info = bot.get_file(msg.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    template = json.loads(downloaded_file)
    add_apps(template)
    session.total += len(template)
    bot.send_msg(msg, Text.app_add_s)


def gen_apps_keyboard(page_index: int):
    page_size = 10
    if not (app_list := list_apps(page_index, page_size)):
        return None
    buttons = [
        [Btn(text=app_name,
             callback_data=app_id,
             callback_func=show_info)]
        for app_id, app_name in app_list]
    btn_page_switch = gen_page_switch(
        page_index=page_index,
        has_next_page=session.total - (page_index + 1) * page_size > 0)
    if btn_page_switch := btn_page_switch:
        buttons.append(btn_page_switch)

    return Keyboard(buttons)
