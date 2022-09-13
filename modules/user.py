# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:48
@Author: Mr.lin
@Version: v1
@File: user
"""
from core import *
from lang import Text
from .res import get_pretty_sku_name


class UserSession:

    def __init__(self):
        self.__user_id: str = ""
        self.user_links: list = [None]
        self.user_keyboard = None
        self.user_search: str = ""
        self.skus: dict = {}
        self.skus_del: dict = {}

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        bot.clear_msg()
        self.__user_id = value


session: UserSession = session_util.register(UserSession)


@bot.cmd("getuser")
def get_users_cmd(msg: Message):
    app = app_pool.get(session.get("app_id"))
    if app:
        session.user_keyboard = user_op_keyboard_back
        keyboard = gen_users_keyboard(app, info_user, 0)
        if keyboard:
            bot.send_msg(msg, Text.user_choose, keyboard)
        else:
            bot.send_msg(msg, Text.user_no)
    else:
        bot.send_msg(msg, Text.app_no)


@bot.cmd("getuserbyname")
def get_user_by_name_cmd(msg: Message):
    app = app_pool.get(session.get("app_id"))
    if app:
        session.user_keyboard = user_op_keyboard
        bot.send_msg(msg, Text.user_by_name)
        bot.register_next_step(msg, info_user_by_name, app)
    else:
        bot.send_msg(msg, Text.app_no)


@bot.cmd("searchuser")
def search_user_cmd(msg: Message):
    app = app_pool.get(session.get("app_id"))
    if app:
        session.user_keyboard = user_op_keyboard_back
        bot.send_msg(msg, Text.user_search)
        bot.register_next_step(msg, search_user_list, app)
    else:
        bot.send_msg(msg, Text.app_no)


@bot.cmd("adduser")
def add_user_cmd(msg: Message):
    app = app_pool.get(session.get("app_id"))
    if app:
        session.user_keyboard = user_op_keyboard
        bot.send_msg(msg, Text.user_data)
        bot.register_next_step(msg, info_user_added, app)
    else:
        bot.send_msg(msg, Text.app_no)


@bot.callback
def info_user(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        session.__user_id = callback.text_parse(msg)
        user_data = app.User.get_infos(session.__user_id)
        bot.edit_msg(msg.message,
                     Format(user_data),
                     session.user_keyboard)
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback
def license_for_user(msg: CallbackQuery):
    skus = session.skus
    callback_data = callback.text_parse(msg)
    license_buffer(callback_data[0], callback_data[1], skus)
    bot.edit_msg(msg.message,
                 '\n'.join(skus.values()),
                 msg.message.reply_markup)


@bot.callback
def user_license(msg: CallbackQuery):
    skus_del = session.skus_del
    callback_data = callback.text_parse(msg)
    license_buffer(callback_data[0], callback_data[1], skus_del)
    bot.edit_msg(msg.message,
                 '\n'.join(skus_del.values()),
                 msg.message.reply_markup)


@bot.callback
def assign_role(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        role_id = callback.text_parse(msg)
        app.Role.add_member(role_id, session.__user_id)
        bot.send_msg(msg.message, Text.user_role_assign_s)
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback
def revoke_role(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        role_id = callback.text_parse(msg)
        app.Role.del_member(role_id, session.__user_id)
        bot.send_msg(msg.message, Text.user_role_del_s)
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback
def assign_license(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        app.User.add_license(
            session.__user_id,
            session.skus.keys())
        session.skus.clear()
        bot.send_msg(msg.message, Text.user_assign_lic_s)
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback
def delete_license(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        app.User.delete_license(
            session.__user_id,
            session.skus_del.keys()
        )
        session.skus_del.clear()
        bot.send_msg(msg.message, Text.user_delete_lic_s)
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback
def get_next_users(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        page_index = int(callback.text_parse(msg))
        keyboard = gen_users_keyboard(app, info_user, page_index)
        if keyboard:
            bot.edit_msg(msg.message, Text.user_choose, keyboard)
        else:
            bot.edit_msg(msg.message, Text.user_no)
    else:
        bot.edit_msg(msg.message, Text.app_no)


@bot.callback
def operation_user(msg: CallbackQuery):
    app = app_pool.get(session.get("app_id"))
    if app:
        match callback.text_parse(msg):
            case "Assign license":
                list_licenses_for_user(msg.message, app)
            case "My license":
                list_user_licenses(msg.message, app)
            case "Assign role":
                list_roles_for_user(msg.message, app)
            case "My role":
                list_user_roles(msg.message, app)
            case "Delete user":
                delete_user(msg.message, app)
            case "Update user info":
                bot.send_msg(msg.message, Text.user_update)
                bot.register_next_step(msg.message, update_user, app)
            case "Refresh":
                refresh_data(msg.message, app)
            case "Back to user list":
                back_to_users(msg.message, app)
    else:
        bot.edit_msg(msg.message, Text.app_no)


def search_user_list(msg: Message, app: App):
    session.user_search = msg.text
    keyboard = gen_users_keyboard(app, info_user, 0, msg.text)
    if keyboard:
        bot.send_msg(msg, Text.user_choose, keyboard)
    else:
        bot.send_msg(msg, Text.user_no)


def info_user_by_name(msg: Message, app: App):
    user_data, session.__user_id = app.User.get_infos_by_name(msg.text)
    bot.send_msg(msg,
                 Format(user_data),
                 user_op_keyboard)


def info_user_added(msg: Message, app: App):
    input_data = msg.text.split('\n')
    user_data, session.__user_id = app.User.create(*input_data)
    bot.send_msg(msg,
                 Text.user_create_s + Format(user_data),
                 user_op_keyboard)


def list_roles_for_user(msg: Message, app: App):
    role_list: list = app.Role.get_all()
    control_buttons = [Btn(
        text="⏪ Back To User",
        callback_data=session.__user_id,
        callback_func=info_user)]
    if role_list:
        buttons = [
            [Btn(text=role["displayName"],
                 callback_data=role['id'],
                 callback_func=assign_role)]
            for role in role_list]
        buttons.append(control_buttons)
        bot.edit_msg(msg, Text.user_role_assign, Keyboard(buttons))
    else:
        bot.edit_msg(msg, Text.user_role_no, Keyboard([control_buttons]))


def list_user_roles(msg: Message, app: App):
    role_list: list = app.User.get_role(session.__user_id)
    control_buttons = [
        Btn(text="⏪ Back To User",
            callback_data=session.__user_id,
            callback_func=info_user)]
    if role_list:
        buttons = [
            [Btn(text=role["displayName"],
                 callback_data=role["roleTemplateId"],
                 callback_func=revoke_role)]
            for role in role_list]
        buttons.append(control_buttons)
        bot.edit_msg(msg, Text.user_role_del, Keyboard(buttons))
    else:
        bot.edit_msg(msg, Text.user_role_no, Keyboard([control_buttons]))


def license_buffer(sku_name: str, sku_id: str, container: dict):
    if container.__contains__(sku_id):
        container.pop(sku_id)
    else:
        container[sku_id] = sku_name


def licenses_user(callback_func, sub_list: list):
    buttons = []
    for sub in sub_list:
        pretty_sku_name = get_pretty_sku_name(sub["skuPartNumber"])
        buttons.append(
            [Btn(text=pretty_sku_name,
                 callback_data=callback.text_gen(pretty_sku_name, sub['skuId']),
                 callback_func=callback_func)])
    return buttons


def list_licenses_for_user(msg: Message, app: App):
    sub_list: list = app.Sub.get_all()
    control_buttons = [
        Btn(text="Assign License",
            callback_func=assign_license),
        Btn(text="Back To User",
            callback_data=session.__user_id,
            callback_func=info_user)]
    if sub_list:
        buttons = licenses_user(license_for_user, sub_list)
        buttons.append(control_buttons)
        bot.edit_msg(msg, Text.user_lic_assign, Keyboard(buttons))
    else:
        bot.edit_msg(msg, Text.user_lic_no, Keyboard([control_buttons]))


def list_user_licenses(msg: Message, app: App):
    sub_list: list = app.User.get_license(session.__user_id)
    control_buttons = [
        Btn(text="Delete License",
            callback_func=delete_license),
        Btn(text="Back To User",
            callback_data=session.__user_id,
            callback_func=info_user)]
    if sub_list:
        buttons = licenses_user(user_license, sub_list)
        buttons.append(control_buttons)
        bot.edit_msg(msg, Text.user_lic_del, Keyboard(buttons))
    else:
        bot.edit_msg(msg, Text.user_lic_no, Keyboard([control_buttons]))


def delete_user(msg: Message, app: App):
    app.User.delete(session.__user_id)
    bot.send_msg(msg, Text.user_delete_s)


def update_user(msg: Message, app: App):
    input_data = msg.text.split('\n')
    app.User.update_infos(session.__user_id, *input_data)
    bot.send_msg(msg, Text.user_update_s)


def refresh_data(msg: Message, app: App):
    user_data = app.User.get_infos(session.__user_id)
    bot.edit_msg(msg,
                 Format(user_data),
                 msg.reply_markup)


def back_to_users(msg: Message, app: App):
    session.user_links = [None]
    keyboard = gen_users_keyboard(app, info_user, 0, session.user_search)
    bot.edit_msg(msg, Text.user_choose, keyboard)


def gen_users_keyboard(app: App,
                       callback_func,
                       page_index: int,
                       search: str = None):
    user_list, next_link = app.User.get_all(session.user_links[page_index], search)
    if user_list:
        buttons = [
            [Btn(text=user["userPrincipalName"],
                 callback_data=user['id'],
                 callback_func=callback_func)]
            for user in user_list]
        btn_page_switch = []
        if page_index > 0:
            btn_page_switch.append(
                Btn(text="⏫ page up",
                    callback_data=str(page_index - 1),
                    callback_func=get_next_users))
        if next_link:
            session.user_links.append(next_link)
            btn_page_switch.append(
                Btn(text="page down ⏬",
                    callback_data=str(page_index + 1),
                    callback_func=get_next_users))
        if btn_page_switch:
            buttons.append(btn_page_switch)
        return Keyboard(buttons)
    else:
        return None


keyboard_data = ["Assign license",
                 "My license",
                 "Assign role",
                 "My role",
                 "Delete user",
                 "Update user info",
                 "Refresh",
                 "Back to user list"]


def gen_user_op_keyboard():
    buttons = [
        [Btn(text=data,
             callback_data=data,
             callback_func=operation_user)
         for data in keyboard_data[i:i + 2]]
        for i in range(0, len(keyboard_data), 2)]
    return Keyboard(buttons)


user_op_keyboard_back = gen_user_op_keyboard()
keyboard_data.pop()
user_op_keyboard = gen_user_op_keyboard()
