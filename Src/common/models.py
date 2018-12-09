# -*- coding: utf-8 -*-
# @author:Alex
# @file: models.py
# @time: 2018/11/17
import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy()


def from_dict(obj, data):
    for key in data:
        value = data.get(key)
        if isinstance(value, list) or isinstance(value, dict):
            value = json.dumps(value)
        setattr(obj, key, value)


def object_to_dict(obj, wanted_list):
    result = dict()
    for key in wanted_list:
        result[key] = getattr(obj, key)
    return result


class BaseModel(object):
    """
    基础model
    """

    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)  # 主键id
    is_delete = db.Column(db.Boolean, default=False)  # 是否删除

    def __init__(self, data_dict):
        """
        初始化对象，使用字典形式
        :param data_dict: 字典
        """

        from_dict(self, data_dict)

    def to_dict(self, wanted_list):
        """
        obj转成dict
        :param wanted_list:
        :return:
        """

        return object_to_dict(self, wanted_list)


class UserInfo(BaseModel, db.Model):
    """
    用户信息
    """

    __tablename__ = "user_info"
    user_name = db.Column(db.String(32))  # 用户名
    user_account = db.Column(db.String(16), nullable=False)  # 用户账号
    password = db.Column(db.String(256), nullable=False)  # 用户密码
    gender = db.Column(db.Boolean, default=True)  # 性别
    phone = db.Column(db.String(12), nullable=False)  # 电话
    email = db.Column(db.String(64))  # 邮箱
    birth = db.Column(db.DateTime)  # 出生日期
    is_active = db.Column(db.Boolean, default=True)  # 是否激活
    token = db.Column(db.String(128))  # 口令

    logs = db.relationship("LogInfo", backref="user", lazy=True)
    diaries = db.relationship("Diary", backref="user", lazy=True)
    capriccios = db.relationship("Capriccio", backref="user", lazy=True)
    essays = db.relationship("Essay", backref="user", lazy=True)
    impressions = db.relationship("Impression", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class LogInfo(BaseModel, db.Model):
    """
    日志信息
    """

    __tablename__ = "log_info"
    user_id = db.Column(db.Integer, db.ForeignKey("user_info.id"))  # 外键id
    client_ip = db.Column(db.String(16), nullable=False)  # 客户端IP
    action_cn = db.Column(db.String(60), nullable=False)  # 操作内容中文
    action_en = db.Column(db.String(120), nullable=False)  # 操作内容英文
    result_cn = db.Column(db.String(12), nullable=False)  # 结果中文
    result_en = db.Column(db.String(12), nullable=False)  # 结果英文
    reason = db.Column(db.String(256))  # 失败原因

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "client_ip": self.client_ip,
            "action_cn": self.action_cn,
            "action_en": self.action_en,
            "result_cn": self.result_cn,
            "result_en": self.result_en,
            "reason": self.reason,
            "create_time": self.create_time
        }


class Diary(BaseModel, db.Model):
    """
    日记
    """

    user_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)  # 外键id
    week = db.Column(db.String(12))  # 星期
    weather = db.Column(db.String(16))  # 天气
    mood = db.Column(db.String(32))  # 心情
    content = db.Column(db.Text, nullable=False)  # 内容
    status = db.Column(db.String(12))  # 状态


class Capriccio(BaseModel, db.Model):
    """
    随想
    """

    user_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)  # 外键id
    extract = db.Column(db.Text, nullable=False)  # 摘录语句、段落
    content = db.Column(db.Text, nullable=False)  # 随想内容
    status = db.Column(db.String(12))  # 状态
    zan_times = db.Column(db.Integer, default=0)  # 点赞数


class Essay(BaseModel, db.Model):
    """
    随笔
    """

    user_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)  # 外键id
    title = db.Column(db.String(120), nullable=False)  # 标题
    abstract = db.Column(db.Text)  # 摘要
    content = db.Column(db.Text, nullable=False)  # 随笔内容
    status = db.Column(db.String(12))  # 状态
    zan_times = db.Column(db.Integer, default=0)  # 点赞数


class Impression(BaseModel, db.Model):
    """
    读后感
    """

    user_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)  # 外键id
    title = db.Column(db.String(120), nullable=False)  # 标题
    abstract = db.Column(db.Text)  # 摘要
    content = db.Column(db.Text, nullable=False)  # 读后感内容
    status = db.Column(db.String(12))  # 状态
    zan_times = db.Column(db.Integer, default=0)  # 点赞数


class Comment(BaseModel, db.Model):
    """
    评论
    """

    foreign_key = db.Column(db.Integer, nullable=False)  # 其他表外键id
    foreign_type = db.Column(db.String(16))  # 评论的种类
    comment_con = db.Column(db.Text)  # 评论内容
    comment_id = db.Column(db.Integer)  # 自关联外键id
    comment_user = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)  # 用户表外键id
