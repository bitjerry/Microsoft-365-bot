# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/4 8:20
@Author: Mr.lin
@Version: v1
@File: trace
"""
import config
from logging import *
from functools import wraps

basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='bot.log',
    filemode='a',
    encoding='utf-8'
)


def monitor(func):
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


logger = getLogger()
if config.DEBUG:
    logger.setLevel(DEBUG)
else:
    logger.setLevel(INFO)

