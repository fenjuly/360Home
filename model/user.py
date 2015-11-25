#!/usr/bin/env python
# coding=utf-8


class UserModel(object):
    def __init__(self, db):
        self.db = db
        self.coll = self.db.user

    def get_user_by_uid(self, uid):
        user = self.coll.find_one({"_id": uid})
        return user

    def get_user_by_qq(self, qq):
        user = self.coll.find_one({"qq": qq})
        return user

    def get_user_by_wechat(self, wechat):
        user = self.coll.find_one({"wechat": wechat})
        return user

    def get_user_by_username(self, username):
        user = self.coll.find_one({"username": username})
        return user

    def add_new_user(self, user_info):
        return self.coll.insert(user_info)

    def update_user(self, username, user_info):
        print({"$set": user_info})
        return self.coll.update({"username": username}, {"$set": user_info})

