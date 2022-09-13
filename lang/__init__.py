# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/9 0:01
@Author: Mr.lin
@Version: v1
@File: db.py
"""
import config
import sys
from . import en
from importlib import import_module

Text = en

if config.lang:
    Text = import_module(f".{config.lang}", __package__)

# __all__ = ["Text"]
