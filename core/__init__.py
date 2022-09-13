# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/7 18:45
@Author: Mr.lin
@Version: v1
@File: core
"""
import uuid
import config
import logging
import sys
import time
import threading
from app import *
from .util import *
from lang import Text
from collections import OrderedDict
from typing import Callable
from types import FunctionType
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, Update

__all__ = ["bot", "session_util", "app_pool", "callback", "App",
           "Btn", "Text", "Format", "Keyboard", "Message",
           "ModuleError", "CallbackQuery"]

logger = logging.getLogger(__name__)


class BotError(Exception):
    ...


class ModuleError(Exception):
    ...


class MessageSession:

    def __init__(self):
        self.msg_tracker: dict[str, list[int]] = {}

    def exist(self, msg: Message):
        return any(msg.message_id in msg_list for msg_list in self.msg_tracker.values())

    def reg(self, module_name: str, msg: Message):
        if module_name in self.msg_tracker.keys():
            self.msg_tracker[module_name].append(msg.message_id)
        else:
            self.msg_tracker[module_name] = [msg.message_id]

    def clear(self, module_name: str):
        self.msg_tracker.pop(module_name)


class Bot(TeleBot):

    class FuncChecked:

        def __init__(self, check: bool, func: Callable):
            self.check: bool = check
            self.func: Callable = func

    class Event:

        def __init__(self, time_out: float, func: Callable, *args, **kwargs):
            self.time_out: float = time_out
            self.func: Callable = func
            self.func_args = (args, kwargs)

    def __init__(self, token: str, admin_id: int):
        super().__init__(token, parse_mode='HTML')
        self.cmd_func_map: dict[str, Callable] = {}
        self.callback_func_map: dict[str, Bot.FuncChecked] = {}
        self.events: dict[str, Bot.Event] = {}
        self.msg_session: MessageSession = session_util.register(MessageSession)
        self.admin_id: int = admin_id
        self.__messages_notify()
        self.__threading = threading.Thread(target=self.__daemon)
        self.__threading.daemon = True
        self.__threading.start()

    def __daemon(self):
        while True:
            time.sleep(1)
            try:
                for event_name in list(self.events.keys()):
                    event = self.events[event_name]
                    event.time_out -= 1
                    if not event.time_out:
                        args = event.func_args
                        event.func(*args[0], **args[1])
                        self.events.pop(event_name)
            except Exception as e:
                logger.exception(e)

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

    @staticmethod
    def __module_name():
        return sys._getframe(2).f_code.co_filename

    def clear_msg(self):
        self.msg_session.clear(self.__module_name())

    def edit_msg(self,
                 msg: Message,
                 text: str,
                 keyboard: InlineKeyboardMarkup = None):
        msg = self.__edit_msg(msg, text, keyboard)
        self.msg_session.reg(self.__module_name(), msg)
        return msg

    def send_msg(self,
                 msg: Message,
                 text: str,
                 keyboard: InlineKeyboardMarkup = None):
        msg = self.__send_msg(msg, text, keyboard)
        self.msg_session.reg(self.__module_name(), msg)
        return msg

    def raise_error(self,
                    msg: Message,
                    e: Exception):
        try:
            error_type = type(e)
            if error_type == BotError:
                self.__edit_msg(msg, str(e))
            elif error_type == ModuleError or error_type == CryptError:
                self.__send_msg(msg, str(e))
            elif error_type == MsError:
                logger.exception(e)
                self.__send_msg(msg, str(e))
            else:
                logger.exception(e)
                self.__send_msg(msg, Text.error)

        except Exception as e:
            logger.exception(e)

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
            func_called = self.callback_func_map.get(callback_func, None)
            if func_called and \
                    (not func_called.check or
                     self.msg_session.exist(msg.message)):
                func_called.func(msg)
            else:
                raise BotError(Text.expire)

        @self.message_handler(
            func=lambda msg: msg.chat.id == self.admin_id,
            content_types=["text"])
        @self.overseer
        def __cmd(msg: Message):
            func = self.cmd_func_map.get(msg.text[1:], None)
            if func:
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
            self.cmd_func_map[command] = func
            return func

        if type(command) == str:
            # print(command)
            return wrapper
        else:
            return wrapper(command)

    def callback(self,
                 callback_func: str | Callable = "",
                 check: bool = True):
        """
        :param callback_func: callback function or function identification
        :param check: check if the message for the current operation exists
        :return:
        """

        def wrapper(func: Callable):
            nonlocal callback_func
            if not callback_func or type(callback_func) == FunctionType:
                callback_func = func.__name__
            self.callback_func_map[callback_func] = Bot.FuncChecked(check, func)
            return func

        if type(callback_func) == str:
            return wrapper
        else:
            return wrapper(callback_func)

    def lock(self, func: Callable):
        secret = config.OPERATION_SECRET

        @self.overseer
        def wrapper(msg: Message | CallbackQuery):
            message = msg if type(msg) == Message else msg.message
            self.__send_msg(message, Text.key_cmp)

            @self.overseer
            def cmp(new_msg: Message):
                if new_msg.text == secret:
                    func(msg)
                else:
                    self.__send_msg(new_msg, Text.key_cmp_error)

            self.register_next_step(message, cmp)

        return wrapper if secret else func

    def delay(self, time_out: float):
        """

        :param time_out:
        :return:
        """

        def decorator(func):

            def wrapper(*args, **kwargs):
                self.events["delay"] = Bot.Event(time_out, func, *args, **kwargs)

            return wrapper

        return decorator

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
            if msg.text[0] == "/":
                self.clear_step_handler(msg)
                self.__send_msg(msg, Text.cancel)
            else:
                try:
                    func(msg, *args, **kw)
                except Exception as e:
                    self.raise_error(msg, e)
                    self.register_next_step(msg, func, *args, **kw)

        self.register_next_step_handler(message, hook_func, *arg, **kwargs)

    def update_message(self, message):
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


session_util = SessionUtil()
app_pool = AppPool()
bot = Bot(config.TOKEN, int(config.ADMIN_ID))
Btn = KeyboardButton
Keyboard = InlineKeyboardMarkup
callback = Callback()
