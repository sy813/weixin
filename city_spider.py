#!/usr/bin/env python3
# 获取城市代码，并存储在sqllite数据库中

from urllib import request
import sqlite3

conn = sqlite3.connect('weixin.db')
conn.execute('''CREATE TABLE IF NOT EXISTS city
               (CODE VARCHAR(10)  PRIMARY KEY NOT NULL,
                NAME VARCHAR(20)  NOT NULL);''')

url1 = 'http://m.weather.com.cn/data5/city.xml'
url2 = 'http://m.weather.com.cn/data5/city%s.xml'

user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko)' \
             ' Version/8.0 Mobile/12A4345d Safari/600.1.4'
headers = {'User-Agent': user_agent}

req = request.Request(url1, headers=headers)
response = request.urlopen(req)
province = response.read().decode('utf-8').split(',')

for pro in province:
    req2 = request.Request(url2 % str(pro[0:2]), headers=headers)
    response2 = request.urlopen(req2)
    city = response2.read().decode('utf-8').split(',')
    for ci in city:
        req3 = request.Request(url2 % str(ci[0:4]), headers=headers)
        response3 = request.urlopen(req3)
        county = response3.read().decode('utf-8').split(',')
        for c in county:
            req4 = request.Request(url2 % str(c[0:6]), headers=headers)
            response4 = request.urlopen(req4)
            c_code = response4.read().decode('utf-8')[7:]
            c_name = c[7:]
            conn.execute("INSERT INTO city VALUES (%s,'%s');" % (c_code, c_name))
            conn.commit()
            print('COUNTY INSERT SUCCESSED!')
        print('CITY INSERT SUCCESSED!')
    print('PROVINCE INSERT SUCCESSED!')
print('ALL INSERT SUCCESSED!')

conn.close()

