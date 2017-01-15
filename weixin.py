# encoding: utf-8
from flask import Flask, request, make_response
import hashlib, time
from xml.etree import cElementTree as ET
import qiubai_spider
import weather_spider
import stock_spider

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'weixin'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        list = [token, timestamp, nonce]
        list.sort()
        list1 = ''.join(list)
        hashcode1 = hashlib.sha1(list1.encode('utf-8')).hexdigest()
        if hashcode1 == signature:
            return make_response(echostr)
        return 'Hello World!' + hashcode1 + '____' + signature

    else:
        xml_rec = ET.fromstring(request.data)
        touser = xml_rec.find('ToUserName').text
        fromuser = xml_rec.find('FromUserName').text
        createtime = xml_rec.find('CreateTime').text
        msgtype = xml_rec.find('MsgType').text
        if msgtype == 'event':
            event = xml_rec.find('Event').text
            if event == 'subscribe':
                msgcontent = '走过路过不要再错过...'
            else:
                msgcontent = 'bye...'
            rec = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
                '''
            response = make_response(rec % (fromuser, touser, int(time.time()), msgcontent))
            response.content_type = 'application/xml'
            return response
        if msgtype == 'text':
            content = xml_rec.find('Content').text
            print(content)
            rec = '''
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    </xml>
                    '''
            if content == '你好':
                reply = '祝你更好！'
            elif content == '笑话':
                reply = qiubai_spider.Spider().run()
            elif content[0:2] == '天气':
                city = content[2:]
                print('city', city)
                rep = weather_spider.Weather(city).run()
                if rep:
                    reply = rep
                else:
                    reply = '请输入正确的地名'
            elif content[0:2] == '股票':
                nc = content[2:]
                try:
                    ncc = int(nc)
                    rep = stock_spider.Stock(code=nc).run()
                    if rep:
                        reply = rep
                    else:
                        reply = '请输入完整的股票代码'
                except:
                    rep = stock_spider.Stock(name=nc).run()
                    if rep:
                        reply = rep
                    else:
                        reply = '请输入完整的股票名字'

            else:
                reply = '更多功能，敬请期待...'
            response = make_response(rec % (fromuser, touser, int(time.time()), reply))
            response.content_type = 'application/xml'
            return response

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
