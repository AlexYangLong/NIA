# -*- coding: utf-8 -*-
# @author:Alex
# @file: service.py
# @time: 2018/11/18
import uuid

from werkzeug.security import generate_password_hash

from Src.common.models import db, LogInfo, UserInfo


class DBService(object):
    """
    用于初始化数据库、删除数据库
    """

    @staticmethod
    def init_db():
        try:
            hash_pwd_admin = generate_password_hash("admin")
            admin_token = uuid.uuid1().hex
            hash_pwd_user = generate_password_hash("user")
            user_token = uuid.uuid1().hex
            admin = UserInfo({
                "user_name": "admin",
                "user_account": "admin",
                "password": hash_pwd_admin,
                "phone": "18408260044",
                "email": "18408260044@163.com",
                "token": admin_token
            })
            user = UserInfo({
                "user_name": "user",
                "user_account": "user",
                "password": hash_pwd_user,
                "phone": "18408260044",
                "token": user_token
            })
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)
        return True

    @staticmethod
    def clear_db():
        try:
            db.drop_all()
        except Exception as ex:
            raise Exception(ex)
        return True


class LogService(object):
    """
    用于操作日志
    """

    @staticmethod
    def write_log(client_ip, action_cn, action_en, result_cn, result_en, reason=None, user_id=None):
        """
        写操作日志
        :param user_id: 用户id
        :param client_ip: 客户端IP
        :param action_cn: 操作内容中文
        :param action_en: 操作内容英文
        :param result_cn: 结果中文
        :param result_en: 结果英文
        :param reason: 失败原因
        :return:
        """

        try:
            log = LogInfo({
                "user_id": user_id,
                "client_ip": client_ip,
                "action_cn": action_cn,
                "action_en": action_en,
                "result_cn": result_cn,
                "result_en": result_en,
                "reason": reason
            })
            db.session.add(log)
            db.session.commit()
        except Exception as ex:
            print(ex)
            # 写运行日日志

    @staticmethod
    def get_log(user_id=None):
        """
        获取日志列表
        :return:
        """

        log_list = LogInfo.query.desc(LogInfo.create_time)
        if user_id:
            log_list = log_list.filter(LogInfo.user_id == user_id)
        return [log.to_dict() for log in log_list]
