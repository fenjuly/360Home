#!/usr/bin/env python
# coding=utf-8
#
# Copied form https://github.com/PaulGuo/F2E.im/blob/master/application.py
# Copyright 2012 F2E.im
# Do have a faith in what you're doing.
# Make your life a story worth telling.

# cat /etc/mime.types
# application/octet-stream    crx

import sys
reload(sys)
sys.setdefaultencoding("utf8")

import os.path
import re
import memcache
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import handler.base
import handler.user

from pymongo import MongoClient
from tornado.options import define, options
from lib.loader import Loader
from lib.session import Session, SessionManager
from jinja2 import Environment, FileSystemLoader

define("port", default = 80, help = "run on the given port", type = int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            blog_title = u"Home of 360",
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = False,
            cookie_secret = "cookie_secret_code",
            login_url = "/login",
            autoescape = None,
            jinja2 = Environment(loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")), trim_blocks = True),
            reserved = ["user", "topic", "home", "setting", "forgot", "login", "logout", "register", "admin"],
        )

        handlers = [
            (r"/register", handler.user.RegisterHandler),
            (r"/u/(\w+)", handler.user.UserDetailHandler),
            (r"/edit", handler.user.UserModifyHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        conn = MongoClient("localhost", 27017)
        self.db = conn.example

        self.loader = Loader(self.db)

        self.user_model = self.loader.use("user.model")

        self.session_manager = SessionManager(settings["cookie_secret"], ["127.0.0.1:11211"], 0)

        self.mc = memcache.Client(["127.0.0.1:11211"])

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()