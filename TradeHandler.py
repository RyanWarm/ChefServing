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
        date = self.get_argument("date", None)
        mode = self.get_argument("mode", None)

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        selected_date = datetime.strptime(date, "%Y-%m-%d")

        if mode is None:
            mode = 0

        trade = self.db.get("SELECT * FROM business WHERE date='" + date + "'")

        #result['test'] = 'HelloWorld'
        #self.write(result)

        if trade is not None:
            trade.youzan_0_average = 0 if (0 == trade.youzan_0_num) else trade.youzan_0_payment / trade.youzan_0_num
            trade.youzan_1_average = 0 if (0 == trade.youzan_1_num) else trade.youzan_1_payment / trade.youzan_1_num
            trade.youzan_2_average = 0 if (0 == trade.youzan_2_num) else trade.youzan_2_payment / trade.youzan_2_num
            trade.weixin_0_average = 0 if (0 == trade.weixin_0_num) else trade.weixin_0_payment / trade.weixin_0_num
            trade.weixin_1_average = 0 if (0 == trade.weixin_1_num) else trade.weixin_1_payment / trade.weixin_1_num
            trade.weixin_2_average = 0 if (0 == trade.weixin_2_num) else trade.weixin_2_payment / trade.weixin_2_num
            trade.cash_0_average = 0 if (0 == trade.cash_0_num) else trade.cash_0_payment / trade.cash_0_num
            trade.cash_1_average = 0 if (0 == trade.cash_1_num) else trade.cash_1_payment / trade.cash_1_num
            trade.cash_2_average = 0 if (0 == trade.cash_2_num) else trade.cash_2_payment / trade.cash_2_num

            trade.total_0_num = trade.youzan_0_num + trade.weixin_0_num + trade.cash_0_num
            trade.total_0_sum = trade.youzan_0_sum + trade.weixin_0_sum + trade.cash_0_sum
            trade.total_0_discount = trade.youzan_0_discount + trade.weixin_0_discount + trade.cash_0_discount
            trade.total_0_payment = trade.youzan_0_payment + trade.weixin_0_payment + trade.cash_0_payment
            trade.total_1_num = trade.youzan_1_num + trade.weixin_1_num + trade.cash_1_num
            trade.total_1_sum = trade.youzan_1_sum + trade.weixin_1_sum + trade.cash_1_sum
            trade.total_1_discount = trade.youzan_1_discount + trade.weixin_1_discount + trade.cash_1_discount
            trade.total_1_payment = trade.youzan_1_payment + trade.weixin_1_payment + trade.cash_1_payment
            trade.total_2_num = trade.youzan_2_num + trade.weixin_2_num + trade.cash_2_num
            trade.total_2_sum = trade.youzan_2_sum + trade.weixin_2_sum + trade.cash_2_sum
            trade.total_2_discount = trade.youzan_2_discount + trade.weixin_2_discount + trade.cash_2_discount
            trade.total_2_payment = trade.youzan_2_payment + trade.weixin_2_payment + trade.cash_2_payment

            trade.total_0_average = 0 if (0 == trade.total_0_num) else trade.total_0_payment / trade.total_0_num
            trade.total_1_average = 0 if (0 == trade.total_1_num) else trade.total_1_payment / trade.total_1_num
            trade.total_2_average = 0 if (0 == trade.total_2_num) else trade.total_2_payment / trade.total_2_num

            trade.daily_in_num = trade.total_0_num + trade.total_1_num + trade.total_2_num
            trade.daily_in_sum = trade.total_0_sum + trade.total_1_sum + trade.total_2_sum
            trade.daily_in_discount = trade.total_0_discount + trade.total_1_discount + trade.total_2_discount
            trade.daily_in_payment = trade.total_0_payment + trade.total_1_payment + trade.total_2_payment
            trade.daily_in_average = 0 if (0 == trade.daily_in_num) else trade.daily_in_payment / trade.daily_in_num

            trade.deliver_0_total = trade.deliver_0_num * trade.deliver_0_single * trade.deliver_0_time
            trade.deliver_1_total = trade.deliver_1_num * trade.deliver_1_single * trade.deliver_1_time
            trade.deliver_2_total = trade.deliver_2_num * trade.deliver_2_single * trade.deliver_2_time

            trade.out_total = trade.deliver_0_total + trade.deliver_1_total + trade.deliver_2_total

            trade.profit = trade.daily_in_payment - trade.materials - trade.out_total

        print "mode: " + str(mode)
        self.render("daily_business.html", date=date, trade=trade, mode=mode, month=selected_date.month, day=selected_date.day)




