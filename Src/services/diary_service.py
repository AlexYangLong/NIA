# -*- coding: utf-8 -*-
# @author:Alex
# @file: diary_service.py
# @time: 2018/11/28
from Src.common.models import Diary, db


class DiaryService(object):
    """
    用于日记操作
    """

    def get_list(self, key_word=None, order_by="down"):
        """
        获取列表
        :param key_word: 查询关键字
        :param order_by: 排序方式
        :return:
        """

        diary_list = Diary.query
        if key_word:
            diary_list = diary_list.filter(Diary.title.ilike("%{}%".format(key_word)))
        if order_by == "up":
            diary_list = diary_list.asc_by()
        else:
            diary_list = diary_list.desc_by()
        return [item.to_dict() for item in diary_list]

    def get_diary_by_id(self, diary_id):
        """
        根据id查询
        :param diary_id:
        :return:
        """

        diary = Diary.query.filter(Diary.id == diary_id).first()
        return diary

    def create_diary(self, week, weather, mood, content, status, user_id):
        """
        创建读后感
        :param week:
        :param weather:
        :param mood:
        :param content:
        :param status:
        :param user_id:
        :return:
        """

        diary = Diary({
            "week": week,
            "weather": weather,
            "mood": mood,
            "user_id": user_id,
            "content": content,
            "status": status
        })

        db.session.add(diary)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def update_diary(self, diary, week, weather, mood, content, status, user_id):
        """
        修改读后感
        :param diary:
        :param week:
        :param weather:
        :param mood:
        :param content:
        :param status:
        :param user_id:
        :return:
        """

        if not isinstance(diary, Diary):
            raise Exception("参数类型错误，不是一个Diary对象")
        diary.week = week
        diary.weather = weather
        diary.mood = mood
        diary.content = content
        diary.status = status
        diary.user_id = user_id
        db.session.add(diary)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def delete_diary(self, diary_id_list=None):
        """
        删除读后感
        :param diary_id_list:
        :return:
        """

        if not diary_id_list:
            raise Exception("日记id不能为None")
        if not isinstance(diary_id_list, list):
            raise Exception("日记id参数不是一个列表")
        diary_list = Diary.query.filter(Diary.id in diary_id_list)
        for diary in diary_list:
            diary.is_delete = True
            db.session.add(diary)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    # def hit_zan(self, diary):
    #     """
    #     点赞
    #     :param diary:
    #     :return:
    #     """
    #
    #     diary.zan_times = diary.zan_times + 1
    #     db.session.add(diary)
    #     try:
    #         db.session.commit()
    #     except Exception as ex:
    #         raise Exception(ex)
