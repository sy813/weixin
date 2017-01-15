#!/usr/bin/env python3
# 爬取股票和其对应代码

from urllib import request
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('stock.db')
conn.execute('''CREATE TABLE IF NOT EXISTS stock
               (CODE VARCHAR(10)  NOT NULL,
                NAME VARCHAR(10)  NOT NULL);''')

url = 'http://quote.eastmoney.com/stocklist.html'
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko)' \
             ' Version/8.0 Mobile/12A4345d Safari/600.1.4'
headers = {'User-Agent': user_agent}
req = request.Request(url=url, headers=headers)
response = request.urlopen(req)
content = response.read().decode('gbk')
soup = BeautifulSoup(content, "html.parser")
div = soup.find_all('div', 'quotebody')
lis = div[0].find_all('li')
for li in lis:
    nc = li.get_text()
    code = nc[-7:-1]
    name = nc[:-8]
    if code[0] in ['0', '3', '6']:
        conn.execute("INSERT INTO stock VALUES ('%s','%s');" % (code, name))
        conn.commit()
        print('INSERT SUCCESSED!')

conn.close()
