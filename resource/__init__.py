# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/3 23:36
@Author: Mr.lin
@Version: v1
@File: db.py
"""
import csv
from os.path import dirname, join

import config
from .i18n import en_us
from importlib import import_module

__all__ = ["Text", "get_pretty_sku_name"]

pkg_path = dirname(__file__)

name_for_sub = {}

with open(join(pkg_path, "name_for_sub.csv"), 'r', encoding='ISO-8859-1') as f:
    """
    read sub name to dict{sub_name: pretty_name}\n
    """
    reader = csv.reader(f)
    reader.__next__()
    for row in reader:
        name_for_sub[row[1].strip()] = row[0]


def get_pretty_sku_name(name: str) -> str:
    """
    get pretty name of sku\n
    :param name:
    :return:
    """
    return name_for_sub.get(name, name)


Text = en_us

if config.lang:
    Text = import_module(f".{config.lang}", f"{__package__}.i18n")
