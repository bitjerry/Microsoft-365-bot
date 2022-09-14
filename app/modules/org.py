# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/2 11:56
@Author: Mr.lin
@Version: v1
@File: org
"""
from ..requests import *
from . import module


@module
class Org:

    def __init__(self, requests: Requests):
        self._req = requests

    def get_infos(self):
        """
        By default, one app corresponds to one organization,

        although there can be multiple apps

        :return:
        """
        params = {
            "$select": "tenantId,"
                       "displayName,"
                       "createdDateTime,"
                       "businessPhones,"
                       "city,"
                       "country,"
                       "countryLetterCode,"
                       "postalCode,"
                       "preferredLanguage,"
                       "state,"
                       "street,"
                       "marketingNotificationEmails,"
                       "technicalNotificationMails,"
                       "tenantType,"
                       "directorySizeQuota,"
                       "verifiedDomains"
        }

        res = self._req.get(url="/organization", params=params)
        return res.json['value']

    def update_infos(self, org_id):
        ...
