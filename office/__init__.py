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
from .module import *


class App:

    def __init__(self, app_data: list):
        self._app_name = app_data[0]
        self._app_auth_info = app_data[1:4]
        req = Requests(*self._app_auth_info)
        for app_module in module_list:
            self.__setattr__(app_module.__name__, app_module(req))

    def rename(self, new_name: str):
        """
        !!!

        :param new_name:
        :return:
        """
        self._app_name = new_name

    def get_name(self) -> str:
        """
        !!!

        :return:
        """
        return self._app_name

    def get_data(self) -> dict:
        """
        !!!

        :return:
        """
        return {
            "name": self._app_name,
            "client_id": f"{self._app_auth_info[0][:13]}******",
            "client_secret": f"{self._app_auth_info[1][:13]}******",
            "tenant_id": f"{self._app_auth_info[2][:13]}******"
        }
        # return {
        #     "name": self._app_name,
        #     "client_id": self._app_auth_info[0],
        #     "client_secret": self._app_auth_info[1],
        #     "tenant_id": self._app_auth_info[2]
        # }


__all__ = ["App"]
