# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 10:44
@Author: Mr.lin
@Version: v1
@File: core.py
"""
import sys
import uuid
import trace
import config
from collections import OrderedDict
from typing import Callable
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, Update
from office.requests import MsError
from office import App
from res import Text
from types import FunctionType
from db import DbServer


class SessionUtil:

    def __init__(self):
        self.__app_id: int = 0
        self.__msgs_tracker: list[int] = []
        self.__sub_sessions: list[object] = []

    def exist_msg(self, msg: Message):
        return msg.message_id in self.__msgs_tracker

    def reg_msg(self, msg: Message):
        self.__msgs_tracker.append(msg.message_id)

    def register(self, sub_session_class: type) -> object:
        """
        Register a session class and return an object instance

        :param sub_session_class: sub_session_class: module session
        :return:
        """
        sub_session = sub_session_class()
        self.__sub_sessions.append(sub_session)
        return sub_session

    def reset(self):
        self.__msgs_tracker.clear()
        for sub_session in self.__sub_sessions:
            sub_session.__init__()

    @property
    def app_id(self):
        return self.__app_id

    @app_id.setter
    def app_id(self, appid: int):
        self.reset()
        self.__app_id = appid


class BotError(Exception):
    ...


class ModuleError(Exception):
    ...


class Bot(TeleBot):

    def __init__(self, token: str, admin_id: int):
        super().__init__(token, parse_mode='HTML')
        self.admin_id = admin_id
        self.__cmd_map: dict[str, Callable] = {}
        self.__callback_map: dict[str, dict] = {}
        self.__messages_notify()

    def __edit_msg(self,
                   msg: Message,
                   text: str,
                   keyboard: InlineKeyboardMarkup = None):
        return self.edit_message_text(text, msg.chat.id, msg.id, reply_markup=keyboard)

    def __send_msg(self,
                   msg: Message,
                   text: str,
                   keyboard: InlineKeyboardMarkup = None):
        return self.send_message(msg.chat.id, text, reply_markup=keyboard)

    def edit_msg(self,
                 msg: Message,
                 text: str,
                 keyboard: InlineKeyboardMarkup = None):
        msg = self.__edit_msg(msg, text, keyboard)
        session.reg_msg(msg)

    def send_msg(self,
                 msg: Message,
                 text: str,
                 keyboard: InlineKeyboardMarkup = None):
        msg = self.__send_msg(msg, text, keyboard)
        session.reg_msg(msg)

    def raise_error(self,
                    msg: Message,
                    e: Exception):
        try:
            error_type = type(e)
            if error_type == BotError:
                self.__edit_msg(msg, str(e))
            elif error_type == ModuleError:
                self.__send_msg(msg, str(e))
            elif error_type == MsError:
                self.__send_msg(msg, str(e))
                trace.exception(e)
            else:
                self.__send_msg(msg, Text.error)
                trace.exception(e)

        except Exception as e:
            trace.exception(e)

    def overseer(self, func: Callable):

        def wrapper(msg: Message | CallbackQuery, *args, **kwargs):
            try:
                return func(msg, *args, **kwargs)
            except Exception as e:
                msg = msg if type(msg) == Message else msg.message
                self.raise_error(msg, e)

        return wrapper

    def __messages_notify(self):
        @self.callback_query_handler(func=lambda msg: True)
        @self.overseer
        def __callback(msg: CallbackQuery):
            callback_func = callback.func_parse(msg)
            func_called = self.__callback_map.get(callback_func, None)
            if func_called and \
                    (not func_called.get("check_msg", True) or session.exist_msg(msg.message)):
                func_called["func"](msg)
            else:
                raise BotError(Text.expire)

        @self.message_handler(
            func=lambda msg: msg.chat.id == self.admin_id,
            content_types=["text"])
        @self.overseer
        def __cmd(msg: Message):
            command = msg.text[1:]
            func = self.__cmd_map.get(command, None)
            if func:
                session.reset()
                func(msg)

    def cmd(self, command: str | Callable = ""):
        """
        :param command: default use function name as bot command. no `/`
        :return:
        """

        def wrapper(func: Callable):
            nonlocal command
            if not command or type(command) == FunctionType:
                command = func.__name__
            self.__cmd_map[command] = func
            return func

        if type(command) == str:
            # print(command)
            return wrapper
        else:
            return wrapper(command)

    def callback(self,
                 callback_func: str | Callable = "",
                 check_msg: bool = True):
        """
        :param callback_func: callback function or function identification
        :param check_msg: check if the message for the current operation exists
        :return:
        """

        def wrapper(func: Callable):
            nonlocal callback_func
            if not callback_func or type(callback_func) == FunctionType:
                callback_func = func.__name__
            self.__callback_map[callback_func] = {
                "func": func,
                "check_msg": check_msg
            }
            return func

        if type(callback_func) == str:
            return wrapper
        else:
            return wrapper(callback_func)

    def register_next_step(self, message: Message, func: Callable, *arg, **kwargs):
        """
        Overwrite `modules.register_next_step_handler`

        Check command before callback function is called

        The `/cancel` command is programmed to cancel the current operation

        :param message:
        :param func:
        :return:
        """

        def hook_func(msg: Message, *args, **kw):
            if msg.text == "/cancel":
                self.clear_step_handler(msg)
                self.__send_msg(msg, Text.cancel)
            else:
                try:
                    func(msg, *args, **kw)
                except Exception as e:
                    self.raise_error(msg, e)
                    self.register_next_step(msg, func, *args, **kw)

        self.register_next_step_handler(message, hook_func, *arg, **kwargs)

    def get_message_call_back(self, message):
        return self.process_new_updates([Update.de_json(message)])


class KeyboardButton(InlineKeyboardButton):

    def __init__(self,
                 text: str,
                 callback_data: str = "",
                 callback_func: str | Callable = None,
                 **kwargs):
        callback_data = callback.data_gen(callback_func, callback_data)
        super().__init__(text=text, callback_data=callback_data, **kwargs)


class Callback:
    class DataStore:
        """
        LRU Cache for callback data

        As we all know, telegram bot cannot have more than 64 bytes of callback data
        """

        def __init__(self):
            """
            data_index = "@@@"+uuid
            """
            self.prefix = "@@@"
            self.capacity = 256
            self.store = OrderedDict()

        def add(self, value: str):
            key = str(uuid.uuid4())
            self.store[key] = value
            self.store.move_to_end(key)
            if len(self.store) > self.capacity:
                self.store.popitem(last=False)
            return self.prefix + key

        def get(self, key: str):
            if key.startswith(self.prefix):
                key = key.strip(self.prefix)
                if key not in self.store:
                    raise BotError(Text.expire)
                else:
                    self.store.move_to_end(key)
                    return self.store[key]
            else:
                return key

    def __init__(self):
        self.store = self.DataStore()
        self.data_sep = "#"
        self.text_sep = ":"

    def __parse(self, msg: CallbackQuery) -> list:
        return msg.data.split(self.data_sep, 1)

    def func_parse(self, msg: CallbackQuery) -> str:
        return self.__parse(msg)[0]

    def text_parse(self, msg: CallbackQuery) -> str | list:
        data_index = self.__parse(msg)[1]
        data = self.store.get(data_index)
        texts = data.split(self.text_sep)
        match len(texts):
            case 0:
                raise BotError(Text.null)
            case 1:
                return texts[0]
            case _:
                return texts

    def data_gen(self, func, text: str = ""):
        func = func.__name__ if type(func) == FunctionType else str(func)
        if text and (len(func) + len(text) + 1 >= 64):
            text = self.store.add(text)
        return func + self.data_sep + text

    def text_gen(self, *args: str) -> str:
        return self.text_sep.join(args)


class AppPool:

    def __init__(self):
        self._apps = []
        apps_data = DbServer.get_apps_data()
        for app_data in apps_data:
            self._add_app(app_data)

    def _add_app(self, app_data: list):
        self._apps.append(App(app_data))

    def add_app(self, app_data: list):
        """
        :param app_data: ["name", "client_id", "client_secret", "tenant_id"]
        :return:
        """
        DbServer.add_app(app_data)
        self._add_app(app_data)

    def remove_app(self, app_id: int):
        """
        Remove app

        :param app_id:
        :return:
        """
        app_name = self.get_app_name(app_id)
        DbServer.delete_app(app_name)
        self._apps.pop(app_id)

    def rename_app(self, app_id: int, new_name: str):
        """
        Rename app.

        :param app_id:
        :param new_name:
        :return:
        """
        app = self._apps[app_id]
        old_name = app.get_name()
        DbServer.rename_app(old_name, new_name)
        app.rename(new_name)

    def edit_app_infos(self, app_id: int, app_info: list):
        """
        :param app_id:
        :param app_info: ["client_id", "client_secret", "tenant_id"]
        :return:
        """
        app_name = self.get_app_name(app_id)
        DbServer.update_app_info(app_name, app_info)
        app_data = [app_name]
        app_data.extend(app_info)
        self._apps[app_id] = App(app_data)

    def get_app_data(self, app_id: int) -> dict:
        """
        :param app_id:
        :return:
        """
        app = self._apps[app_id]
        return app.get_data()

    def get_app(self, app_id: int) -> App:
        """
        :param app_id:
        :return:
        """
        return self._apps[app_id]

    def get_app_name(self, app_id: int) -> str:
        """
        Gets the name of the specified app

        :param app_id:
        :return:
        """
        app = self._apps[app_id]
        return app.get_name()

    def get_apps_name(self) -> list:
        """
        All apps name

        :return:
        """
        return [app.get_name() for app in self._apps]


def format_html(data: dict | str, prefix: str = ""):
    """
    Convert dictionary to HTML style string

    :param data:
    :param prefix: Prefix each line (do not use it!!!)
    :return:
    """
    if type(data) is dict:
        result = '\n'
        for d in data.items():
            format_data = format_html(d[1], prefix + ' - ')
            result += f'{prefix}<b>{d[0]}</b>: {format_data}'
        return result
    elif type(data) is list:
        match len(data):
            case 0:
                ...
            case 1:
                return format_html(data[0], prefix)
            case _:
                format_data = [format_html(d, prefix) for d in data]
                result = " -  -  -  -  -  - ".join(format_data)
                return result
    return f"<i>{data}</i>\n"


def app_check(func: Callable):
    def wrapper(msg: Message | CallbackQuery):
        app: App = app_pool.get_app(session.app_id)
        if app:
            func(msg, app)
        else:
            msg = msg if type(msg) == Message else msg.message
            bot.send_msg(msg, Text.app_no)

    wrapper.__name__ = func.__name__
    return wrapper


session = SessionUtil()
DbServer = DbServer()
app_pool = AppPool()
bot = Bot(config.TOKEN, int(config.ADMIN_ID))
Btn = KeyboardButton
Keyboard = InlineKeyboardMarkup
callback = Callback()

__all__ = ["app_pool",
           "app_check",
           "session",
           "format_html",
           "bot",
           "callback",
           "Btn",
           "Keyboard",
           "Message",
           "ModuleError",
           "CallbackQuery"]
