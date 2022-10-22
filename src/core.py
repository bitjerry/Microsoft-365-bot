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

__all__ = ["bot", "Btn", "Keyboard", "Message", "CallbackQuery"]

logger = logging.getLogger(__name__)
Keyboard = InlineKeyboardMarkup


def get_module_name(level: int):
    """
    Search the name of the module

    And make sure the module is in the service

    :param level: start level
    :type level: int
    :return:
    :rtype:
    """
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
    """
    Button of keyboard

    :param text: display on the button
    :type text: str
    :param callback_data: callback data for CallbackQuery when the button is triggered
    :type callback_data: int | str | list
    :param callback_func: callback function or function identifier
    :type callback_func: str | Callable
    :param args:
    :type args:
    :param kwargs:
    :type kwargs:
    """

    def __init__(self,
                 text: str,
                 callback_data: Any = "",
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
        """
        Add value to the container

        1. As the cache for the next quick invocation

        2. Compress the size of callback data

        :param value: data
        :type value: str
        :return: '@'+index of cache
        :rtype: str
        """
        key = hash(value)
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
        return self.prefix + str(key)

    def __get(self, key: str):
        """
        Get the value by key

        :param key: '@'+index of cache | other
        :type key: str
        :return: value
        :rtype:
        """
        if key.startswith(self.prefix):
            key = int(key.strip(self.prefix))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
        else:
            return key

    def parse(self, msg: CallbackQuery):
        """
        Parse the callback data

        Work for core

        Restore `msg.data` to callback_data and return the function id

        :param msg: The message returned when the button is triggered
        :type msg: CallbackQuery
        :return: function_id
        :rtype: str
        """
        if data := self.__get(msg.data):
            (function_id, text) = data.split(self.data_sep)
            texts = text.split(self.text_sep)
            msg.data = texts if len(texts) > 1 else texts[0]
            return function_id

    def gen(self, func: Callable | str, data: Any):
        """
        Generate callback data

        Work for core

        The callback function and callback data synthesis together,
        so that telegram bot button can bind callback function

        if len(result) > 64 return the compressed data(the index of cache)
        else return result

        :param func: function | function identifier
        :type func: Callable | str
        :param data: callback data
        :type data: Any
        :return: the index of cache | result
        :rtype: str
        """
        if type(data) == list:
            data = self.text_sep.join(data)
        if type(func) == FunctionType:
            func = func.__name__
        result = f"{get_module_name(3)}{func}{self.data_sep}{data}"
        return self.__add(result) if len(result) > 64 else result


class Bot(TeleBot):
    """
    See `TeleBot`

    - Message tracking to ensure data consistency in multiple tasks
    - The callback function is automatically bound to the callback data
    - Added the automatic startup execution function
    - Better error tracking
    - Improvements to register_next_step_handler
    - Short for decorator
    """

    def __init__(self):
        super().__init__(config.TOKEN, parse_mode='HTML')
        self.ADMIN_ID = config.ADMIN_ID
        self.message_tracker = {}
        self.func_map = {}
        self.func_check = set()
        self.start_func_queue = set()

    def __messages_notify(self):
        """
        Work for callback, command and on start function

        :return:
        :rtype:
        """

        @self.callback_query_handler(func=lambda msg: True)
        @self.overseer
        def __callback(msg: CallbackQuery):
            message = msg.message
            while function_id := callback.parse(msg):
                if function_id in self.func_check and message.id not in self.message_tracker:
                    break
                if func := self.func_map.get(function_id):
                    return func(msg)
                else:
                    break

            bot.edit_message_text(Text.expire, message.chat.id, message.id)

        @self.message_handler(
            func=lambda msg: msg.chat.id == self.ADMIN_ID,
            content_types=["text"])
        @self.overseer
        def __cmd(msg: Message):
            if func := self.func_map.get(msg.text[1:]):
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
        """
        Register message id to ensure data consistency

        :param func:
        :type func:
        :return:
        :rtype:
        """

        def wrapper(self, *args, **kwargs):
            message = func(self, *args, **kwargs)
            self.message_tracker[message.id] = get_module_name(2)
            return message

        return wrapper

    @__register_message
    def edit_msg(self, msg: Message, text: str, keyboard: Keyboard = None, **keyword):
        """
        Edit existing message data

        Throws an exception if the data (excluding the format) has not modified after editing

        The message is registered

        See `bot.edit_message_text()`

        :param msg: While message you want to modify
        :type msg: Message
        :param text: Display text after modify
        :type text: str
        :param keyboard: The Keyboard after modify
        :type keyboard: InlineKeyboardMarkup | Keyboard
        :param keyword:
        :type keyword:
        :return:
        :rtype:
        """
        return self.edit_message_text(
            text=text,
            chat_id=msg.chat.id,
            message_id=msg.id,
            reply_markup=keyboard,
            **keyword)

    @__register_message
    def send_msg(self, msg: Message, text: str, keyboard: Keyboard = None, **keyword):
        """
        Send a message to the user

        The message is registered

        See `bot.send_message()`

        :param msg:
        :type msg: Message
        :param text:
        :type text:
        :param keyboard:
        :type keyboard:
        :param keyword:
        :type keyword:
        :return:
        :rtype:
        """
        return self.send_message(
            chat_id=msg.chat.id,
            text=text,
            reply_markup=keyboard,
            **keyword)

    @__register_message
    def send_doc(self, msg: Message, doc: str, keyboard: Keyboard = None, **keyword):
        """
        Send a document to the user

        The message is registered

        See `bot.send_document()`

        :param msg:
        :type msg:
        :param doc:
        :type doc:
        :param keyboard:
        :type keyboard:
        :param keyword:
        :type keyword:
        :return:
        :rtype:
        """
        return self.send_document(
            chat_id=msg.chat.id,
            document=doc,
            reply_markup=keyboard,
            **keyword)

    def clear_all_msg(self):
        """
        Expire all messages

        :return:
        :rtype:
        """
        self.message_tracker.clear()

    def expire_mod_msg(self):
        """
        Expires the specified module message to ensure data consistency

        You don't need to supply any parameters, just use that in a service module

        :return:
        :rtype:
        """
        for k, v in tuple(self.message_tracker.items()):
            if v == get_module_name(2):
                self.message_tracker.pop(k)

    def overseer(self, func: Callable):
        """
        A decorator monitor exceptions to the robot

        Unknown exceptions are recorded in a log file

        Known exceptions are returned to the client

        :param func: The function to be monitored
        :type func: Callable
        :return:
        :rtype:
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if e.__class__.__name__ in ["CryptError", "MsError"]:
                    return self.send_message(self.ADMIN_ID, str(e))
                elif hasattr(e, "description") and "not modified" in e.description:
                    return self.send_message(self.ADMIN_ID, Text.not_modified)
                logger.exception(e)
                self.send_message(self.ADMIN_ID, Text.error)

        return wrapper

    def cmd(self, command: str | Callable = ""):
        """
        A decorator for the command response function of the robot

        :param command: default use function name as bot command. no `/`
        :type command: str
        :return:
        :rtype:
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

    def callback(self, function_identifier: str | Callable = "", check: bool = True):
        """
        A decorator to registers functions as callback functions

        :param function_identifier: function identification or callback function
        :type function_identifier: str | Callable
        :param check: check if the message for the current operation exists
        :type check: bool
        :return:
        :rtype:
        """
        module_name = get_module_name(2)

        def wrapper(func: Callable):

            nonlocal function_identifier
            if not function_identifier or type(function_identifier) == FunctionType:
                function_identifier = func.__name__
            function_id = module_name + function_identifier

            if check:
                self.func_check.add(function_id)
            self.func_map[function_id] = func
            return func

        if type(function_identifier) == str:
            return wrapper
        else:
            return wrapper(function_identifier)

    def on_startup(self, func: Callable):
        """
        A decorator makes the function to be called immediately after the robot starts, without any instructions

        :param func:
        :type func:
        :return:
        :rtype:
        """
        self.start_func_queue.add(func)
        return func

    def register_next_step(self, func: Callable, *args, **kwargs):
        """
        Check command before callback function is called

        Any command could interrupt the next step

        See `bot.register_next_step_handler()`

        :param func: The function to be called next. `def func(msg: Message, args, kwargs)`
        :type func: Callback
        :param args: The next function args
        :type args:
        :param kwargs: The next function kwargs
        :type kwargs:
        :return:
        :rtype:
        """

        @self.overseer
        def hook_func(*arg, **kw):
            if text := arg[0].text:
                if text[0] == "/":
                    self.clear_step_handler_by_chat_id(self.ADMIN_ID)
                    return self.send_message(self.ADMIN_ID, Text.cancel)
            func(*arg, **kw)

        self.register_next_step_handler_by_chat_id(self.ADMIN_ID, hook_func, *args, **kwargs)

    def update_message(self, message):
        """
        Update the message as new information comes in

        :param message:
        :type message: Any
        :return:
        :rtype:
        """
        return self.process_new_updates([Update.de_json(message)])

    def webhook(self, *args, **kwargs):
        self.__messages_notify()
        super().set_webhook(*args, **kwargs)

    def polling(self, *args, **kwargs):
        self.__messages_notify()
        self.delete_webhook()
        super().polling(*args, **kwargs)


bot = Bot()
Btn = KeyboardButton
callback = Callback()
