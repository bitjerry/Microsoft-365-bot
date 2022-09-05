# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/29 23:39
@Author: Mr.lin
@Version: v1
@File: config
"""
import os

PORT = os.getenv('PORT', 5000)
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DATABASE_URL = os.getenv('DATABASE_URL')
DEBUG = True
