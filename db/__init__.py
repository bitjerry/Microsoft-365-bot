# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/12 23:31
@Author: Mr.lin
@Version: v1
@File: __init__.py
"""

import logging
import uuid
import config
from .cryption import *
from contextlib import contextmanager
from sqlalchemy import Column, String, create_engine, inspect
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

uri = config.DATABASE_URL
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
engine = create_engine(uri, echo=False)
Base = declarative_base()

table_name = "apps"
column_name = ["id", "name", "client_id", "client_secret", "tenant_id"]
data_name = column_name[1:]
info_name = data_name[1:]


class Apps(Base):
    __tablename__ = table_name

    id = Column(String(36), primary_key=True)
    name = Column(String(64))
    client_id = Column(String(255))
    client_secret = Column(String(255))
    tenant_id = Column(String(255))

    def __init__(self,
                 name: str,
                 client_id: str,
                 client_secret: str,
                 tenant_id: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.client_id = crypt.encrypt(client_id)
        self.client_secret = crypt.encrypt(client_secret)
        self.tenant_id = crypt.encrypt(tenant_id)

    def parse(self):
        print(self.client_id)
        return [self.id,
                self.name,
                crypt.decrypt(self.client_id),
                crypt.decrypt(self.client_secret),
                crypt.decrypt(self.tenant_id)]


@contextmanager
def get_session() -> Session:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class DbServer:
    page_size = 10

    def __init__(self):
        inspector = inspect(engine)
        if not inspector.has_table(table_name):
            Base.metadata.create_all(engine, checkfirst=False)

    @staticmethod
    def check_empty():
        """
        Check if data already exists

        :return:
        """
        with get_session() as s:
            return s.query(Apps).first()

    @staticmethod
    def try_decode():
        with get_session() as s:
            return s.query(Apps).first().parse()

    @staticmethod
    def drop_apps():
        """

        :return:
        """
        Apps.__table__.drop(engine)

    @staticmethod
    def get_apps():
        """

        :return:
        """
        with get_session() as s:
            return [app.parse() for app in s.query(Apps).all()]

    @staticmethod
    def clear_apps():
        """

        :return:
        """
        with get_session() as s:
            s.execute(f"TRUNCATE {table_name}")

    @staticmethod
    def get_app_ids(page_index: int):
        """

        :param page_index:
        :return:
        """
        with get_session() as s:
            return s.query(Apps.id) \
                .limit(DbServer.page_size) \
                .offset(page_index * DbServer.page_size) \
                .all()

    @staticmethod
    def get_app(app_id: str):
        """

        :param app_id:
        :return:
        """
        with get_session() as s:
            return s.query(Apps).filter_by(id=app_id).first().parse()

    @staticmethod
    def add_app(*app_data):
        """

        :param app_data:
        :return:
        """
        with get_session() as s:
            s.add(Apps(*app_data))

    @staticmethod
    def add_apps(apps: list):
        """
        app: "id", "name", "client_id", "client_secret", "tenant_id"

        :param apps:
        :return:
        """
        if apps:
            with get_session() as s:
                s.execute(
                    Apps.__table__.insert(),
                    [{"id": app[0],
                      "name": app[1],
                      "client_id": crypt.encrypt(app[2]),
                      "client_secret": crypt.encrypt(app[3]),
                      "tenant_id": crypt.encrypt(app[4])}
                     for app in apps])

    @staticmethod
    def rename_app(app_id: str, new_name: str):
        """
        :param app_id:
        :param new_name:
        :return:
        """
        with get_session() as s:
            s.query(Apps).filter_by(id=app_id).update({"name": new_name}).first()

    @staticmethod
    def update_app_info(app_id: str, infos: list):
        """
        :param app_id:
        :param infos: new infos[client_id, client_secret, tenant_id]
        :return:
        """
        with get_session() as s:
            s.query(Apps).filter_by(id=app_id).update(
                {info_name[i]: crypt.encrypt(infos[i])
                 for i in range(len(infos))}).first()

    @staticmethod
    def delete_app(app_id: str):
        with get_session() as s:
            s.query(Apps).filter_by(id=app_id).delete().first()


__all__ = ["DbServer", "crypt", "CryptError"]
