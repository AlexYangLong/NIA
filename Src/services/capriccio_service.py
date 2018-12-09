# -*- coding: utf-8 -*-
# @author:Alex
# @file: capriccio_service.py
# @time: 2018/11/28
from Src.common.models import Capriccio, db


class CapriccioService(object):
    """
    用于随想操作
    """

    def get_list(self, key_word=None, order_by="down"):
        """
        获取列表
        :param key_word: 查询关键字
        :param order_by: 排序方式
        :return:
        """

        capriccio_list = Capriccio.query
        if key_word:
            capriccio_list = capriccio_list.filter(Capriccio.title.ilike("%{}%".format(key_word)))
        if order_by == "up":
            capriccio_list = capriccio_list.asc_by()
        else:
            capriccio_list = capriccio_list.desc_by()
        return [item.to_dict() for item in capriccio_list]

    def get_capriccio_by_id(self, capriccio_id):
        """
        根据id查询
        :param capriccio_id:
        :return:
        """

        capriccio = Capriccio.query.filter(Capriccio.id == capriccio_id).first()
        return capriccio

    def create_capriccio(self, extract, content, status, user_id):
        """
        创建
        :param extract:
        :param content:
        :param status:
        :param user_id:
        :return:
        """

        capriccio = Capriccio({
            "extract": extract,
            "user_id": user_id,
            "content": content,
            "status": status
        })

        db.session.add(capriccio)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def update_capriccio(self, capriccio, extract, content, status, user_id):
        """
        修改
        :param capriccio:
        :param extract:
        :param content:
        :param status:
        :param user_id:
        :return:
        """

        if not isinstance(capriccio, Capriccio):
            raise Exception("参数类型错误，不是一个Capriccio对象")
        capriccio.extract = extract
        capriccio.content = content
        capriccio.status = status
        capriccio.user_id = user_id
        db.session.add(capriccio)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def delete_capriccio(self, capriccio_id_list=None):
        """
        删除
        :param capriccio_id_list:
        :return:
        """

        if not capriccio_id_list:
            raise Exception("随想id不能为None")
        if not isinstance(capriccio_id_list, list):
            raise Exception("随想id参数不是一个列表")
        capriccio_list = Capriccio.query.filter(Capriccio.id in capriccio_id_list)
        for capriccio in capriccio_list:
            capriccio.is_delete = True
            db.session.add(capriccio)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def hit_zan(self, capriccio):
        """
        点赞
        :param capriccio:
        :return:
        """

        capriccio.zan_times = capriccio.zan_times + 1
        db.session.add(capriccio)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)
