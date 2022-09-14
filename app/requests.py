# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/28 18:01
@Author: Mr.lin
@Version: v1
@File: requests
"""
import json
import logging
import config
from types import FunctionType
from http.client import HTTPSConnection
from urllib.parse import urlencode
from time import time

__all__ = ["MsError", "Response", "Requests"]

logger = logging.getLogger(__name__)


class MsError(Exception):
    ...


class Response:

    def __init__(self, conn: HTTPSConnection):
        self.__text: bytes = b""
        self.__ok: bool = False
        self.__json = None
        self._parse_res(conn.getresponse())

    def _parse_res(self, response):
        """
        If an exception occurs in the request,
        either a MsError exception or a http exception is thrown

        :return:
        """
        self.__text = response.read()
        self.__ok = 200 <= response.status < 400
        if self.__ok:
            if self.__text and "json" in response.getheader("Content-type"):
                self.__json = json.loads(self.__text)
        else:
            if "json" in response.getheader("Content-Type"):
                error: dict = json.loads(self.__text)
                raise MsError(error["error"]["message"])
            else:
                raise Exception(self.__text)

    @property
    def json(self):
        return self.__json

    @property
    def text(self):
        return self.__text

    @property
    def ok(self):
        return self.__ok


class Requests:
    """
    By encapsulating the `http.client` module, a series of request methods are provided

    The header `Authorization` is attached,
    if you want to customize the request header, you do not need to include it
    """

    def __init__(self, client_id: str, client_secret: str, tenant_id: str):
        print(client_id, client_secret, tenant_id)
        self.__client_id: str = client_id
        self.__client_secret: str = client_secret
        self.__tenant_id: str = tenant_id
        self.__access_token: str = ""
        self.__token_expires: int = 0

    @staticmethod
    def _requests(method: str, host: str, url: str, body, headers: dict):
        conn = HTTPSConnection(host)
        conn.set_debuglevel(2 if config.DEBUG else 0)
        conn.request(method, url, body, headers)
        return Response(conn)

    def _refresh_token(self):
        if not self.__access_token or time() > self.__token_expires:
            self._get_token()

    def _get_token(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        res: Response = self._requests(method="POST",
                                       host="login.microsoftonline.com",
                                       url=f'/{self.__tenant_id}/oauth2/v2.0/token',
                                       body=urlencode(data),
                                       headers={'Content-Type': 'application/x-www-form-urlencoded'})
        json_data = res.json
        self.__access_token = json_data['access_token']
        self.__token_expires = int(json_data['expires_in']) + int(time())

    @staticmethod
    def _ms_requests(func: FunctionType):
        method = func.__name__.upper()

        def wrapper(self, url: str, **kwargs):
            self._refresh_token()
            url = f"/v1.0/{url.strip('/')}"
            if params := kwargs.get("params", None):
                url = f"{url}?{urlencode(params)}"

            if data := kwargs.get("data", None):
                body = urlencode(data)
            else:
                json_data = kwargs.get("json", None)
                body = json.dumps(json_data) if json_data else None

            auth_header = {'Authorization': f'Bearer {self.__access_token}'}
            headers = kwargs.get("headers", {'Content-Type': 'application/json'})
            headers |= auth_header
            return self._requests(method, "graph.microsoft.com", url, body, headers)

        return wrapper

    @_ms_requests
    def get(self, url: str, headers: dict, params: dict) -> Response:
        ...

    @_ms_requests
    def post(self, url: str, headers: dict, params: dict, data: dict, json) -> Response:
        ...

    @_ms_requests
    def delete(self, url: str, headers: dict) -> Response:
        ...

    @_ms_requests
    def patch(self, url: str, headers: dict, data: dict, json) -> Response:
        ...
