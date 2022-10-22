# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/9/18 9:54
@Author: Mr.lin
@Version: v1
@File: domain
"""
from util.request import *


class Domain(MsRequest):

    def __init__(self, request: Requests):
        super().__init__(request)

    def list(self):
        res = self.req.get(url="domains", params={"$select": "id, isVerified", "$value": ""})
        return res.json["value"]

    def get(self, domain_name: str):
        res = self.req.get(url=f"domains/{domain_name}")
        res.json.pop("@odata.context")
        return res.json

    def add(self, domain_name: str):
        res = self.req.post(url="domains", json={"id": domain_name})
        res.json.pop("@odata.context")
        return res.json

    def get_dns(self, domain_name: str):
        res = self.req.get(url=f"domains/{domain_name}/verificationDnsRecords")
        value = res.json["value"]
        for i in range(len(value)):
            value[i].pop('@odata.type')
            value[i].pop('id')
            value[i].pop("isOptional")
            value[i].pop("label")
        return value

    def verify(self, domain_name: str):
        res = self.req.post(url=f"domains/{domain_name}/verify")
        return res.ok

    def delete(self, domain_name: str):
        self.req.delete(url=f"domains/{domain_name}")
