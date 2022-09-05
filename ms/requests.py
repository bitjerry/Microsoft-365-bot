# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/28 18:01
@Author: Mr.lin
@Version: v1
@File: requests
"""
import json
import trace
from types import FunctionType
from http.client import HTTPSConnection
from urllib.parse import urlencode
from time import time


class MsError(Exception):
    ...


class Response:
    text: bytes = b""
    ok: bool = False

    def __init__(self, conn: HTTPSConnection):
        self._json = None
        self._parse_res(conn.getresponse())

    def _parse_res(self, response):
        """
        If an exception occurs in the request,
        either a MsError exception or a http exception is thrown

        :return:
        """
        self.text = response.read()
        self.ok = 200 <= response.status < 400
        if self.ok:
            if self.text and "json" in response.getheader("Content-type"):
                self._json = json.loads(self.text)
        else:
            # trace.exception(self.text)
            if "json" in response.getheader("Content-Type"):
                error: dict = json.loads(self.text)
                raise MsError(error["error"]["message"])
            else:
                raise Exception(self.text)

    def json(self):
        return self._json

    def __str__(self):
        return self.text


class Requests:
    """
    By encapsulating the `http.client` module, a series of request methods are provided

    The header `Authorization` is attached,
    if you want to customize the request header, you do not need to include it
    """

    def __init__(self, client_id: str, client_secret: str, tenant_id: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._tenant_id = tenant_id
        self._access_token = ""
        self._token_expires = 0

    @staticmethod
    def _requests(method, host, url, body, headers):
        conn = HTTPSConnection(host)
        conn.request(method, url, body, headers)
        return Response(conn)

    def _refresh_token(self):
        if not self._access_token or time() > self._token_expires:
            self._get_token()

    def _get_token(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        res: Response = self._requests(method="POST",
                                       host="login.microsoftonline.com",
                                       url=f'/{self._tenant_id}/oauth2/v2.0/token',
                                       body=urlencode(data),
                                       headers={'Content-Type': 'application/x-www-form-urlencoded'})
        json_data = res.json()
        self._access_token = json_data['access_token']
        self._token_expires = int(json_data['expires_in']) + int(time())

    def _ms_requests(self, method: str, url: str, **kwargs):
        url = f"/v1.0/{url.strip('/')}"
        params = kwargs.get("params", None)
        if params:
            url = f"{url}?{urlencode(params)}"

        data = kwargs.get("data", None)
        if data:
            body = urlencode(data)
        else:
            json_data = kwargs.get("json", None)
            body = json.dumps(json_data) if json_data else None

        auth_header = {'Authorization': f'Bearer {self._access_token}'}
        headers = kwargs.get("headers", {'Content-Type': 'application/json'})
        headers |= auth_header
        return self._requests(method, "graph.microsoft.com", url, body, headers)

    @staticmethod
    def ms_requests(func: FunctionType):
        method = func.__name__.upper()

        def wrapper(self, url, **kwargs):
            self._refresh_token()
            return self._ms_requests(method, url, **kwargs)

        return wrapper

    @ms_requests
    def get(self, url: str, headers: dict, params: dict) -> Response:
        ...

    @ms_requests
    def post(self, url: str, headers: dict, params: dict, data: dict, json) -> Response:
        ...

    @ms_requests
    def delete(self, url: str, headers: dict) -> Response:
        ...

    @ms_requests
    def patch(self, url: str, headers: dict, data: dict, json) -> Response:
        ...


__all__ = ["MsError", "Response", "Requests"]
