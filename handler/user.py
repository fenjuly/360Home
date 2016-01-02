#!/usr/bin/env python
# coding=utf-8

import uuid
import hashlib
import StringIO
import time
import json
import re
import urllib2
import urllib
import tornado.web

from base import *

def do_login(self, user_id):
    user_info = self.user_model.get_user_by_uid(user_id)
    user_id = user_info["_id"]
    self.session["uid"] = user_id
    self.session["username"] = user_info["username"]
    self.session["qq"] = user_info["qq"]
    self.session["wechat"] = user_info["wechat"]
    self.session["password"] = user_info["password"]
    self.session.save()
    self.set_secure_cookie("user", str(user_id))

def do_logout(self):
    # destroy sessions
    self.session["uid"] = None
    self.session["username"] = None
    self.session["qq"] = None
    self.session["wechat"] = None
    self.session["password"] = None
    self.session.save()

    # destroy cookies
    self.clear_cookie("user")

class RegisterHandler(BaseHandler):
    def get(self, input):
        self.write(input)
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        response = {}
        username = ''
        password = ''
        motto = ''
        wechat = ''
        qq = ''
        name = ''
        if "username" in data:
            username = data["username"]
        if "password" in data:
            password = data["password"]
        if "motto" in data:
            motto = data["motto"]
        if "wechat" in data:
            wechat = data["wechat"]
        if "qq" in data:
            qq = data["qq"]
        if "name" in data:
            name = data["name"]

        if (username and password):
            is_exist = self.user_model.get_user_by_username(username)
            if is_exist:
                response['error'] = u'用户已经存在'
                self.get(response)
                return
        if (username == None or password == None):
            response['error'] = u'缺少用户名或密码'
            self.get(response)
            return

        if (username == '' or len(username) < 6):
            response['error'] = u'用户名长度不能小于6'
            self.get(response)
            return
        elif password == '' or len(password) < 6:
            response['error'] = u'密码长度不能小于6'
            self.get(response)
            return

        user_info = {
            "username": username,
            "password": password,
            "qq": qq,
            "motto": motto,
            "name": name,
            "wechat": wechat,
            "type": 0,
            "state": '',
            "avatar": '',
            "blogs": {},
            "created": time.strftime('%Y-%m-%d %H:%M:%S'),
            "modified": time.strftime('%Y-%m-%d %H:%M:%S')
        }

        user_id = self.user_model.add_new_user(user_info)

        if user_id:
            print(user_id)
            do_login(self, user_id)
            success_info = {}
            success_info['success'] = u'注册成功'
            self.get(success_info)
            return
        else:
            error_info = {}
            error_info['error'] = u'注册出错,数据库插入出错'
            self.get(error_info)
            return

class UserDetailHandler(BaseHandler):

    def get(self, input):
        if input:
            user = self.user_model.get_user_by_username(input)
            if user:
                del user["_id"]
                self.write(user)

class UserModifyHandler(BaseHandler):

    def get(self, input):
        if input:
            self.write(input)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        response = {}
        username = None
        password = None
        motto = None
        wechat = None
        qq = None
        name = None
        if "username" in data:
            username = data["username"]
        if "password" in data:
            password = data["password"]
        if "motto" in data:
            motto = data["motto"]
        if "wechat" in data:
            wechat = data["wechat"]
        if "qq" in data:
            qq = data["qq"]
        if "name" in data:
            name = data["name"]

        if(username):
            user_info = self.user_model.get_user_by_username(username)
            if user_info == None:
                response['error'] = u'用户不存在'
                self.get(response)
                return
            else:
                if password != None:
                    if (password == '' or len(password) < 6):
                        response['error'] = u'密码长度不能小于6'
                        self.get(response)
                        return
                    user_info["password"] = password
                if qq != None:
                    user_info["qq"] = qq
                if motto != None:
                    user_info["motto"] = motto
                if wechat != None:
                    user_info["wechat"] = wechat
                if name != None:
                    user_info["name"] = name

                user_info["modified"] = time.strftime('%Y-%m-%d %H:%M:%S')
                is_success = self.user_model.update_user(username, user_info)
                if is_success["updatedExisting"]:
                    response['success'] = u'修改用户信息成功'
                    self.get(response)
                else:
                    response['error'] = u'修改用户信息失败'
                    self.get(response)
                return
