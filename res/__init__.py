# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/3 23:36
@Author: Mr.lin
@Version: v1
@File: __init__.py
"""
import csv
from . import en
from os.path import dirname, join

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


# with open(join(pkg_path, "role.json"), 'r') as f:
#     """
#     read role template to dict{name:｛desc:xxx, id:xxx｝}\n
#     """
#     role_template: dict = json.load(f)


# def get_role_info(name: str) -> dict:
#     """
#     get more info of role\n
#     "Restricted Guest User": {\n
#         "id": "xxx",\n
#         "description": "xxxxxx"\n
#     }\n
#     :param name:
#     :return:
#     """
#     return role_template.get(name)


# roles_list = [(role[0], role[1]["id"]) for role in role_template.items()]
# _roles_list_len = len(roles_list)


# def get_roles(page_index: int, step: int = 10):
#     """
#     Get role information by section `[(name, id)...]`
#
#     :param page_index:
#     :param step: step = 10
#     :return: section for roles, is next section exist
#     """
#     start = page_index * step
#     end = start + step
#     return roles_list[start: end], end < _roles_list_len


Text = en

__all__ = ["get_pretty_sku_name", "Text"]
