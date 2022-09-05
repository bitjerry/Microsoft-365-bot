# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
Office 365 global management app
@Time: 2022/7/31 14:58
@Author: Mr.lin
@Version: v1
@File: __init__.py
"""
from .requests import *
from .modules import *


class App:

    def __init__(self, app_data: list):
        self._name = app_data[0]
        self._auth_info = app_data[1:4]
        req = Requests(*self._auth_info)
        for app_module in module_list:
            self.__setattr__(app_module.__name__, app_module(req))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def get_data(self) -> dict:
        return {
            "name": self._name,
            "client_id": f"{self._auth_info[0][:13]}******",
            "client_secret": f"{self._auth_info[1][:13]}******",
            "tenant_id": f"{self._auth_info[2][:13]}******"
        }


__all__ = ["App"]
