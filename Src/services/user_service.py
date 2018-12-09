# -*- coding: utf-8 -*-
# @author:Alex
# @file: user_service.py
# @time: 2018/11/19
import uuid

from werkzeug.security import generate_password_hash

from Src.common.models import UserInfo, db


class UserService(object):
    """
    用于用户操作
    """

    def get_user_by_id(self, user_id):
        """
        根据用户id获取用户
        :param user_id:
        :return:
        """

        user = UserInfo.query.filter(UserInfo.id == user_id).first()
        return user

    def get_user_by_account(self, account):
        """
        根据账号获取用户
        :param account: 账号
        :return:
        """

        user = UserInfo.query.filter(UserInfo.user_account == account).first()
        return user

    def get_user_by_token(self, token):
        """
        根据token获取用户
        :param token:
        :return:
        """

        user = UserInfo.query.filter(UserInfo.token == token).first()
        return user

    def create_user(self, account, password, phone, username="", gender=True, email="", birth="", is_active=True):
        """
        创建用户
        :param account: 账号
        :param password: 密码
        :param phone: 国内电话
        :param username: 用户名
        :param gender: 性别
        :param email: 邮箱
        :param birth: 出生日期
        :param is_active: 是否激活
        :return:
        """

        token = uuid.uuid1()
        hash_pwd = generate_password_hash(password)
        user = UserInfo({
            "user_name": username,
            "user_account": account,
            "password": hash_pwd,
            "gender": gender,
            "phone": phone,
            "email": email,
            "birth": birth,
            "is_active": is_active,
            "token": token
        })

        db.session.add(user)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def update_user_info(self, user, phone, username="", gender=True, email="", birth=""):
        """
        修改用户普通信息
        :param user: 原user对象
        :param phone: 电话
        :param username: 用户名
        :param gender: 性别
        :param email: 邮箱
        :param birth: 出生日期
        :return:
        """

        if not isinstance(user, UserInfo):
            raise Exception("参数类型错误，不是一个UserInfo对象")
        user.phone = phone
        user.username = username
        user.gender = gender
        user.email = email
        user.birth = birth
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def update_user_password(self, user, new_password):
        """
        修改用户密码
        :param user: 原user对象
        :param new_password: 新密码
        :return:
        """

        if not isinstance(user, UserInfo):
            raise Exception("参数类型错误，不是一个UserInfo对象")
        hash_pwd = generate_password_hash(new_password)
        user.password = hash_pwd
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def change_user_active(self, user, is_active=True):
        """
        改变用户的状态
        :param user: 原user对象
        :param is_active: 激活状态
        :return:
        """

        if not isinstance(user, UserInfo):
            raise Exception("参数类型错误，不是一个UserInfo对象")
        user.is_active = is_active
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def delete_user_by_id(self, user_id_list=None):
        """
        删除用户
        :param user_id_list: 需删除的用户的id列表
        :return:
        """

        if not user_id_list:
            raise Exception("用户id列表不能为None")
        if not isinstance(user_id_list, list):
            raise Exception("用户id参数不是一个列表")
        user_list = UserInfo.query.filter(UserInfo.id in user_id_list)
        for user in user_list:
            user.is_delete = True
            db.session.add(user)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def update_user_token(self, user, new_token):
        """
        修改用户token
        :param user:
        :param new_token:
        :return:
        """

        if not isinstance(user, UserInfo):
            raise Exception("参数类型错误，不是一个UserInfo对象")
        user.token = new_token
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)
