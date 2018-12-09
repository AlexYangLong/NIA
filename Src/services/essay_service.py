# -*- coding: utf-8 -*-
# @author:Alex
# @file: essay_service.py
# @time: 2018/11/28
from Src.common.models import Essay, db


class EssayService(object):
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

        essay_list = Essay.query
        if key_word:
            essay_list = essay_list.filter(Essay.title.ilike("%{}%".format(key_word)))
        if order_by == "up":
            essay_list = essay_list.asc_by()
        else:
            essay_list = essay_list.desc_by()
        return [item.to_dict() for item in essay_list]

    def get_essay_by_id(self, essay_id):
        """
        根据id查询
        :param essay_id:
        :return:
        """

        essay = Essay.query.filter(Essay.id == essay_id).first()
        return essay

    def create_essay(self, title, content, status, user_id):
        """
        创建
        :param title:
        :param content:
        :param status:
        :param user_id:
        :return:
        """

        essay = Essay({
            "title": title,
            "user_id": user_id,
            "content": content,
            "status": status
        })

        db.session.add(essay)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def update_essay(self, essay, title, content, status, user_id):
        """
        修改
        :param essay:
        :param title:
        :param content:
        :param status:
        :param user_id:
        :return:
        """

        if not isinstance(essay, Essay):
            raise Exception("参数类型错误，不是一个Essay对象")
        essay.title = title
        essay.content = content
        essay.status = status
        essay.user_id = user_id
        db.session.add(essay)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def delete_essay(self, essay_id_list=None):
        """
        删除
        :param essay_id_list:
        :return:
        """

        if not essay_id_list:
            raise Exception("随笔id不能为None")
        if not isinstance(essay_id_list, list):
            raise Exception("随笔id参数不是一个列表")
        essay_list = Essay.query.filter(Essay.id in essay_id_list)
        for essay in essay_list:
            essay.is_delete = True
            db.session.add(essay)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def hit_zan(self, essay):
        """
        点赞
        :param essay:
        :return:
        """

        essay.zan_times = essay.zan_times + 1
        db.session.add(essay)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)
