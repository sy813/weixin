# encoding: utf-8
from flask import Flask, request, make_response
import hashlib

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
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
