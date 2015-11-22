#!/usr/bin/env python
# coding=utf-8

import pymongo

class UserModel(object):
    def __init__(self, db):
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["example"]

    def get_user_by_uid(self, uid):
        coll = self.application.db.user
        word_doc = coll.find_one({"_id": uid})
        return word_doc