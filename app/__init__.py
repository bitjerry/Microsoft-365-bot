# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
Office 365 Global App

@Time: 2022/7/31 14:58
@Author: Mr.lin
@Version: v1
@File: __init__
"""
from lang import Text
from db import *
from .requests import *
from .modules import *
from collections import OrderedDict

__all__ = ["App", "AppPool", "MsError", "CryptError"]


class App:

    def __init__(self, *app_data: str):
        """

        :param app_data: ["name", "client_id", "client_secret", "tenant_id"]
        """
        self._name = app_data[0]
        self._auth_info = app_data[1:4]
        req = Requests(*self._auth_info)
        for app_module in module_list:
            setattr(self, app_module.__name__, app_module(req))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    def get_data(self) -> dict:
        return {
            "name": self._name,
            "client_id": crypt.hidden(self._auth_info[0]),
            "client_secret": crypt.hidden(self._auth_info[1]),
            "tenant_id": crypt.hidden(self._auth_info[2])
        }


class AppPool:

    def __init__(self):
        self.maxsize = 128
        self.__apps = OrderedDict()

    def __add(self, app_id: str, *app_data: str):
        self.__apps[app_id] = App(*app_data)
        self.__apps.move_to_end(app_id)
        if len(self.__apps) > self.maxsize:
            self.__apps.popitem(last=False)

    def add(self, *app_data: str):
        """
        :param app_data: ["name", "client_id", "client_secret", "tenant_id"]
        :return:
        """
        app_id = add_app(*app_data)
        self.__add(app_id, *app_data)

    def get(self, app_id: str) -> App:
        """
        :param app_id:
        :return:
        """
        if app_id in self.__apps:
            self.__apps.move_to_end(app_id)
            return self.__apps[app_id]
        else:
            self.__add(*get_app(app_id))
            return self.__apps[app_id]

    def clear(self):
        """
        clear all apps

        :return:
        """
        clear_apps()
        self.__apps.clear()

    def remove(self, app_id: str):
        """
        Remove app

        :param app_id:
        :return:
        """
        app_name = self.get_name(app_id)
        delete_app(app_name)
        self.__apps.pop(app_id)

    def rename(self, app_id: str, new_name: str):
        """
        Rename app.

        :param app_id:
        :param new_name:
        :return:
        """
        app = self.get(app_id)
        rename_app(app_id, new_name)
        app.name = new_name

    def edit_info(self, app_id: str, *app_info: str):
        """
        :param app_id:
        :param app_info: ["client_id", "client_secret", "tenant_id"]
        :return:
        """
        app_name = self.get_name(app_id)
        update_app_info(app_name, *app_info)
        self.__apps[app_id] = App(app_name, *app_info)

    def get_data(self, app_id: str) -> dict:
        """
        :param app_id:
        :return:
        """
        app = self.get(app_id)
        app._name = 0
        return app.get_data()

    def get_name(self, app_id: str) -> str:
        """
        Gets the name of the specified app

        :param app_id:
        :return:
        """
        return self.get(app_id).name

    def get_names(self) -> list:
        """
        Cache page [(app_id, app_name)...]

        :return:
        """
        app_ids = get_app_ids(0)
        return [(app_id[0], self.get_name(app_id[0])) for app_id in app_ids]
