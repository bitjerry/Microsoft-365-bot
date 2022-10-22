# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/28 18:01
@Author: Mr.lin
@Version: v1
@File: requests
"""
import logging
import http
import config
import json as jsontool
from types import FunctionType
from http.client import HTTPSConnection
from urllib.parse import urlencode
from time import time

__all__ = ["MsError", "Response", "Requests", "MsRequest"]

logger = logging.getLogger("http.client")


def print_to_log(*args, **kwargs):
    logger.debug(" ".join(args))


# monkey-patch a `print` global into the http.client module; all calls to
# print() in that module will then use our print_to_log implementation
http.client.print = print_to_log


class MsError(Exception):

    def __init__(self, error_body):
        self.error_body = error_body

    def __str__(self):
        if type(self.error_body) == dict and (error := self.error_body.get("error")):
            if type(error) == dict and (message := error.get("message")):
                return message
            elif message := self.error_body.get("message"):
                return message
        return str(self.error_body)


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
                self.__json = jsontool.loads(self.__text)
        else:
            if "json" in response.getheader("Content-Type"):
                raise MsError(jsontool.loads(self.__text))
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
        self.__client_id: str = client_id
        self.__client_secret: str = client_secret
        self.__tenant_id: str = tenant_id
        self.__access_token: str = ""
        self.__token_expires: float = 0.0

    @staticmethod
    def _requests(method: str, host: str, url: str, body, headers: dict):
        conn = HTTPSConnection(host)
        conn.set_debuglevel(5 if config.DEBUG else 0)
        conn.request(method, url, body, headers)
        return Response(conn)

    def _refresh_token(self):
        """
        If the message expires,
        we use the refresh token to exchange new access token and refresh token.

        :return:
        :rtype:
        """
        if not self.__access_token or time() > self.__token_expires:
            self._get_token()

    def _get_token(self):
        """
        Encapsulates the OAuth2 authentication flow

        Get access token and refresh token by `client_id`, `client_secret` and `tenant_id`

        :return:
        :rtype:
        """
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        res: Response = self._requests(
            method="POST",
            host="login.microsoftonline.com",
            url=f'/{self.__tenant_id}/oauth2/v2.0/token',
            body=urlencode(data),
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        json = res.json
        self.__access_token = json['access_token']
        self.__token_expires = time() + json['expires_in']

    @staticmethod
    def _ms_requests(func: FunctionType):
        method = func.__name__.upper()

        def wrapper(self, **kwargs):
            self._refresh_token()
            if url := kwargs.get("url"):
                url = f"/v1.0/{url.strip('/')}"
                if params := kwargs.get("params"):
                    url = f"{url}?{urlencode(params)}"
            else:
                return

            if data := kwargs.get("data"):
                body = urlencode(data)
            elif json := kwargs.get("json"):
                body = jsontool.dumps(json)
            else:
                body = None

            auth_header = {'Authorization': f'Bearer {self.__access_token}'}
            headers = kwargs.get("headers", {'Content-Type': 'application/json'})
            headers |= auth_header
            return self._requests(method, "graph.microsoft.com", url, body, headers)

        return wrapper

    @_ms_requests
    def get(self, url: str, headers: dict, params: dict) -> Response:
        """
        Make a Get request to Microsoft Graph API

        :param url: Relative resource path. eg: `/user`
        :type url:
        :param headers: Custom header. The default value is `Content-Type: application/json`
        :type headers:
        :param params:
        :type params:
        :return:
        :rtype:
        """
        ...

    @_ms_requests
    def post(self, url: str, headers: dict, params: dict, data: dict, json) -> Response:
        """
        Make a Post request to Microsoft Graph API

        :param url: Relative resource path. eg: `/user`
        :type url:
        :param headers: Custom header. The default value is `Content-Type: application/json`
        :type headers:
        :param params:
        :type params:
        :param data:
        :type data:
        :param json:
        :type json:
        :return:
        :rtype:
        """
        ...

    @_ms_requests
    def delete(self, url: str, headers: dict) -> Response:
        """
        Make a Delete request to Microsoft Graph API

        :param url: Relative resource path. eg: `/user`
        :type url:
        :param headers: Custom header. The default value is `Content-Type: application/json`
        :type headers:
        :return:
        :rtype:
        """
        ...

    @_ms_requests
    def patch(self, url: str, headers: dict, data: dict, json) -> Response:
        """
        Make a Patch request to Microsoft Graph API

        :param url: Relative resource path. eg: `/user`
        :type url:
        :param headers: Custom header. The default value is `Content-Type: application/json`
        :type headers:
        :param data:
        :type data:
        :param json:
        :type json:
        :return:
        :rtype:
        """
        ...


class MsRequest:
    """
    Please extend this class in the app module to request the Microsoft server
    """
    def __init__(self, request: Requests):
        self.req = request
