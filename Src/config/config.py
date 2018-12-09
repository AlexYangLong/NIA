# -*- coding: utf-8 -*-
# @author:Alex
# @file: config.py
# @time: 2018/11/17
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class CommonConfig(object):
    pass
    # SECRET_KEY = os.urandom(24)
    # # session相关配置，并将session中的数据保存到redis
    # SESSION_TYPE = 'redis'


class DevelopConfig(CommonConfig):
    # 配置Debug模式为 True
    DEBUG = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        'mysql', 'pymysql', 'alex', 'yl952001', '120.55.63.27', '3306', 'nia')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductConfig(CommonConfig):
    DEBUG = False


class TestConfig(CommonConfig):
    DEBUG = False
