# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
Office 365 Global App

@Time: 2022/7/31 14:58
@Author: Mr.lin
@Version: v1
@File: __init__
"""
import uuid
from lang import Text
from db import *
from .requests import *
from .modules import *
from collections import OrderedDict

__all__ = ["App", "AppPool", "MsError", "CryptError"]


class App:

    def __init__(self, app_id: str, name: str, *app_info: str):
        self._id = app_id
        self._name = name
        self._auth_info = app_info
        self.__bind_modules()

    def __bind_modules(self):
        req = Requests(*self._auth_info)
        for app_module in module_list:
            setattr(self, app_module.__name__, app_module(req))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        rename_app(self._id, new_name)
        self._name = new_name

    def get_data(self) -> dict:
        return {
            "name": self._name,
            "client_id": crypt.hidden(self._auth_info[0]),
            "client_secret": crypt.hidden(self._auth_info[1]),
            "tenant_id": crypt.hidden(self._auth_info[2])
        }

    def edit_info(self, *app_info: str):
        """
        :param app_info: ["client_id", "client_secret", "tenant_id"]
        :return:
        """
        update_app_info(self._id, *app_info)
        self._auth_info = app_info
        self.__bind_modules()


class AppPool:

    def __init__(self):
        self.maxsize = 128
        self.__apps = OrderedDict()

    def add(self, *app_data: str):
        """
        :param app_data: ["name", "client_id", "client_secret", "tenant_id"]
        :return:
        """
        app_id = str(uuid.uuid4())
        add_app(app_id, *app_data)
        self.__apps[app_id] = App(app_id, *app_data)
        self.__apps.move_to_end(app_id)
        if len(self.__apps) > self.maxsize:
            self.__apps.popitem(last=False)

    def get(self, app_id: str) -> App:
        """
        :param app_id:
        :return:
        """
        if app_id in self.__apps:
            self.__apps.move_to_end(app_id)
            return self.__apps[app_id]
        else:
            self.add(*get_app(app_id))
            return self.__apps[app_id]

    def clear(self):
        """
        clear all apps

        :return:
        """
        clear_all_apps()
        self.__apps.clear()

    def remove(self, app_id: str):
        """
        Remove app

        :param app_id:
        :return:
        """
        delete_app(app_id)
        self.__apps.pop(app_id)

    def get_names(self) -> list:
        """
        Cache page [(app_id, app_name)...]

        :return:
        """
        return [(app_id[0], self.get(app_id[0]).name)
                for app_id in get_app_ids(0)]
