# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/13 6:55
@Author: Mr.lin
@Version: v1
@File: cryption
"""
import os
from lang import Text
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa


class CryptError(Exception):
    ...


class Cryption:

    def __init__(self):
        self.__key: str = ""
        self.Fernet = None

    @property
    def key(self):
        """
        Show key

        :return:
        """
        return self.__key

    @key.setter
    def key(self, key: str):
        """
        Reset the key and protect it

        :param key:
        :return:
        """
        self.__key = self.hidden(key)
        self.Fernet = Fernet(key)

    def new(self):
        key = str(Fernet.generate_key(), 'utf-8')
        self.key = key
        return key

    @staticmethod
    def hidden(data: str):
        return f"{data[:13]}******" if data else ""

    def encrypt(self, data: str):
        """

        :param data:
        :return:
        """
        if self.Fernet:
            try:
                return str(self.Fernet.encrypt(bytes(data, 'utf-8')), "utf-8")
            except Exception:
                raise
        else:
            raise CryptError(Text.key_empty)

    def decrypt(self, data: str):
        """

        :param data:
        :return:
        """
        if self.Fernet:
            try:
                return str(self.Fernet.decrypt(data), "utf-8")
            except Exception:
                raise
        else:
            raise CryptError(Text.key_empty)


crypt = Cryption()

__all__ = ["crypt", "CryptError"]