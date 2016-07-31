#!/usr/bin/env python
#encoding=utf-8
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

#import bcrypt
import concurrent.futures
import MySQLdb
import os.path
import re
import subprocess
import torndb
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
from BaseHandler import BaseHandler
from datetime import datetime

from tornado.options import define, options

class TradeHandler(BaseHandler):
    def get(self):
        trade = self.db.get("SELECT * FROM trades ORDER BY deliver_time DESC LIMIT 1")
        result = {}
        for key in trade:
            #result[key.encode('utf-8')] = str(trade[key.encode('utf-8')]).encode('utf-8')
            if isinstance(trade[key], datetime):
                result[key] = trade[key].strftime("%Y-%m-%d %H:%M:%S")
                continue
            result[key] = trade[key]

        result['test'] = 'HelloWorld'
        #self.write(result)
        self.render("daily_business.html")
