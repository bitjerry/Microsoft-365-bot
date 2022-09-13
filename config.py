# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/29 23:39
@Author: Mr.lin
@Version: v1
@File: config
"""
import os

PORT = os.getenv("PORT", 5000)
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
WELCOME_URL = os.getenv("WELCOME_URL", "/")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "/")
SET_WEBHOOK_URL = os.getenv("SET_WEBHOOK_URL", "/set_webhook")
STOP_WEBHOOK_URL = os.getenv("STOP_WEBHOOK_URL", "/stop_webhook")
DATABASE_URL = os.getenv("DATABASE_URL")
OPERATION_SECRET = os.getenv("OPERATION_SECRET")
lang = "en"
SET_KEY = False
DEBUG = True
