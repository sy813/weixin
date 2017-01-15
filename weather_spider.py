#!/usr/bin/env python3
# 根据地名爬取7天天气

from urllib import request
import sqlite3
from bs4 import BeautifulSoup


class Weather(object):
    def __init__(self, city):
        self.url = 'http://www.weather.com.cn/weather/%s.shtml'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                          '54.0.2840.99 Safari/537.36'
        self.city = city

    def run(self):
        headers = {'User-Agent':self.user_agent}
        city = self.city
        conn = sqlite3.connect('weixin.db')
        cursor = conn.execute("SELECT CODE from city WHERE NAME='%s'" % city)
        for row in cursor:
            code = row[0]
            req = request.Request(url=self.url % code, headers=headers)
            response = request.urlopen(req)
            content = response.read().decode('utf-8')
            soup = BeautifulSoup(content, "html.parser")
            ul = soup.find_all('ul', 't')
            lis = ul[0].find_all('li')
            wea = ''
            for li in lis:
                text = li.get_text().replace('\n', '')
                wea = wea + text + '\n'
            return wea
        conn.close()

if __name__ == '__main__':
    weather = Weather('无锡')
    weather.run()

