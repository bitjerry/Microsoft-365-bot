# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/1 18:26
@Author: Mr.lin
@Version: v1
@File: User
"""
import re
from typing import Iterable
from util.request import *


class User(MsRequest):

    def __init__(self, request: Requests):
        super().__init__(request)

    def get_all(self, url: str = "", search: str = ""):
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
        res = self.req.get(url=url, params=params, headers=headers)
        next_link = res.json.get("@odata.nextLink")
        next_link = re.sub(".*?/users", "/users", next_link) if next_link else None
        return res.json["value"], next_link

    def delete(self, user_id: str):
        """

        :param user_id:
        :return:
        """
        return self.req.delete(url=f"users/{user_id}")

    def update_infos(
            self,
            user_id: str,
            username: str = None,
            display_name: str = None,
            password: str = None,
            enable: bool = True):
        """

        :param user_id:
        :param display_name:
        :param username:
        :param password:
        :param enable:
        :return:
        """
        json = {}
        if display_name:
            json['displayName'] = display_name
        if username:
            json['userPrincipalName'] = username
        if password:
            json['passwordProfile'] = {'password': password}

        json["accountEnabled"] = enable

        self.req.patch(url=f"/users/{user_id}", json=json)

    def _get_infos(self, user_id: str):
        """
        Get user infos by user_id

        :param user_id:
        :return:
        """
        params = {"$select": "id,"
                             "displayName, "
                             "userPrincipalName, "
                             "accountEnabled, "
                             "mail, "
                             "otherMails, "
                             "mobilePhone, "
                             "preferredDataLocation, "
                             "preferredLanguage, "
                             "createdDateTime, "
                             "lastPasswordChangeDateTime"}
        res = self.req.get(url=f"/users/{user_id}", params=params)
        res.json.pop('@odata.context')
        return res.json

    def get_infos(self, user_id: str):
        """
        Get user infos by user_id

        :param user_id:
        :return:
        """
        infos = self._get_infos(user_id)
        infos.pop("id")
        return infos

    def get_infos_by_name(self, username: str):
        """
        Get user infos by username

        :param username: xxx@contoso.com
        :return:
        """
        infos = self._get_infos(username)
        return infos, infos.pop("id")

    def get_license(self, user_id: str):
        """
        List licenseDetails

        :param user_id:
        :return:
        """
        url = f"/users/{user_id}/licenseDetails"
        params = {"$select": "skuPartNumber, skuId"}
        res = self.req.get(url=url, params=params)
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
        self.req.post(url=url, json=json)

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
        self.req.post(url=url, json=json)

    def get_role(self, user_id: str):
        """

        :param user_id:
        :return:
        """
        url = f"/users/{user_id}/memberOf/microsoft.graph.directoryRole"
        params = {"$select": "displayName, roleTemplateId"}
        res = self.req.get(url=url, params=params)
        return res.json['value']

    def create(self, username: str, password: str):
        """
        :param password: user password
        :param username: xxx@domain.com
        :return:
        """
        display_name = username.split('@', 1)[0]
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
        res = self.req.post(url="/users", json=json)
        return res.json["id"]
