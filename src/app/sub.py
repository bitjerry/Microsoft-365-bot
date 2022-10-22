# !/usr/bin/python3
# -*-coding: UTF-8-*-
"""
@Time: 2022/8/1 18:27
@Author: Mr.lin
@Version: v1
@File: sub
"""
from util.request import *


class Sub(MsRequest):

    def __init__(self, request: Requests):
        super().__init__(request)

    def get_all(self) -> list:
        """
        Get all subscribes from this global

        :return:
        """
        params = {"$select": "skuPartNumber, skuId, id"}
        res = self.req.get(url="/subscribedSkus", params=params)
        return res.json["value"]

    def get_info(self, sku_id: str) -> dict:
        """

        :param sku_id:
        :return:
        """
        params = {
            "$select": "capabilityStatus,consumedUnits,prepaidUnits,skuId,skuPartNumber"
        }
        res = self.req.get(url=f"/subscribedSkus/{sku_id}", params=params)
        data = res.json
        data.pop('@odata.context')
        return data
