# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/2 20:44
@Author: Mr.lin
@Version: v1
@File: role
"""
from util.request import *


class Role(MsRequest):

    def __init__(self, request: Requests):
        super().__init__(request)

    def get_all(self) -> dict[dict]:
        """
        List the directory roles that are activated in the tenant.

        :return: {"displayName": "id", ...}
        """
        params = {"$select": "displayName, id"}
        res = self.req.get(url="/directoryRoles", params=params)
        return res.json["value"]

    def get_info(self, role_id: str) -> dict:
        """
        Get role's detailed information by id

        :param role_id:
        :return:{displayName:xxx, description:xxx}
        """
        url = f"/directoryRoles/roleTemplateId={role_id}"
        params = {"$select": "displayName, description"}
        res = self.req.get(url=url, params=params)
        info = res.json
        info.pop("@odata.context")
        return info

    def get_member(self, role_id: str) -> list[dict]:
        """
        Retrieve the list of principals that are assigned to the directory role.

        :param role_id:
        :return: [{"userPrincipalName":xxx}, {""userPrincipalName":yyy}...]
        """
        url = f"/directoryRoles/roleTemplateId={role_id}/members/microsoft.graph.user"
        params = {"$select": "userPrincipalName"}
        res = self.req.get(url=url, params=params)
        return res.json['value']

    def add_member(self, role_id: str, user_id: str):
        """
        Assign a role to a specified user

        :param role_id:
        :param user_id:
        :return:
        """
        url = f"/directoryRoles/roleTemplateId={role_id}/members/$ref"
        json = {
            "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
        }
        self.req.post(url=url, json=json)

    def del_member(self, role_id, user_id):
        """
        Remove a member from a directoryRole.

        :param role_id:
        :param user_id:
        :return:
        """
        url = f"/directoryRoles/roleTemplateId={role_id}/members/{user_id}/$ref"
        self.req.delete(url=url)
