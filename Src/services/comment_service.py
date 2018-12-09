# -*- coding: utf-8 -*-
# @author:Alex
# @file: comment_service.py
# @time: 2018/11/28
from Src.common.models import Comment, db


class CommentService(object):
    """
    评论操作
    """

    def get_comment_by_type_key(self, foreign_type, foreign_key):
        """
        根据评论种类、外键id获取
        :param foreign_type:
        :param foreign_key:
        :return:
        """

        comment_list = Comment.query.filter(Comment.foreign_key == foreign_key, Comment.foreign_type == foreign_type)
        return [item.to_dict() for item in comment_list]

    def create_comment(self, foreign_type, foreign_key, comment_con, comment_user, comment_id=None):
        """
        创建
        :param foreign_type:
        :param foreign_key:
        :param comment_con:
        :param comment_user:
        :param comment_id:
        :return:
        """

        comment = Comment({
            "foreign_type": foreign_type,
            "foreign_key": foreign_key,
            "comment_con": comment_con,
            "comment_user": comment_user,
            "comment_id": comment_id
        })
        db.session.add(comment)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def update_comment(self, comment, foreign_type, foreign_key, comment_con, comment_user, comment_id=None):
        """
        修改
        :param comment:
        :param foreign_type:
        :param foreign_key:
        :param comment_con:
        :param comment_user:
        :param comment_id:
        :return:
        """

        if not isinstance(comment, Comment):
            raise Exception("参数类型错误，不是一个Comment对象")
        comment.foreign_type = foreign_type
        comment.foreign_key = foreign_key
        comment.comment_con = comment_con
        comment.comment_user = comment_user
        comment.comment_id = comment_id
        db.session.add(comment)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

    def delete_comment(self, comment_id_list=None):
        """
        删除
        :param essay_id_list:
        :return:
        """

        if not comment_id_list:
            raise Exception("评论id不能为None")
        if not isinstance(comment_id_list, list):
            raise Exception("评论id参数不是一个列表")
        essay_list = Comment.query.filter(Comment.id in comment_id_list)
        for comment in essay_list:
            comment.is_delete = True
            db.session.add(comment)
        try:
            db.session.commit()
        except Exception as ex:
            raise Exception(ex)

