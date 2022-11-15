# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/12 23:31
@Author: Mr.lin
@Version: v1
@File: db
"""

from sqlalchemy import Column, String, Integer, create_engine, inspect, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

import logging
from contextlib import contextmanager

import config
from util.cryption import *

__all__ = ["count", "is_empty", "try_decode", "add_app", "add_apps",
           "get_all_apps", "drop_apps", "list_apps", "get_app", "delete_app",
           "clear_all_apps", "rename_app", "update_app_info", "crypt", "CryptError"]

TABLE_NAME = "apps"
COLUMN_NAME = ["app_id", "name", "client_id", "client_secret", "tenant_id"]
DATA_NAME = COLUMN_NAME[1:]
INFO_NAME = DATA_NAME[1:]

logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.DEBUG if config.DEBUG else logging.NOTSET)

URI = config.DATABASE_URL
if URI.startswith("postgres://"):
    URI = URI.replace("postgres://", "postgresql://", 1)
engine = create_engine(
    URI,
    echo=False,
    pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True)
Base = declarative_base()


class Apps(Base):
    __tablename__ = TABLE_NAME

    app_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(64))
    client_id = Column(String(255))
    client_secret = Column(String(255))
    tenant_id = Column(String(255))

    def __init__(self,
                 name: str,
                 client_id: str,
                 client_secret: str,
                 tenant_id: str):
        self.name = name
        self.client_id = crypt.encrypt(client_id)
        self.client_secret = crypt.encrypt(client_secret)
        self.tenant_id = crypt.encrypt(tenant_id)

    def parse(self):
        return [self.name,
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


def create():
    Base.metadata.create_all(engine, checkfirst=False)


def count() -> int:
    with get_session() as session:
        return session.query(func.count(Apps.app_id)).scalar()


def is_empty() -> bool:
    """
    Check if data already exists

    :return:
    """
    with get_session() as session:
        return not session.query(Apps).first()


def try_decode() -> list:
    with get_session() as session:
        return session.query(Apps).first().parse()


def drop_apps():
    Apps.__table__.drop(engine)


def get_all_apps() -> list:
    with get_session() as session:
        return [dict(zip(DATA_NAME, app.parse()))
                for app in session.query(Apps).all()]


def clear_all_apps():
    """

    :return:
    """
    with get_session() as session:
        session.execute(f"TRUNCATE {TABLE_NAME}")
        # session.execute("ALTER SEQUENCE Apps.app_id RESTART WITH 1")


def list_apps(page_index: int, page_size: int) -> list:
    """
    Only app_id and name.

    :param page_size:
    :param page_index:
    :return:
    """
    with get_session() as session:
        return session \
            .query(Apps.app_id, Apps.name) \
            .order_by(Apps.app_id) \
            .limit(page_size) \
            .offset(page_index * page_size) \
            .all()


def get_app(app_id: int) -> (int, list):
    """

    :param app_id:
    :return:
    """
    with get_session() as session:
        app: Apps = session.query(Apps).filter_by(app_id=app_id).first()
        return (app.app_id, app.parse()) if app else None


def add_app(*app_data: str):
    """

    :param app_data: "name", "client_id", "client_secret", "tenant_id"
    :return:
    """
    with get_session() as session:
        session.add(Apps(*app_data))


def add_apps(apps: list):
    """
    app: "app_id", "name", "client_id", "client_secret", "tenant_id"

    :param apps: all app
    :return:
    """
    if not apps:
        return

    for app in apps:
        app["client_id"] = crypt.encrypt(str(app["client_id"]))
        app["client_secret"] = crypt.encrypt(str(app["client_secret"]))
        app["tenant_id"] = crypt.encrypt(str(app["tenant_id"]))
    with get_session() as session:
        session.execute(Apps.__table__.insert(), apps)


def rename_app(app_id: int, new_name: str):
    """
    :param app_id:
    :param new_name:
    :return:
    """
    with get_session() as session:
        session.query(Apps).filter_by(app_id=app_id).update({"name": new_name})


def update_app_info(app_id: int, *app_info: str):
    """
    :param app_id:
    :param app_info: new infos[client_id, client_secret, tenant_id]
    :return:
    """
    with get_session() as session:
        session.query(Apps).filter_by(app_id=app_id).update(
            {INFO_NAME[i]: crypt.encrypt(app_info[i])
             for i in range(len(app_info))})


def delete_app(app_id: int):
    with get_session() as session:
        session.query(Apps).filter_by(app_id=app_id).delete()


inspector = inspect(engine)
if inspector.has_table(TABLE_NAME):
    COLUMN_NAME_EXIST = {col["name"] for col in inspector.get_columns(TABLE_NAME)}
    if COLUMN_NAME_EXIST != set(COLUMN_NAME):
        logger.info(f"Rebuilding Apps Table... The origin columns name is {COLUMN_NAME_EXIST}")
        drop_apps()
        create()
else:
    logger.info(f"Create Apps Table...")
    create()
