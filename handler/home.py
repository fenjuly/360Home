#!/usr/bin/env python
# coding=utf-8

from base import *

class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")