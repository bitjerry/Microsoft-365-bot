# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/22 21:23
@Author: Mr.lin
@Version: v1
@File: core
"""
import os
import sys
import config
import logging
from resource import Text
from collections import OrderedDict
from typing import Callable, Any
from types import FunctionType
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, Update

__all__ = ["bot", "callback", "Btn", "Keyboard", "Message", "CallbackQuery"]

logger = logging.getLogger(__name__)


def get_module_name(level: int):
    max_level = 8
    name = "service"
    while level < max_level:
        filepath = str(sys._getframe(level).f_code.co_filename)
        module_path = filepath.split(os.path.sep)
        if module_path[-2] == name:
            return os.path.splitext(module_path[-1])[0]
        else:
            level += 1
    logger.exception(Text.module_name_error)


class KeyboardButton(InlineKeyboardButton):

    def __init__(self,
                 text: str,
                 callback_data: str | list = "",
                 callback_func: str | Callable = None,
                 *args,
                 **kwargs):
        callback_data = callback.gen(callback_func, callback_data)
        super().__init__(text=text, callback_data=callback_data, *args, **kwargs)


class Callback:
    """
    data = module_name func_flag # text0 : text1 : text2 ...

    callback_data = @1234567 or data

    LRU Cache for callback data

    As we all know, telegram bot cannot have more than 64 bytes of callback data
    """

    def __init__(self):
        self.data_sep = "#"
        self.text_sep = ":"
        self.prefix = "@"
        self.capacity = 1024
        self.cache = OrderedDict()

    def __add(self, value: str):
        key = hash(value)
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
        return self.prefix + str(key)

    def __get(self, key: str):
        if key.startswith(self.prefix):
            key = int(key.strip(self.prefix))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
        else:
            return key

    def parse(self, msg: CallbackQuery):
        """

        :param msg:
        :return:
        """
        if data := self.__get(msg.data):
            (function_id, text) = data.split(self.data_sep)
            texts = text.split(self.text_sep)
            msg.data = texts if len(texts) > 1 else texts[0]
            return function_id

    def gen(self, func: FunctionType | str, data: str | list):
        """
        len(module_name) + len(func_flag) <= 26
        :param func:
        :param data:
        :return:
        """
        if type(data) == list:
            data = self.text_sep.join(data)
        if type(func) == FunctionType:
            func = func.__name__
        result = f"{get_module_name(3)}{func}{self.data_sep}{data}"
        return self.__add(result) if len(result) > 64 else result


class Bot(TeleBot):

    def __init__(self):
        super().__init__(config.TOKEN, parse_mode='HTML')
        self.ADMIN_ID = config.ADMIN_ID
        self.message_tracker = {}
        self.func_map = {}
        self.func_check = set()
        self.start_func_queue = set()

    def __messages_notify(self):
        @self.callback_query_handler(func=lambda msg: True)
        @self.overseer
        def __callback(msg: CallbackQuery):
            self.clear_step()
            message = msg.message
            if function_id := callback.parse(msg):
                if func := self.func_map.get(function_id, None):
                    if function_id not in self.func_check or message.message_id in self.message_tracker:
                        return func(msg)
            bot.edit_message_text(Text.expire, message.chat.id, message.id)

        @self.message_handler(
            func=lambda msg: msg.chat.id == self.ADMIN_ID,
            content_types=["text"])
        @self.overseer
        def __cmd(msg: Message):
            if func := self.func_map.get(msg.text[1:], None):
                func(msg)
            else:
                ...

        @self.overseer
        def __start_up():
            for func in self.start_func_queue:
                func()

        __start_up()

    @staticmethod
    def __register_message(func: Callable):
        def wrapper(self, *args, register: bool = True):
            message = func(self, *args)
            if register:
                self.message_tracker[message.message_id] = get_module_name(2)
            return message

        return wrapper

    @__register_message
    def edit_msg(self, msg: Message, text: str, keyboard: InlineKeyboardMarkup = None):
        return self.edit_message_text(text, msg.chat.id, msg.id, reply_markup=keyboard)

    @__register_message
    def send_msg(self, msg: Message, text: str, keyboard: InlineKeyboardMarkup = None):
        return self.send_message(msg.chat.id, text, reply_markup=keyboard)

    @__register_message
    def send_doc(self, msg: Message, doc: str, keyboard: InlineKeyboardMarkup = None):
        return self.send_document(msg.chat.id, doc, reply_markup=keyboard)

    def clear_all_msg(self):
        self.message_tracker.clear()

    def expire_mod_msg(self):
        for k, v in tuple(self.message_tracker.items()):
            if v == get_module_name(2):
                self.message_tracker.pop(k)

    def overseer(self, func: Callable):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if e.__class__.__name__ in ["CryptError", "MsError"]:
                    logger.exception(e)
                    self.send_message(self.ADMIN_ID, str(e))
                else:
                    logger.exception(e)
                    self.send_message(self.ADMIN_ID, Text.error)

        return wrapper

    def cmd(self, command: str | Callable = ""):
        """
        :param command: default use function name as bot command. no `/`
        :return:
        """

        def wrapper(func: Callable):
            nonlocal command
            if not command or type(command) == FunctionType:
                command = func.__name__
            self.func_map[command] = func
            return func

        if type(command) == str:
            return wrapper
        else:
            return wrapper(command)

    def callback(self, callback_func: str | Callable = "", check: bool = True):
        """
        :param callback_func: callback function or function identification
        :param check: check if the message for the current operation exists
        :return:
        """
        module_name = get_module_name(2)

        def wrapper(func: Callable):

            nonlocal callback_func
            if not callback_func or type(callback_func) == FunctionType:
                callback_func = func.__name__
            function_id = module_name + callback_func

            if check:
                self.func_check.add(function_id)
            self.func_map[function_id] = func
            return func

        if type(callback_func) == str:
            return wrapper
        else:
            return wrapper(callback_func)

    def on_startup(self, func: Callable):
        self.start_func_queue.add(func)
        return func

    def register_next_step(self, func: Callable, *args, **kwargs):
        """
        Overwrite `server.register_next_step_handler`

        Check command before callback function is called

        The `/cancel` command is programmed to cancel the current operation

        :param func:
        :return:
        """

        @self.overseer
        def hook_func(*arg, **kw):
            if text := arg[0].text:
                if text[0] == "/":
                    self.clear_step()
                    return self.send_message(self.ADMIN_ID, Text.cancel)
            func(*arg, **kw)

        self.register_next_step_handler_by_chat_id(self.ADMIN_ID, hook_func, *args, **kwargs)

    def clear_step(self):
        self.clear_step_handler_by_chat_id(self.ADMIN_ID)

    def update_message(self, message):
        return self.process_new_updates([Update.de_json(message)])

    def set_webhook(self, *args, **kwargs):
        self.__messages_notify()
        super().set_webhook(*args, **kwargs)

    def polling(self, *args, **kwargs):
        self.__messages_notify()
        super().polling(*args, **kwargs)


bot = Bot()
Btn = KeyboardButton
Keyboard = InlineKeyboardMarkup
callback = Callback()
