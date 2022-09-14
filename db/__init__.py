# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/12 23:31
@Author: Mr.lin
@Version: v1
@File: __init__
"""

import logging
import config
from .cryption import *
from contextlib import contextmanager
from sqlalchemy import Column, String, create_engine, inspect
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["check_empty", "try_decode", "add_app", "add_apps", "get_all_apps",
           "drop_apps", "get_app_ids", "get_app", "delete_app", "clear_all_apps",
           "rename_app", "update_app_info", "crypt", "CryptError"]

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

TABLE_NAME = "apps"
COLUMN_NAME = ["id", "name", "client_id", "client_secret", "tenant_id"]
DATA_NAME = COLUMN_NAME[1:]
INFO_NAME = DATA_NAME[1:]

PAGE_SIZE = 10

URI = config.DATABASE_URL
if URI.startswith("postgres://"):
    URI = URI.replace("postgres://", "postgresql://", 1)
engine = create_engine(URI, echo=False)
Base = declarative_base()


class Apps(Base):
    __tablename__ = TABLE_NAME

    id = Column(String(36), primary_key=True)
    name = Column(String(64))
    client_id = Column(String(255))
    client_secret = Column(String(255))
    tenant_id = Column(String(255))

    def __init__(self,
                 app_id: str,
                 name: str,
                 client_id: str,
                 client_secret: str,
                 tenant_id: str):
        self.id = app_id
        self.name = name
        self.client_id = crypt.encrypt(client_id)
        self.client_secret = crypt.encrypt(client_secret)
        self.tenant_id = crypt.encrypt(tenant_id)

    def parse(self):
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


inspector = inspect(engine)
if not inspector.has_table(TABLE_NAME):
    Base.metadata.create_all(engine, checkfirst=False)


def check_empty():
    """
    Check if data already exists

    :return:
    """
    with get_session() as s:
        return s.query(Apps).first()


def try_decode():
    with get_session() as s:
        return s.query(Apps).first().parse()


def drop_apps():
    Apps.__table__.drop(engine)


def get_all_apps():
    with get_session() as s:
        return [app.parse() for app in s.query(Apps).all()]


def clear_all_apps():
    """

    :return:
    """
    with get_session() as s:
        s.execute(f"TRUNCATE {TABLE_NAME}")


def get_app_ids(page_index: int):
    """

    :param page_index:
    :return:
    """
    with get_session() as s:
        return s.query(Apps.id) \
            .limit(PAGE_SIZE) \
            .offset(page_index * PAGE_SIZE) \
            .all()


def get_app(app_id: str):
    """

    :param app_id:
    :return:
    """
    with get_session() as s:
        return s.query(Apps).filter_by(id=app_id).first().parse()


def add_app(*app):
    """

    :param app: "id", "name", "client_id", "client_secret", "tenant_id"
    :return:
    """
    with get_session() as s:
        s.add(Apps(*app))


def add_apps(apps: list):
    """
    app: "id", "name", "client_id", "client_secret", "tenant_id"

    :param apps: all app
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


def rename_app(app_id: str, new_name: str):
    """
    :param app_id:
    :param new_name:
    :return:
    """
    with get_session() as s:
        s.query(Apps).filter_by(id=app_id).update({"name": new_name})


def update_app_info(app_id: str, *app_info: str):
    """
    :param app_id:
    :param app_info: new infos[client_id, client_secret, tenant_id]
    :return:
    """
    with get_session() as s:
        s.query(Apps).filter_by(id=app_id).update(
            {INFO_NAME[i]: crypt.encrypt(app_info[i])
             for i in range(len(app_info))})


def delete_app(app_id: str):
    with get_session() as s:
        s.query(Apps).filter_by(id=app_id).delete()
