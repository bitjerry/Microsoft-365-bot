# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/13 6:55
@Author: Mr.lin
@Version: v1
@File: cryption
"""
from resource import Text
from cryptography.fernet import Fernet

__all__ = ["crypt", "CryptError"]


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
        try:
            self.__key = self.hidden(key)
            self.Fernet = Fernet(key)
        except Exception as e:
            self.__init__()
            raise CryptError(e)

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
                self.__init__()
                raise CryptError(Text.key_unlock_f)
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
                self.__init__()
                raise CryptError(Text.key_unlock_f)
        else:
            raise CryptError(Text.key_empty)


crypt = Cryption()
