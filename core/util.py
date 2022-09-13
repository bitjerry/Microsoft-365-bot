# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/7 18:45
@Author: Mr.lin
@Version: v1
@File: util
"""


class SessionUtil:

    def __init__(self):
        self.__sub_sessions: dict[str, object] = {}

    def get(self, var: str):
        """
        Get the property value by the property name for Cross-Module Calls

        :param var:
        :return:
        """
        sub_session = self.__sub_sessions.get(var, None)
        if sub_session:
            return getattr(sub_session, var)
        else:
            return None

    def register(self, sub_session_class: type):
        """
        Register a session class and return an object instance

        :param sub_session_class: sub_session_class: module session
        :return:
        """
        sub_session = sub_session_class()
        for var in vars(sub_session).keys():
            self.__sub_sessions[var] = sub_session
        return sub_session

    def reset(self):
        """
        Expire all messages and reset all sessions

        :return:
        """
        for sub_session in self.__sub_sessions.values():
            sub_session.__init__()


class Format:
    """
    Convert dictionary to HTML + Yaml Style string
    """
    dict_prefix = "   "
    list_prefix = " - "

    def __init__(self, data):
        self.data = data

    def __dict(self, data: dict, level: int):
        result = ""
        for k, v in data.items():
            type_value = type(v)
            prefix = self.dict_prefix * level + f"<b>{k}</b>:"
            if type_value == dict:
                result += f"{prefix}{key}\n{self.__dict(v, level + 1)}"
            elif type_value == list:
                result += f"{prefix}{key}\n{self.__list(va, level + 1)}"
            else:
                result += f"{prefix}{key}{self.__var(v)}"
        return result

    def __list(self, data: list, level: int):
        result = ""
        for value in data:
            type_value = type(value)
            prefix = self.dict_prefix * (level - 1) + self.list_prefix
            if type_value == dict:
                res = self.__dict(value, level)
            elif type_value == list:
                res = self.__list(value, level + 1)
            else:
                res = self.__var(value)
            result += f"{prefix}{res.replace(self.dict_prefix * level, '', 1)}"
        return result

    @staticmethod
    def __var(data):
        return f"<i>{data}</i>\n"

    def __str__(self):
        type_value = type(self.data)
        if type_value == dict:
            return self.__dict(self.data, 0)
        elif type_value == list:
            return self.__list(self.data, 1)
        else:
            return self.__var(self.data)


__all__ = ["Format", "SessionUtil"]
