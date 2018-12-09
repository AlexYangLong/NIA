# -*- coding: utf-8 -*-
# @author:Alex
# @file: diary_controller.py
# @time: 2018/11/30
from flask import request, jsonify, session
from flask_restful import Resource

from Src.common.constant import STATUS_CODE
from Src.common.services import Message
from Src.services.diary_service import DiaryService
from Src.services.service import LogService
from Src.services.user_service import UserService
from Src.utils.decorator import login_required


class DiaryController(Resource):
    """
    日记增删改查接口
    """

    @staticmethod
    @login_required
    def get():
        """
        列表
        :return:
        """

        client_ip = request.remote_addr
        user = UserService().get_user_by_id(session.get("user_id"))
        try:
            # 获取日记列表
            diary_list = DiaryService().get_list()
            # 写运行日志、操作日志
            LogService.write_log(client_ip=client_ip, action_cn="获取日记列表", action_en="get diary list",
                                 result_cn="成功", result_en="SUCCESS", reason="获取日记列表成功",
                                 user_id=user.id)
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="获取日记列表成功",
                             msg_en="success to get diary list.").to_dict()
            result["data"] = diary_list
            return jsonify(result)
        except Exception as ex:
            print("获取日记列表失败，{}".format(ex))
            # 写运行日志、操作日志
            LogService.write_log(client_ip=client_ip, action_cn="获取日记列表", action_en="get diary list",
                                 result_cn="失败", result_en="FAIL", reason="获取日记列表失败，{}".format(ex),
                                 user_id=user.id)
            result = Message(status_code=STATUS_CODE["ERROR"], msg_cn="获取日记列表失败，{}".format(ex),
                             msg_en="failed to get diary list.").to_dict()
            return jsonify(result)

    @staticmethod
    @login_required
    def post():
        pass

    @staticmethod
    @login_required
    def put():
        pass

    @staticmethod
    @login_required
    def delete():
        pass
