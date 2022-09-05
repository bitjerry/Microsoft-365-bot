# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 12:43
@Author: Mr.lin
@Version: v1
@File: __init__.py
"""
import glob
from os.path import dirname, basename, isfile, join


module_list: list[type] = []


def module(app_module: type):
    """
    Please refer to Microsoft official documents for request parameters

    :param app_module: corresponds to an ms function module
    :return:
    """
    module_list.append(app_module)
    return app_module


__all__ = ["module", "module_list"]

modules = glob.glob(join(dirname(__file__), "*.py"))
for f in modules:
    if isfile(f) and not f.endswith('__init__.py'):
        __all__.append(basename(f)[:-3])
