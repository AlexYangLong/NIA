# -*- coding: utf-8 -*-
# @author:Alex
# @file: services.py
# @time: 2018/11/25
from Src.common.constant import STATUS_CODE


class Message(object):
    def __init__(self, status_code=STATUS_CODE["SUCCESS"], msg_cn="", msg_en=""):
        self.status_code = status_code
        self.msg_cn = msg_cn
        self.msg_en = msg_en

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "msg_cn": self.msg_cn,
            "msg_en": self.msg_en
        }
