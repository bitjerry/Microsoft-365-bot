# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/9 21:30
@Author: Mr.lin
@Version: v1
@File: db.py
"""
import config
from functools import wraps


def monitor(func):
    """
    Monitor input and output of functions.

    :param func:
    :return:
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        result = func(*args, **kwargs)
        info(f"{func.__name__}{args, kwargs}: -> {result}")
        return result

    return decorator


def debug(func):
    """
    Only executed when debugged(DEBUG=True)

    :param func:
    :return:
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs) if config.DEBUG else None

    return decorator


def release(func):
    """
    Only executed when released(DEBUG=FALSE)

    :param func:
    :return:
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs) if not config.DEBUG else None

    return decorator