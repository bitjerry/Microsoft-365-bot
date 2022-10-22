# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
Office 365 Global App

@Time: 2022/7/31 14:58
@Author: Mr.lin
@Version: v1
@File: __init__
"""
import os
from importlib import import_module
from collections import defaultdict, OrderedDict
from resource import Text
from db import *
from util.request import *


__all__ = ["App", "app_pool"]

for f in os.listdir(os.path.dirname(__file__)):
    if f.endswith('.py') and f != '__init__.py':
        import_module(f".{f[:-3]}", __package__)

module_class_list = MsRequest.__subclasses__()


class App:

    def __init__(self, app_id: int, name: str, *app_info: str):
        self._id = app_id
        self._name = name
        self._auth_info = app_info
        self.__bind_modules()

    def __bind_modules(self):
        req = Requests(*self._auth_info)
        for app_module in module_class_list:
            setattr(self, app_module.__name__, app_module(req))

    def get_data(self) -> dict:
        return {
            "name": self._name,
            "client_id": crypt.hidden(self._auth_info[0]),
            "client_secret": crypt.hidden(self._auth_info[1]),
            "tenant_id": crypt.hidden(self._auth_info[2])
        }

    def rename(self, new_name: str):
        rename_app(self._id, new_name)
        self._name = new_name

    def edit_info(self, *app_info: str):
        """
        :param app_info: ["client_id", "client_secret", "tenant_id"]
        :return:
        """
        update_app_info(self._id, *app_info)
        self._auth_info = app_info
        self.__bind_modules()


class AppPool:
    """
    LFU Cache
    """

    def __init__(self):
        self._capacity = 128
        self.least_freq = 1
        self._id_freq_map = {}
        self._freq_apps_map = defaultdict(OrderedDict)

    def __get(self, app_id: int) -> App:
        freq = self._id_freq_map[app_id]
        self._id_freq_map[app_id] += 1
        app = self._freq_apps_map[freq].pop(app_id)
        self._freq_apps_map[freq + 1][app_id] = app
        if not len(self._freq_apps_map[freq]):
            self.least_freq += 1
        return app

    def __put(self, app_id: int, app: App):
        self._id_freq_map[app_id] = 1
        self._freq_apps_map[1][app_id] = app
        if len(self._id_freq_map) > self._capacity:
            k, _ = self._freq_apps_map[self.least_freq].popitem(last=False)
            self._id_freq_map.pop(k)
        self.least_freq = 1

    def get(self, app_id: int) -> App:
        """
        :param app_id:
        :return:
        """
        if app_id in self._id_freq_map:
            return self.__get(app_id)
        elif app := get_app(app_id):
            app_obj = App(app[0], *app[1])
            self.__put(app_id, app_obj)
            return app_obj

    def clear(self):
        """
        clear all apps

        :return:
        """
        clear_all_apps()
        self.__init__()

    def remove(self, app_id: int):
        """
        Remove app

        :param app_id:
        :return:
        """
        delete_app(app_id)
        if app_id not in self._id_freq_map:
            return None
        freq = self._id_freq_map.pop(app_id)
        self._freq_apps_map[freq].pop(app_id)
        if not len(self._freq_apps_map[freq]) and freq == self.least_freq:
            self.least_freq += 1


app_pool = AppPool()
