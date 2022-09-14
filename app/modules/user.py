# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/1 18:26
@Author: Mr.lin
@Version: v1
@File: User
"""
import secrets
import re
from typing import Iterable
from ..requests import *
from . import module


@module
class User:

    def __init__(self, requests: Requests):
        self._req = requests

    def get_all(self, url: str = "", search: str = "") -> tuple[list, str]:
        """
        get all user infos (10 users)

        :param search:
        :param url:
        :return: user list and next_url
        """
        headers = {}
        if url:
            params = None
        else:
            url = "/users"
            params = {
                "$top": 10,
                "$orderby": "userPrincipalName",
                "$select": "userPrincipalName, id"
            }
            if search:
                params["$search"] = f"\"userPrincipalName:{search}\""
                headers = {"ConsistencyLevel": "eventual"}
        res = self._req.get(url=url, params=params, headers=headers)
        data: dict = res.json
        next_link: str = data.get("@odata.nextLink", None)
        next_link = re.sub(".*?/users", "/users", next_link) if next_link else None
        return data["value"], next_link

    def delete(self, user_id: str):
        """

        :param user_id:
        :return:
        """
        return self._req.delete(url=f"users/{user_id}")

    def update_infos(self,
                     username: str,
                     new_username: str = None,
                     display_name: str = None,
                     password: str = None):
        """

        :param username:
        :param display_name:
        :param new_username:
        :param password:
        :return:
        """
        json = {}
        if display_name:
            json['displayName'] = display_name
        if new_username:
            json['userPrincipalName'] = new_username
        if password:
            json['passwordProfile'] = {'password': password}

        self._req.patch(url=f"/users/{username}", json=json)

    def _get_infos(self, user_id: str) -> dict:
        """
        Get user infos by user_id

        :param user_id:
        :return:
        """
        params = {"$select": "id,"
                             "displayName, "
                             "userPrincipalName, "
                             "mail, "
                             "otherMails, "
                             "mobilePhone, "
                             "preferredDataLocation, "
                             "preferredLanguage, "
                             "createdDateTime, "
                             "lastPasswordChangeDateTime"}
        res = self._req.get(url=f"/users/{user_id}", params=params)
        data: dict = res.json
        data.pop('@odata.context')
        return data

    def get_infos(self, user_id: str) -> dict:
        """
        Get user infos by user_id

        :param user_id:
        :return:
        """
        infos = self._get_infos(user_id)
        infos.pop("id")
        return infos

    def get_infos_by_name(self, username: str) -> tuple[dict, str]:
        """
        Get user infos by username

        :param username: xxx@contoso.com
        :return:
        """
        infos = self._get_infos(username)
        return infos, infos.pop("id")

    def get_license(self, user_id: str) -> dict:
        """
        List licenseDetails

        :param user_id:
        :return:
        """
        url = f"/users/{user_id}/licenseDetails"
        params = {"$select": "skuPartNumber, skuId"}
        res = self._req.get(url=url, params=params)
        return res.json["value"]

    def add_license(self, user_id: str, sku_ids: Iterable):
        """
        Add license to user

        :param user_id: xxx@domain.com
        :param sku_ids: the sku id list of license
        :return:
        """
        url = f"/users/{user_id}/assignLicense"
        json = {"addLicenses": [{'skuId': sku_id} for sku_id in sku_ids],
                "removeLicenses": []}
        self._req.post(url=url, json=json)

    def delete_license(self, user_id: str, sku_ids: Iterable):
        """
        Delete user's license

        :param user_id:
        :param sku_ids: the sku id list of license
        :return:
        """
        url = f'/users/{user_id}/assignLicense'
        json = {"addLicenses": [],
                "removeLicenses": list(sku_ids)}
        self._req.post(url=url, json=json)

    def get_role(self, user_id: str):
        """

        :param user_id:
        :return:
        """
        url = f"/users/{user_id}/memberOf/microsoft.graph.directoryRole"
        params = {"$select": "displayName, roleTemplateId"}
        res = self._req.get(url=url, params=params)
        return res.json['value']

    def create(self,
               username: str,
               display_name: str = None,
               password: str = None):
        """
        :param display_name:
        :param password: user password
        :param username: xxx@domain.com
        :return:
        """
        if not password:
            password = secrets.token_urlsafe(8)
        if not display_name:
            display_name = username.split('@')[0]
        json = {
            'accountEnabled': True,
            'displayName': display_name,
            'mailNickname': display_name,
            'passwordPolicies': 'DisablePasswordExpiration, DisableStrongPassword',
            'passwordProfile': {
                'password': password,
                'forceChangePasswordNextSignIn': True
            },
            'userPrincipalName': username,
            'usageLocation': 'CN'
        }
        res = self._req.post(url="/users", json=json)
        return {
                   "username": username,
                   "display_name": display_name,
                   "password": password
               }, res.json["id"]
