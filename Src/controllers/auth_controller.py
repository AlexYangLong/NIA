# -*- coding: utf-8 -*-
# @author:Alex
# @file: auth_controller.py
# @time: 2018/11/19
import uuid

from flask import request, session, jsonify
from flask_restful import Resource

from Src.common.constant import STATUS_CODE
from Src.common.services import Message
from Src.services.service import LogService
from Src.services.user_service import UserService


class AuthController(Resource):
    """
    用户登录、登出接口
    """

    @staticmethod
    def post():
        """
        登录
        :return:
        """

        client_ip = request.remote_addr
        data = request.json
        # 判断是否有数据
        if data is None:
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="用户登录", action_en="user login",
                                 result_cn="失败", result_en="FAIL", reason="请求参数错误")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="请求参数错误",
                             msg_en="request parameter error.").to_dict()
            return jsonify(result)
        # 判断账户、密码的数据格式
        if not data.get("account").strip():
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="用户登录", action_en="user login",
                                 result_cn="失败", result_en="FAIL", reason="登录账号为空")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="登录账号为空",
                             msg_en="login account is empty.").to_dict()
            return jsonify(result)
        if not data.get("password").strip():
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="用户登录", action_en="user login",
                                 result_cn="失败", result_en="FAIL", reason="登录密码为空")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="登录密码为空",
                             msg_en="login password is empty.").to_dict()
            return jsonify(result)
        # UserService对象
        user_service = UserService()
        # 获取用户
        user = user_service.get_user_by_account(data.get("account").strip())
        # 判断是否存在
        if not user:
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="用户登录", action_en="user login",
                                 result_cn="失败", result_en="FAIL", reason="账户不存在")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="账户不存在",
                             msg_en="user account is not existed.").to_dict()
            return jsonify(result)
        # 判断密码是否正确
        if not user.check_password(data.get("password").strip()):
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="用户登录", action_en="user login",
                                 result_cn="失败", result_en="FAIL", reason="登录密码错误")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="登录密码错误",
                             msg_en="login password error.").to_dict()
            return jsonify(result)
        # 判断是否激活
        if not user.is_active:
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="用户登录", action_en="user login",
                                 result_cn="失败", result_en="FAIL", reason="用户未激活")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="用户未激活， 请联系管理员",
                             msg_en="user is not active, please contact administrator.").to_dict()
            return jsonify(result)
        # 生成新的token
        user_token = uuid.uuid1().hex
        # 更新token
        user_service.update_user_token(user, user_token)
        # 将用户信息保存在session中
        session["user_token"] = user_token
        session["user_id"] = user.id
        # 写运行日志

        # 写操作日志
        LogService.write_log(client_ip=client_ip, action_cn="用户登录", action_en="user login",
                             result_cn="成功", result_en="SUCCESS", reason="登录成功", user_id=user.id)
        result = Message(status_code=STATUS_CODE["SUCCESS"], msg_cn="登录成功",
                         msg_en="user login successful.").to_dict()
        return jsonify(result)

    @staticmethod
    def delete():
        """
        登出
        :return:
        """

        client_ip = request.remote_addr
        # 判断session中是否有token
        if not session.get("user_token"):
            # 写运行日志

            # 写操作日志
            LogService.write_log(client_ip=client_ip, action_cn="用户登出", action_en="user logout",
                                 result_cn="成功", result_en="SUCCESS", reason="用户已经登出")
            result = Message(status_code=STATUS_CODE["SUCCESS"], msg_cn="用户已经登出",
                             msg_en="user already logout.").to_dict()
            return jsonify(result)
        # 获取用户
        user = UserService().get_user_by_token(session.get("user_token"))
        # 清空session
        session.clear()
        # 写运行日志

        # 写操作日志
        LogService.write_log(client_ip=client_ip, action_cn="用户登出", action_en="user logout",
                             result_cn="成功", result_en="SUCCESS", reason="用户登出成功", user_id=user.id)
        result = Message(status_code=STATUS_CODE["SUCCESS"], msg_cn="用户登出成功",
                         msg_en="user logout successful.").to_dict()
        return jsonify(result)

