# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/7/31 17:24
@Author: Mr.lin
@Version: v1
@File: cryption
"""
import os
import rsa
import base64
from trace import *


class Cryption:

    def __init__(self):
        pkg_path = os.path.split(os.path.realpath(__file__))[0]
        self.pubkey_path = f'{pkg_path}/pubkey'
        self.prvkey_path = f'{pkg_path}/prvkey'
        self._pub_key, self._prv_key = self._get_keys()

    def _get_keys(self):
        """
        Read the public key, private key
        If it does not exist, generate a key pair
        :return: public key, private key
        """

        if os.path.exists(self.pubkey_path) and os.path.exists(self.prvkey_path):
            with open(self.pubkey_path, 'rb') as pubkey_file:
                pubkey = rsa.PublicKey.load_pkcs1(pubkey_file.read())
            with open(self.prvkey_path, 'rb') as prvkey_file:
                prvkey = rsa.PrivateKey.load_pkcs1(prvkey_file.read())
        else:
            pubkey, prvkey = rsa.newkeys(512)
            with open(self.pubkey_path, 'wb') as pubkey_file:
                pubkey_file.write(pubkey.save_pkcs1())
            with open(self.prvkey_path, 'wb') as prvkey_file:
                prvkey_file.write(prvkey.save_pkcs1())
        self.clear_keyfile()
        return pubkey, prvkey

    @release
    def clear_keyfile(self):
        if os.path.exists(self.pubkey_path) and os.path.exists(self.prvkey_path):
            os.remove(self.pubkey_path)
            os.remove(self.prvkey_path)

    def encryption(self, data):
        """
        rsa encrypted data
        :param data:
        :return:
        """
        encrypted_text = rsa.encrypt(data.encode('utf-8'), self._pub_key)
        return str(base64.b64encode(encrypted_text), "utf-8")

    def decryption(self, data):
        """
        rsa decrypted data
        :param data:
        :return:
        """
        decrypted_text = base64.b64decode(data)
        return str(rsa.decrypt(decrypted_text, self._prv_key), 'utf-8')
