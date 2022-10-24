# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/22 21:50
@Author: Mr.lin
@Version: v1
@File: tool
"""
import time
import threading
import logging
import config
from resource import Text
from app import App, app_pool
from core import *
from typing import Callable

logger = logging.getLogger(__name__)


class SessionUtil:

    def __init__(self):
        self.__sub_sessions = {}

    def __add_session(self, sub_session, *args):
        for var in args:
            self.__sub_sessions[var] = sub_session

    def __get_session(self, var: str):
        if sub_session := self.__sub_sessions.get(var):
            return sub_session

        for session in set(self.__sub_sessions.values()):
            if hasattr(session, var):
                sub_session = session
                break
        self.__add_session(sub_session, var)
        return sub_session

    def get(self, var: str):
        """
        Get the property value by the property name for Cross-Module Calls

        :param var:
        :return:
        """
        return getattr(self.__get_session(var), var)

    def set(self, var: str, value: str):
        return setattr(self.__get_session(var), var, value)

    def register(self, sub_session):
        """
        :param sub_session:
        :return:
        """
        self.__add_session(sub_session, *vars(sub_session).keys())

    def reset(self):
        """
        Expire all messages and reset all sessions

        :return:
        """
        for sub_session in self.__sub_sessions.values():
            sub_session.__init__()


class Event:
    """
    Event for Task
    """

    def __init__(self, time_out: int, loop: bool, func: Callable, *args, **kwargs):
        self.now: int = time_out
        self.func: Callable = func
        self.func_args = (args, kwargs)
        self.time_out: int = self.now if loop else 0


class Task:

    def __init__(self):
        self.__events: dict[str, Event] = {}
        self.__threading = threading.Thread(target=self.__task)
        self.__threading.daemon = True
        self.__threading.start()

    def __task(self):
        """
        Task time loop, loop a segment every second

        :return:
        :rtype:
        """
        while True:
            time.sleep(1)
            try:
                for event_name in list(self.__events.keys()):
                    event = self.__events[event_name]
                    event.now -= 1
                    if event.now:
                        continue
                    args = event.func_args
                    event.func(*args[0], **args[1])
                    if event.time_out:
                        event.now = event.time_out
                    else:
                        self.__events.pop(event_name)
            except Exception as e:
                logger.exception(e)

    def clear(self):
        """
        Cancel all tasks

        :return:
        :rtype:
        """
        self.__events.clear()

    def cancel(self, name: str):
        """
        Cancel a specified task by the task name

        :param name: task name
        :type name:
        :return:
        :rtype:
        """
        self.__events.pop(name)

    def delay(self, time_out: int, loop: bool = False, name: str = None):
        """
        As a decorator, delay the execution of a function

        :param time_out: Delay time
        :type time_out: int
        :param loop: Whether to execute the function in a loop.
        If yes, it will be executed every `time_out` after startup without stopping
        :type loop: bool
        :param name: task name
        :type name: str
        :return:
        :rtype:
        """

        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                nonlocal name
                name = name if name else func.__name__
                self.__events[name] = Event(time_out, loop, func, *args, **kwargs)

            wrapper.__name__ = func.__name__
            return wrapper

        return decorator


def lock(func: Callable):
    """
    A decorator to perform secret verification before the function is executed

    It works only if the` secret` in the environment variable has been configured

    :param func:
    :type func:
    :return:
    :rtype:
    """

    def wrapper(*args, **kwargs):
        bot.send_message(bot.ADMIN_ID, Text.secret_cmp)

        @bot.overseer
        def cmp(msg):
            global secret_max_times
            if not secret_max_times:
                return bot.send_msg(msg, Text.secret_lock)
            if msg.text == secret:
                secret_max_times = config.SECRET_TIMES
                func(*args, **kwargs)
            else:
                secret_max_times -= 1
                bot.send_msg(msg, Text.secret_cmp_error.format(secret_max_times))
                bot.register_next_step(cmp)

        bot.register_next_step(cmp)

    wrapper.__name__ = func.__name__

    return wrapper if secret else func


class Format:
    """
    Convert dictionary to HTML + Yaml Style string
    """
    dict_prefix = "   "
    list_prefix = " - "

    def __init__(self, data):
        self.data = self.__parse(data)

    def __parse(self, data):
        """
        Parse objects: dict, list, or var

        :param data:
        :type data:
        :return:
        :rtype:
        """
        type_value = type(data)
        if type_value == dict:
            return self.__dict(data)
        elif type_value == list:
            if len(data) == 1:
                return self.__parse(data[0])
            else:
                return self.__list(data)
        else:
            return self.__var(data)

    def __dict(self, data: dict, level: int = 0):
        """
        The dictionary style is `<b>key</b>: \n data`

        :param data: Each layer of data
        :type data: dict
        :param level: n level data, the level of layers is related to indentation
        :type level: int
        :return:
        :rtype:
        """
        result = ""
        prefix = self.dict_prefix * level
        for k, v in data.items():
            type_value = type(v)
            k = f"<b>{k}</b>:"
            if type_value == dict:
                result += f"{prefix}{k}\n{self.__dict(v, level + 1)}"
            elif type_value == list:
                result += f"{prefix}{k}\n{self.__list(v, level + 1)}"
            else:
                result += f"{prefix}{k} {self.__var(v)}"
        return result

    def __list(self, data: list, level: int = 1):
        """
        The list style is `- <i>value</i>`

        :param data: Each layer of data
        :type data: list
        :param level: n level data, the level of layers is related to indentation
        :type level: n
        :return:
        :rtype:
        """
        result = ""
        prefix = self.dict_prefix * (level - 1) + self.list_prefix
        for value in data:
            type_value = type(value)
            if type_value == dict:
                res = self.__dict(value, level)
            elif type_value == list:
                res = self.__list(value, level + 1)
            else:
                res = self.__var(value)
            result += prefix + res.replace(self.dict_prefix * level, '', 1)
        return result

    @staticmethod
    def __var(data):
        return f"<i>{data}</i>\n"

    def __str__(self):
        return self.data


def app_autowired(func: Callable):
    """
    As a decorator to inject the app object into the function

    Throws an exception if the object does not exist

    Make sure it's added at the end

    :param func:
    :type func:
    :return:
    :rtype:
    """

    @bot.overseer
    def wrapper(msg):
        if app := app_pool.get(session_util.get("app_id")):
            return func(msg, app)
        else:
            bot.send_message(bot.ADMIN_ID, Text.app_no)

    wrapper.__name__ = func.__name__
    return wrapper


def gen_control_keyboard(btn_data: dict, btn_line: int = 2):
    """
    Generate the control panel keyboard

    :param btn_data: Corresponds to the keyboard dict in Text
    :type btn_data:
    :param btn_line: n buttons per row
    :type btn_line:
    :return:
    :rtype:
    """
    btn_key = list(btn_data.keys())
    return Keyboard(
        [[Btn(text=btn_data.get(key),
              callback_func=key)
          for key in btn_key[i:i + btn_line]]
         for i in range(0, len(btn_key), btn_line)])


def gen_page_switch(page_index: int, has_next_page: bool):
    """
    Generates the up and down page buttons for the keyboard

    :param page_index: Page n(n=0,1,2...)
    :type page_index: int
    :param has_next_page: Whether there is a next page
    :type has_next_page: bool
    :return:
    :rtype:
    """
    btn_page_switch = []
    if page_index > 0:
        btn_page_switch.append(
            Btn(text=Text.page_up_btn,
                callback_data=page_index - 1,
                callback_func="get_next_page"))
    if has_next_page:
        btn_page_switch.append(
            Btn(text=Text.page_down_btn,
                callback_data=page_index + 1,
                callback_func="get_next_page"))
    return btn_page_switch


secret_max_times = config.SECRET_TIMES
secret = config.OPERATION_SECRET
task = Task()
session_util = SessionUtil()
