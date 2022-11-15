# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/29 23:39
@Author: Mr.lin
@Version: v1
@File: config
"""
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

PORT = os.getenv("PORT", 5000)
DATABASE_URL = os.getenv("DATABASE_URL")
OPERATION_SECRET = os.getenv("SECRET")
SECRET_TIMES = int(os.getenv("SECRET_TIMES", -1))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WELCOME_URL = os.getenv("WELCOME_URL", "/")
LANG = os.getenv("BOT_LANG", "en_us")
EXPIRE_KEY = int(os.getenv("EXPIRE_KEY", 300))
EXPIRE_LOGS = int(os.getenv("EXPIRE_LOGS", 30*24*3600))
DEBUG = bool(os.getenv("DEBUG", False))

