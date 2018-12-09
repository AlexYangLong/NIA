# -*- coding: utf-8 -*-
# @author:Alex
# @file: capriccio_controller.py
# @time: 2018/12/07
from flask_restful import Resource

from Src.services.capriccio_service import CapriccioService


class CapriccioController(Resource):
    """
    随想相关接口
    """

    @staticmethod
    def get():
        CapriccioService().get_list()

    @staticmethod
    def post():
        pass

    @staticmethod
    def put():
        pass

    @staticmethod
    def delete():
        pass
