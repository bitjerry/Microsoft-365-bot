# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/2 11:56
@Author: Mr.lin
@Version: v1
@File: org
"""
from util.request import *


class Org(MsRequest):

    def __init__(self, request: Requests):
        super().__init__(request)

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
                       "verifiedDomains"}

        res = self.req.get(url="/organization", params=params)
        return res.json['value']

    def update_infos(self, org_id):
        ...
