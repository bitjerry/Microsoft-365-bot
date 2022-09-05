# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/1 18:08
@Author: Mr.lin
@Version: v1
@File: Pgdb
"""
import config
import psycopg2
# import sqlite3
import trace


class Pgdb:

    def __init__(self):
        self._dsn = config.DATABASE_URL

    def _execute(self, sql: str, data: list):
        conn = psycopg2.connect(self._dsn)
        cur = conn.cursor()
        # result = True
        try:
            cur.execute(sql, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            trace.exception(e)
            # result = False
        finally:
            conn.close()
        # return result

    def _query(self, sql: str) -> list:
        conn = psycopg2.connect(self._dsn)
        cur = conn.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            trace.exception(e)
            return []
        finally:
            conn.close()


# class SQLite:
#
#     def __init__(self):
#         self._dsn = "bot.db"
#
#     def _execute(self, sql: str, data: list):
#         conn = sqlite3.connect(self._dsn)
#         cur = conn.cursor()
#         # result = True
#         try:
#             cur.execute(sql.replace("%s", "?"), data)
#             conn.commit()
#         except Exception as e:
#             conn.rollback()
#             trace.exception(e)
#             # result = False
#         finally:
#             conn.close()
#         # return result
#
#     def _query(self, sql:str) -> list:
#         conn = sqlite3.connect(self._dsn)
#         cur = conn.cursor()
#         try:
#             res = cur.execute(sql)
#             return res.fetchall()
#         except Exception as e:
#             trace.exception(e)
#             return []
#         finally:
#             conn.close()
