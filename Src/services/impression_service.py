# -*- coding: utf-8 -*-
# @author:Alex
# @file: impression_service.py
# @time: 2018/11/28
from Src.common.models import Impression, db


class ImpressionService(object):
    """
    用于读后感操作
    """

    def get_list(self, key_word=None, order_by="down"):
        """
        获取列表
        :param key_word: 查询关键字
        :param order_by: 排序方式
        :return:
        """

        impression_list = Impression.query
        if key_word:
            impression_list = impression_list.filter(Impression.title.ilike("%{}%".format(key_word)))
        if order_by == "up":
            impression_list = impression_list.asc_by()
        else:
            impression_list = impression_list.desc_by()
        return [item.to_dict() for item in impression_list]

    def get_impression_by_id(self, impression_id):
        """
        根据id查询
        :param impression_id:
        :return:
        """

        impression = Impression.query.filter(Impression.id == impression_id).first()
        return impression

    def create_impression(self, title, content, status, user_id):
        """
        创建读后感
        :param title:
        :param content:
        :param status:
        :param user_id:
        :return:
        """

        impression = Impression({
            "title": title,
            "content": content,
            "status": status,
            "user_id": user_id
        })

        db.session.add(impression)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def update_impression(self, impression, title, content, status, user_id):
        """
        修改读后感
        :param impression:
        :param title:
        :param content:
        :param status:
        :param user_id:
        :return:
        """

        if not isinstance(impression, Impression):
            raise Exception("参数类型错误，不是一个Impression对象")
        impression.title = title
        impression.content = content
        impression.status = status
        impression.user_id = user_id
        db.session.add(impression)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def delete_impression(self, impression_id_list=None):
        """
        删除读后感
        :param impression_id_list:
        :return:
        """

        if not impression_id_list:
            raise Exception("读后感id不能为None")
        if not isinstance(impression_id_list, list):
            raise Exception("读后感id参数不是一个列表")
        impression_list = Impression.query.filter(Impression.id in impression_id_list)
        for impression in impression_list:
            impression.is_delete = True
            db.session.add(impression)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def hit_zan(self, impression):
        """
        点赞
        :param impression:
        :return:
        """

        impression.zan_times = impression.zan_times + 1
        db.session.add(impression)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)
