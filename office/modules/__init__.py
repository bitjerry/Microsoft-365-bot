# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/27 12:43
@Author: Mr.lin
@Version: v1
@File: __init__.py
"""
from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
