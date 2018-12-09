# -*- coding: utf-8 -*-
# @author:Alex
# @file: app.py
# @time: 2018/11/17
import os

from flask import Flask

from Src.conf.config import BASE_DIR, DevelopConfig


def create_app():
    """
    创建应用程序实例，并加载配置、蓝图、实例化第三方库等
    :return:
    """

    # 获取模板、静态文件路径
    templates_dir = os.path.join(BASE_DIR, "Web/templates")
    static_dir = os.path.join(BASE_DIR, "Web/static")
    # 应用程序实例
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    # 加载配置信息
    app.config.from_object(DevelopConfig)
    # 注册蓝图

    return app
