# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:48
@Author: Mr.lin
@Version: v1
@File: user
"""
import re
import secrets
from core import *
from resource import *
from util.helper import *


class UserSession:

    def __init__(self):
        self.__user_id: str = ""
        self.username: list = []
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
        bot.expire_mod_msg()
        self.__user_id = value


session = UserSession()
session_util.register(session)
control_keyboard_back = gen_control_keyboard(Text.user_control_back)
control_keyboard = gen_control_keyboard(Text.user_control)
control_keyboard_back_only = gen_control_keyboard(Text.user_control_back_only)

@bot.cmd("getuser")
@app_injector
def get_cmd(msg: Message, app: App):
    session.user_keyboard = control_keyboard_back
    session.user_search = None
    if keyboard := gen_users_keyboard(app, 0):
        bot.send_msg(msg, Text.user_select, keyboard)
    else:
        bot.send_msg(msg, Text.user_no)


@bot.cmd("getuserbyname")
@app_injector
def get_by_name_cmd(msg: Message, app: App):
    session.user_keyboard = control_keyboard
    bot.send_msg(msg, Text.user_by_name)
    bot.register_next_step(show_info_by_name, app)


@bot.cmd("searchuser")
@app_injector
def search_cmd(msg: Message, app: App):
    session.user_keyboard = control_keyboard_back
    bot.send_msg(msg, Text.user_search)
    bot.register_next_step(list_by_search, app)


@bot.cmd("adduser")
@app_injector
def add_cmd(msg: Message, app: App):
    if not (keyboard := gen_username_suffix(app)):
        return bot.send_msg(msg, Text.domain_no)
    session.user_keyboard = control_keyboard
    bot.send_msg(msg, Text.user_name_suffix_select, keyboard)


@bot.callback
@app_injector
def show_info(msg: CallbackQuery, app: App):
    (username, session.user_id) = msg.data
    username = re.search("(.*)@(.*)", username)
    session.username = [username.group(1), username.group(2)]
    refresh(msg.message, app)


@bot.callback
def show_license_assign(msg: CallbackQuery):
    skus = session.skus
    store_lic_sel(msg.data[0], msg.data[1], skus)
    bot.edit_msg(msg.message,
                 Text.user_lic_asg.format('\n'.join(skus.values())),
                 msg.message.reply_markup)


@bot.callback
def show_license_delete(msg: CallbackQuery):
    skus_del = session.skus_del
    store_lic_sel(msg.data[0], msg.data[1], skus_del)
    bot.edit_msg(msg.message,
                 Text.user_lic_del.format('\n'.join(skus_del.values())),
                 msg.message.reply_markup)


@bot.callback
@lock
@app_injector
def assign_role(msg: CallbackQuery, app: App):
    app.Role.add_member(msg.data, session.user_id)
    bot.send_msg(msg.message, Text.user_role_asg_s)


@bot.callback
@lock
@app_injector
def revoke_role(msg: CallbackQuery, app: App):
    app.Role.del_member(msg.data, session.user_id)
    bot.send_msg(msg.message, Text.user_role_del_s)


@bot.callback
@app_injector
def assign_license(msg: CallbackQuery, app: App):
    app.User.add_license(session.user_id, session.skus.keys())
    session.skus.clear()
    bot.send_msg(msg.message, Text.user_lic_asg_s)


@bot.callback
@app_injector
def delete_license(msg: CallbackQuery, app: App):
    app.User.delete_license(session.user_id, session.skus_del.keys())
    session.skus_del.clear()
    bot.send_msg(msg.message, Text.user_lic_del_s)


@bot.callback
@app_injector
def get_next_page(msg: CallbackQuery, app: App):
    if keyboard := gen_users_keyboard(app, int(msg.data)):
        bot.edit_msg(msg.message, Text.user_select, keyboard)
    else:
        bot.edit_msg(msg.message, Text.user_no)


@bot.callback
@app_injector
def add(msg: CallbackQuery, app: App):
    keyboard = Keyboard([[Btn(text=Text.user_name_suffix_back,
                              callback_func=back_to_name_suffix_list)]])
    bot.edit_msg(msg.message, Text.user_data, keyboard)
    bot.register_next_step(show_added_info, app, msg)


@bot.callback
@app_injector
def update_mailbox_suffix(msg: CallbackQuery, app: App):
    app.User.update_infos(user_id=session.user_id, username=session.username[0] + '@' + msg.data)
    refresh(msg.message, app)
    bot.send_msg(msg.message, Text.user_name_suffix_update_s)


@bot.callback
@app_injector
def back_to_user(msg: CallbackQuery, app: App):
    refresh(msg.message, app)


@bot.callback
@app_injector
def back_to_name_suffix_list(msg: CallbackQuery, app: App):
    if not (keyboard := gen_username_suffix(app)):
        return bot.send_msg(msg.message, Text.domain_no)
    bot.edit_msg(msg.message, Text.user_name_suffix_select, keyboard)


@bot.callback
@app_injector
def control(msg: CallbackQuery, app: App):
    match int(msg.data):
        case 0:
            list_lic_asg(msg, app)
        case 1:
            list_lic_del(msg, app)
        case 2:
            list_roles_asg(msg, app)
        case 3:
            list_roles_rvk(msg, app)
        case 4:
            delete(msg.message, app)
        case 5:
            read_name(msg.message, app)
        case 6:
            reset_password(msg.message, app)
        case 7:
            select_mailbox_suffix(msg, app)
        case 8:
            refresh(msg.message, app)
        case 9:
            back_to_users(msg.message, app)
        case _:
            raise Exception(Text.match_error)


@lock
def delete(msg: Message, app: App):
    app.User.delete(session.user_id)
    bot.edit_msg(msg, Text.user_delete_s, control_keyboard_back_only)


@lock
def read_name(msg: Message, app: App):
    bot.send_msg(msg, Text.user_rename)
    bot.register_next_step(rename, app, msg)


@lock
def select_mailbox_suffix(msg: CallbackQuery, app: App):
    if not (domain_list := app.Domain.list()):
        return bot.send_msg(msg.message, Text.domain_no)
    buttons = [[Btn(text=domain["id"],
                    callback_data=domain["id"],
                    callback_func=update_mailbox_suffix)]
               for domain in domain_list if domain["isVerified"]]
    buttons.append([Btn(text=Text.user_back_btn,
                        callback_func=back_to_user)])
    bot.edit_msg(msg.message,
                 Text.user_name.format("@".join(session.username)) + Text.user_name_suffix_select,
                 Keyboard(buttons))


@lock
def reset_password(msg: Message, app: App):
    password = gen_password()
    app.User.update_infos(user_id=session.user_id, password=password)
    bot.send_msg(msg, Text.user_reset_password.format(password))


def rename(msg: Message, app: App, old_msg: Message):
    app.User.update_infos(user_id=session.user_id,
                          username=msg.text + '@' + session.username[1],
                          display_name=msg.text)
    session.username[0] = msg.text
    refresh(old_msg, app)
    bot.send_msg(msg, Text.user_rename_s)


def refresh(msg: Message, app: App):
    user_data = app.User.get_infos(session.user_id)
    text = Format(user_data)
    try:
        bot.edit_msg(msg, text, session.user_keyboard)
    except Exception:
        pass


def list_by_search(msg: Message, app: App):
    session.user_search = msg.text
    if keyboard := gen_users_keyboard(app, 0):
        bot.send_msg(msg, Text.user_select, keyboard)
    else:
        bot.send_msg(msg, Text.user_no)
        bot.register_next_step(list_by_search, app)


def show_info_by_name(msg: Message, app: App):
    user_data, session.user_id = app.User.get_infos_by_name(msg.text)
    bot.send_msg(msg, Format(user_data), control_keyboard)


def show_added_info(msg: Message, app: App, callback_msg: CallbackQuery):
    input_data = msg.text.split('\n')
    username = input_data[0] + callback_msg.data
    password = input_data[1] if len(input_data) > 1 else gen_password()
    session.user_id = app.User.create(username, password)
    session.username = username.split("@")
    bot.edit_msg(callback_msg.message,
                 Text.user_create_s.format(username, password),
                 control_keyboard)


def list_roles_asg(msg: CallbackQuery, app: App):
    control_buttons = [Btn(text=Text.user_back_btn,
                           callback_func=back_to_user)]
    if not (role_list := app.Role.get_all()):
        return bot.edit_msg(msg.message, Text.user_role_no, Keyboard([control_buttons]))
    buttons = [[Btn(text=role["displayName"],
                    callback_data=role['id'],
                    callback_func=assign_role)]
               for role in role_list]
    buttons.append(control_buttons)
    bot.edit_msg(msg.message, Text.user_role_asg, Keyboard(buttons))


def list_roles_rvk(msg: CallbackQuery, app: App):
    control_buttons = [Btn(text=Text.user_back_btn,
                           callback_func=back_to_user)]
    if not (role_list := app.User.get_role(session.user_id)):
        return bot.edit_msg(msg.message, Text.user_role_no, Keyboard([control_buttons]))
    buttons = [[Btn(text=role["displayName"],
                    callback_data=role["roleTemplateId"],
                    callback_func=revoke_role)]
               for role in role_list]
    buttons.append(control_buttons)
    bot.edit_msg(msg.message, Text.user_role_del, Keyboard(buttons))


def store_lic_sel(sku_name: str, sku_id: str, container: dict):
    if sku_id in container:
        container.pop(sku_id)
    else:
        container[sku_id] = sku_name


def list_lic(callback_func, sub_list: list):
    buttons = []
    for sub in sub_list:
        pretty_sku_name = get_pretty_sku_name(sub["skuPartNumber"])
        buttons.append([Btn(text=pretty_sku_name,
                            callback_data=[pretty_sku_name, sub['skuId']],
                            callback_func=callback_func)])
    return buttons


def list_lic_asg(msg: CallbackQuery, app: App):
    control_buttons = [Btn(text=Text.user_lic_asg_btn,
                           callback_func=assign_license),
                       Btn(text=Text.user_back_btn,
                           callback_func=back_to_user)]
    if not (sub_list := app.Sub.get_all()):
        return bot.edit_msg(msg.message, Text.user_lic_no, Keyboard([control_buttons]))
    buttons = list_lic(show_license_assign, sub_list)
    buttons.append(control_buttons)
    bot.edit_msg(msg.message, Text.user_lic_asg_sel, Keyboard(buttons))


def list_lic_del(msg: CallbackQuery, app: App):
    control_buttons = [Btn(text=Text.user_lic_del_btn,
                           callback_func=delete_license),
                       Btn(text=Text.user_back_btn,
                           callback_func=back_to_user)]
    if not (sub_list := app.User.get_license(session.user_id)):
        return bot.edit_msg(msg.message, Text.user_lic_no, Keyboard([control_buttons]))
    buttons = list_lic(show_license_delete, sub_list)
    buttons.append(control_buttons)
    bot.edit_msg(msg.message, Text.user_lic_del_sel, Keyboard(buttons))


def back_to_users(msg: Message, app: App):
    session.user_links = [None]
    keyboard = gen_users_keyboard(app, 0)
    bot.edit_msg(msg, Text.user_select, keyboard)


def gen_password():
    return secrets.token_urlsafe(8)


def gen_username_suffix(app: App):
    if not (domain_list := app.Domain.list()):
        return
    buttons = [[Btn(text=domain["id"],
                    callback_data='@' + domain["id"],
                    callback_func=add)]
               for domain in domain_list if domain["isVerified"]]
    return Keyboard(buttons)


def gen_users_keyboard(app: App, page_index: int):
    user_list, next_link = app.User.get_all(session.user_links[page_index], session.user_search)
    if not user_list:
        return
    buttons = [[Btn(text=user["userPrincipalName"],
                    callback_data=[user["userPrincipalName"], user['id']],
                    callback_func=show_info)]
               for user in user_list]
    btn_page_switch = gen_page_switch(page_index, next_link)
    if next_link:
        session.user_links.append(next_link)
    if btn_page_switch:
        buttons.append(btn_page_switch)
    return Keyboard(buttons)
