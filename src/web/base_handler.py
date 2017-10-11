#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web


# from py_class import user


# TODO add user detection here
# @userapp.tornado.config(app_id=user.USER_APP_ID)
class BaseHandler(tornado.web.RequestHandler):
    _debug = None
    _manual = None
    _lore = None
    _db = None
    _global_arg = {}

    def initialize(self, **kwargs):
        self._lore = kwargs.get("lore")
        self._global_arg = {
            "debug": kwargs.get("debug"),
            "use_internet_static": kwargs.get("use_internet_static"),
            "db": self._db,
        }

    def get_current_user(self):
        pass
        # TODO not work
        # return self._db.get_user(_uuid=self.get_secure_cookie("user"))
