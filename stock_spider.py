#!/usr/bin/env python3
# 根据股票名字或代码爬取股价

from urllib import request
import sqlite3


class Stock(object):
    def __init__(self, code=None, name=None):
        self.url = 'http://hq.sinajs.cn/list=%s'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                          '54.0.2840.99 Safari/537.36'
        self.code = code
        self.name = name

    def run(self):
        headers = {'User-Agent':self.user_agent}
        code = self.code
        if code:
            if code[0] == '6':
                code = 'sh' + code
            else:
                code = 'sz' + code
            req = request.Request(url=self.url % code, headers=headers)
            response = request.urlopen(req)
            content = response.read().decode('gbk')
            lis = content[21:].strip().split(',')
            increase = round(100 * (float(lis[3]) - float(lis[2])) / float(lis[2]), 2)
            reply = lis[0] + ':' + '现价' + lis[3] + '涨幅' + str(increase) + '%' + '\n'
            reply += '今日开盘价' + lis[1] + '昨日收盘价' + lis[2] + '\n'
            reply += '今日最高价' + lis[4] + '今日最低价' + lis[5]
            return reply
        name = self.name
        if name:
            conn = sqlite3.connect('stock.db')
            cursor = conn.execute("SELECT CODE from stock WHERE NAME LIKE '%s'" % name)
            for row in cursor:
                code = row[0]
                if code[0] == '6':
                    code = 'sh' + code
                else:
                    code = 'sz' + code
                req = request.Request(url=self.url % code, headers=headers)
                response = request.urlopen(req)
                content = response.read().decode('gbk')
                lis = content[21:].strip().split(',')
                increase = round(100*(float(lis[3])-float(lis[2]))/float(lis[2]), 2)
                reply = lis[0] + ':' + '现价' + lis[3] + '涨幅' + str(increase) + '%' + '\n'
                reply += '今日开盘价' + lis[1] + '昨日收盘价' + lis[2] + '\n'
                reply += '今日最高价' + lis[4] + '今日最低价' + lis[5]
                return reply

if __name__ == '__main__':
    stock = Stock('', '万科A')
    stock.run()
