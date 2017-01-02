from flask import Flask, request, make_response
import hashlib

app = Flask(__name__)

'''
1）将token、timestamp、nonce三个参数进行字典序排序
2）将三个参数字符串拼接成一个字符串进行sha1加密
3）开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
'''


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'weixin'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamo', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s).encode('utf-8')
        if hashlib.sha1(s).hexdigest() == signature:
            return make_response(echostr)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
