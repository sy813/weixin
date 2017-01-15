#!/usr/bin/env python3
# 爬取糗事百科文字笑话

from urllib import request
import re, random


class Spider(object):
    def __init__(self):
        self.url = 'http://www.qiushibaike.com/text/page/%s'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                          '54.0.2840.99 Safari/537.36'

    def get_page(self, page):
        headers = {'User-Agent':self.user_agent}
        req = request.Request(url=self.url % str(page), headers=headers)
        response = request.urlopen(req)
        return response.read().decode('utf-8')

    def analysis(self, content):
        pattern = re.compile('<div class="content">(.*?)</', re.S)
        return re.findall(pattern, content)

    def run(self):
        try:
            content = self.get_page(random.choice(range(1, 35)))
            items = self.analysis(content)
            # 随机返回一个笑话
            return random.choice(items).strip().replace('<br/>', '').replace('<span>', '')
        except request.HTTPError as e:
            print(e)
        except request.URLError as e:
            print(e)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    spider = Spider()
    spider.run()
