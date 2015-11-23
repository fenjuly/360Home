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
    user_id = user_info["uid"]
    self.session["uid"] = user_id
    self.session["username"] = user_info["username"]
    self.session["email"] = user_info["email"]
    self.session["password"] = user_info["password"]
    self.session.save()
    self.set_secure_cookie("user", str(user_id))

def do_logout(self):
    # destroy sessions
    self.session["uid"] = None
    self.session["username"] = None
    self.session["email"] = None
    self.session["password"] = None
    self.session.save()

    # destroy cookies
    self.clear_cookie("user")

class RegisterHandler(BaseHandler):
    def get(self, input):
        self.write(input)
    def post(self):
        response = {}
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if (username != None and password != None):
            is_exist = self.user_model.get_user_by_username(username)
            if is_exist:
                response['error'] = u'用户已经存在'
                self.get(response)
                return

        user_info = {
            "username": self.get_argument('username', ''),
            "qq": self.get_argument('qq', ''),
            "motto": self.get_argument('motto', ''),
            "name": self.get_argument('name', ''),
            "wechat": self.get_argument('wechat', ''),
            "type": 0,
            "state": self.get_argument('state', ''),
            "avatar": '',
            "blogs": {},
            "created": time.strftime('%Y-%m-%d %H:%M:%S')
        }

        user_id = self.user_model.add_new_user(user_info)

        if user_id:
            print(user_id)
            self.get("success")
            return
        else:
            self.get('add error')
            return


