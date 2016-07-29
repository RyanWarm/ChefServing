#!/usr/bin/env python
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
import BaseHandler

from tornado.options import define, options

define("port", default=8080, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="chef database host")
define("mysql_database", default="chef", help="chef database name")
define("mysql_user", default="root", help="chef database user")
define("mysql_password", default="chef2015L", help="chef database password")

class TradeHandler(BaseHandler):
    def get(self):
        trade = self.db.get("SELECT * FROM trades ORDER BY deliver_time DESC LIMIT 1")
        result = {}
        for key in trade:
            result[key] = trade[key]
        self.write(result)
