#!/usr/bin/env python3
# 获取接口
from urllib import request
import time
import json


class Basic:
    def __init__(self):
        self.__accessToken = 'Uy5V6KV64z-6hJ6DbBiYSNIGjONlzQ8IayVtmPW2oFyhWy5fs6bxoGEtgn1Ryg6DVbFDt8boVRiQwmh8Y6' \
                             'CH2HVlXnlA0gBJezRoQoRCFEMAPbbh3rkMmAtw1sbQQK0bUNFaAHAIBT'
        self.__leftTime = 0

    def __real_get_access_token(self):
        appId = "wxfb36a8b09d2149b1"
        appSecret = "b63b6e5c971570f9f95bdd5473c92a9d"

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                   "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = request.urlopen(postUrl)
        res = urlResp.read().decode('utf-8')
        urlResp = json.loads(res)

        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while (True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()