# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/3 21:09
@Author: Mr.lin
@Version: v1
@File: module
"""

module_list: list[type] = []


def module(app_module: type):
    """
    Please refer to Microsoft official documents for request parameters

    :param app_module: corresponds to an office function module
    :return:
    """
    module_list.append(app_module)
    return app_module


__all__ = ["module_list", "module"]
