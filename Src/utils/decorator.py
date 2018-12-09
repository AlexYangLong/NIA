# -*- coding: utf-8 -*-
# @author:Alex
# @file: decorator.py
# @time: 2018/11/30
import functools

from flask import session, jsonify, request

from Src.common.constant import STATUS_CODE
from Src.common.services import Message
from Src.services.service import LogService
from Src.services.user_service import UserService


def login_required(func):
    """
    判断用户是否登录的装饰器
    :param func:
    :return:
    """

    @functools.wraps
    def wrapper(*args, **kwargs):
        client_ip = request.remote_addr
        # 判断session中用户id
        if not session.get("user_id"):
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="判断session中用户id", action_en="judged user id in session",
                                 result_cn="失败", result_en="FAIL", reason="session中用户id不存在")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="session中用户id不存在",
                             msg_en="user id in session is not existed.").to_dict()
            return jsonify(result)
        # 判断session中用户token
        if not session.get("user_token"):
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="判断session中用户token",
                                 action_en="judged user token in session",
                                 result_cn="失败", result_en="FAIL", reason="session中用户token不存在")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="session中用户token不存在",
                             msg_en="user token in session is not existed.").to_dict()
            return jsonify(result)
        user = UserService().get_user_by_id(session.get("user_id"))
        if not user:
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="获取用户",
                                 action_en="get user by id",
                                 result_cn="失败", result_en="FAIL", reason="用户信息不存在")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="用户信息不存在",
                             msg_en="user is not existed.").to_dict()
            return jsonify(result)
        if user.token != session.get("user_token"):
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="判断用户token",
                                 action_en="judged user token",
                                 result_cn="失败", result_en="FAIL", reason="session中的用户token与数据库不一致")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="session中的用户token与数据库不一致",
                             msg_en="user is not existed.").to_dict()
            return jsonify(result)

        return func(*args, **kwargs)
    return wrapper
