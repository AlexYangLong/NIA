# -*- coding: utf-8 -*-
# @author:Alex
# @file: db_controller.py
# @time: 2018/11/18
from flask import request, jsonify, session
from flask_restful import Resource

from Src.common.constant import STATUS_CODE
from Src.common.services import Message
from Src.services.service import DBService, LogService
from Src.services.user_service import UserService


class DBController(Resource):
    @staticmethod
    def get():
        """
        初始化数据库
        :return:
        """

        client_ip = request.remote_addr
        try:
            if DBService.init_db():
                # 写运行日志、操作日志
                LogService.write_log(client_ip=client_ip, action_cn="初始化数据库", action_en="init db",
                                     result_cn="成功", result_en="SUCCESS")
                result = Message(status_code=STATUS_CODE["SUCCESS"], msg_cn="操作成功",
                                 msg_en="operation success.").to_dict()
                return jsonify(result)
        except Exception as ex:
            print("数据库初始化失败，{}".format(ex))
            # 写运行日志、操作日志
            LogService.write_log(client_ip=client_ip, action_cn="初始化数据库", action_en="init db",
                                 result_cn="失败", result_en="FAIL", reason="数据库初始化失败，{}".format(ex))
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="操作失败",
                             msg_en="operation fail.").to_dict()
            return jsonify(result)

    @staticmethod
    def delete():
        """
        删除数据库
        :return:
        """

        client_ip = request.remote_addr
        user_token = session.get("user_token")
        if not user_token:
            # 写运行日志、操作日志
            LogService.write_log(client_ip=client_ip, action_cn="删除数据库", action_en="drop db",
                                 result_cn="失败", result_en="FAIL", reason="数据库删除失败，用户token失效")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="数据库删除失败，用户token失效",
                             msg_en="operation fail.").to_dict()
            return jsonify(result)
        user = UserService().get_user_by_token(user_token)
        if not user:
            # 写运行日志、操作日志
            LogService.write_log(client_ip=client_ip, action_cn="删除数据库", action_en="drop db",
                                 result_cn="失败", result_en="FAIL", reason="数据库删除失败，用户不存在")
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="数据库删除失败，用户不存在",
                             msg_en="operation fail.").to_dict()
            return jsonify(result)
        try:
            if DBService.clear_db():
                # 写运行日志

                result = Message(status_code=STATUS_CODE["SUCCESS"], msg_cn="操作成功",
                                 msg_en="operation success.").to_dict()
                return jsonify(result)
        except Exception as ex:
            print("数据库删除失败，{}".format(ex))
            # 写运行日志、操作日志
            LogService.write_log(client_ip=client_ip, action_cn="删除数据库", action_en="drop db",
                                 result_cn="失败", result_en="FAIL", reason="数据库删除失败，{}".format(ex),
                                 user_id=user.id)
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="操作失败",
                             msg_en="operation fail.").to_dict()
            return jsonify(result)
