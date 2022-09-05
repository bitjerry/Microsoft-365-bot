# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
CRUD for app{name: [client_id, client_secret, tenant_id]} only
postgresql support

@Time: 2022/7/31 14:59
@Author: Mr.lin
@Version: v1
@File: __init__.py
"""
import trace

from .db import Pgdb
from . import cryption


# dsn = config.DATABASE_URL

class DbServer(Pgdb):

    def __init__(self):
        super().__init__()
        self._crypt = cryption.Cryption()
        self._init_table()

    def _init_table(self):
        sql = "select exists(select * from information_schema.tables where table_name='apps')"
        result = self._query(sql, [])
        if not result or not result[0][0]:
            sql = """CREATE TABLE apps (
                    "name" varchar(255) PRIMARY KEY NOT NULL,
                    "client_id" varchar(255) NOT NULL,
                    "client_secret" varchar(255) NOT NULL,
                    "tenant_id" varchar(255) NOT NULL)"""
            self._execute(sql, [])

    def get_apps_data(self) -> list:
        """
        get all apps

        :return: dirt of apps info {name: [client_id, client_secret, tenant_id]}
        """
        result = []
        try:
            for row in self._query("SELECT * FROM apps", []):
                row_decode = [row[0]]
                for r in row[1:]:
                    row_decode.append(self._crypt.decryption(r))
                result.append(row_decode)
        except Exception as e:
            trace.exception(e)
        return result

    def add_app(self, app_data: list):
        """
        :param app_data: new app_data[name, client_id, client_secret, tenant_id]
        :return:
        """
        sql = "INSERT INTO apps VALUES (%s, %s, %s, %s)"
        data = [app_data[0], *[self._crypt.encryption(info) for info in app_data[1:4]]]
        return self._execute(sql, data)

    def rename_app(self, old_name: str, new_name: str):
        """
        :param old_name:
        :param new_name:
        :return:
        """
        sql = "UPDATE apps SET name = %s WHERE name = %s"
        data = [new_name, old_name]
        return self._execute(sql, data)

    def update_app_info(self, name: str, infos: list):
        """
        :param name: app name
        :param infos: new infos[client_id, client_secret, tenant_id]
        :return:
        """
        sql = "UPDATE apps SET client_id = %s, client_secret = %s, tenant_id = %s WHERE name = %s"
        data = [self._crypt.encryption(info) for info in infos]
        data.append(name)
        return self._execute(sql, data)

    def delete_app(self, name: str):
        """
        :param name:
        :return:
        """
        sql = "DELETE FROM apps WHERE name = %s"
        return self._execute(sql, [name])


__all__ = ["DbServer"]
