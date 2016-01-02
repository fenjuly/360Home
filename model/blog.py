#!/usr/bin/env python
# coding=utf-8

class BlogModel(object):
    def __init__(self, db):
        self.db = db
        self.coll = self.db.blog

    def get_latest_blogs(self):
        blogs = self.coll.find(limit=5)
        return blogs

    def add_new_blog(self, blog_info):
        return self.coll.insert(blog_info)
