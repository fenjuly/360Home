#!/usr/bin/env python
# coding=utf-8

import json

from base import *
from tornado import escape
from tornado.escape import utf8

class BlogHandler(BaseHandler):
    def get(self):
        for blog in self.blog_model.get_latest_blogs():
            del blog["_id"]
            self.write(blog)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        title = ''
        content = ''
        user_id = ''
        type = 0
        if "title" in data:
            title = data["title"]
        if "content" in data:
            content = data["content"]
        if "type" in data:
            type = data["type"]
        if "user_id" in data:
            user_id = data["user_id"]


        blog_info = {
            "title": title,
            "content": content,
            "user_id": user_id,
            "type": type,
            "created": time.strftime('%Y-%m-%d %H:%M:%S'),
            "modified": time.strftime('%Y-%m-%d %H:%M:%S')
        }

        blog_id = self.blog_model.add_new_blog(blog_info)

        if blog_id:
            print(blog_id)
            success_info = {}
            success_info['success'] = u'发布成功'
            self.write(success_info)
            return
        else:
            error_info = {}
            error_info['error'] = u'发布出错,数据库插入出错'
            self.write(error_info)
            return