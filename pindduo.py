# coding=utf-8
import os
import re
import time
import json
import random
import jsonpath
import requests
import linecache
from lxml import etree
# from collections import OrderedDict
import sys
# import imp
# imp.reload(sys)
# sys.setdefaultencoding('utf-8')


class Comment(object):
    def __init__(self):
        # self.headers = ""
        # 代理服务器
        proxyHost = "n10.t.16yun.cn"
        proxyPort = "6442"

        # 代理隧道验证信息
        proxyUser = "16SBYYUY"
        proxyPass = "658666"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        print(proxyMeta)
        self.proxy = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        self.srequest = requests.Session()

    def change_ua(self):
        tunnel = random.randint(1, 1036)
        # print tunnel
        user_agent = linecache.getline('1000ua-pc.log', tunnel)
        user_agent = user_agent.strip().replace('\n', '').replace('\r', '')
        # print user_agent
        # 请求头携带Host会导致无法访问数据，有时候可以
        self.headers = {
            'X-PDD-QUERIES': "width=1080&height=2240&net=1&brand=HUAWEI&model=CLT-AL00&osv=8.1.0&appv=4.15.0&pl=2",
            'ETag': "NHCVKydR",
            'Referer': "Android",
            'Content-Type': "application/json;charset=UTF-8",
            'User-Agent': "android Mozilla/5.0 (Linux; Android 8.1.0; CLT-AL00 Build/HUAWEICLT-AL00; wv)            AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36  phh_android_version/4.15.0 phh_android_build/228842 phh_android_channel/qihu360",
            # 'Host': "apiv4.yangkeduo.com",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Cookie': "api_uid=rBUBtVthJ0VRS2kPRnXiAg==; JSESSIONID=3EEE6B7FC7343B16B11951B925FED920",
            'Cache-Control': "no-cache",
            'Postman-Token': "618890b9-2316-e323-494a-bb1af29958e1"
        }

    def comment_json(self):
        self.change_ua()
        #抓取到的地址，单次爬取
        # url = 'http://apiv4.yangkeduo.com/v3/operation/1281/groups?opt_type=1&offset=0&sort_type=DEFAULT&size=50&pdduid= '
        # url = 'http://apiv3.yangkeduo.com/operation/14/groups?opt_type=1&size=100&offset=0&flip=&pdduid=0'
        # url = 'http://apiv3.yangkeduo.com/reviews/9193910/list?picture=1&page=1&size=20'
        # url = "http://apiv3.yangkeduo.com/reviews/9193910/list?picture=1&page=12&size=20&pdduid=0"
        i = 0
        mylis = []
        # url = 'http://apiv4.yangkeduo.com/v3/operation/14/groups?opt_type=1&offset=2100&sort_type=DEFAULT&size=50&pdduid='
        #翻页
        while i < 100000:
            url = 'http://apiv4.yangkeduo.com/v3/operation/14/groups?opt_type=1&offset='+str(i) +'&sort_type=DEFAULT&size=50&pdduid='
            i += 50
            mylis.append(url)
        #print(mylis)
        # url = 'http://apiv4.yangkeduo.com/v3/operation/14/groups?opt_type=1&offset=50&sort_type=DEFAULT&size=50&flip=60%3B10%3B0%3B50&pdduid= '
        for i in mylis:
        #遇到错误或空，跳过
            try:
                res = requests.get(i, headers=self.headers, proxies=self.proxy).text
                # print(res)
                json_data = json.loads(res)
                # json_obj = jsonpath.jsonpath(json_data, expr='$..data[*].comment')
                # time_obj = jsonpath.jsonpath(json_data, expr='$..data[*].time')

                for li in json_data['goods_list']:
                    name = li['goods_name']
                    print(name)
                    price = li['group']['price']
                    counts = li['cnt']
                    #保存成txt格式
                    with open(r'C:\Users\qijianshuma\Desktop\pinyifu3.txt', 'a') as f:
                        f.write(name + ',')
                        f.write(str(price)+',')
                        f.write(str(counts)+'\n')
                    f.close()
            except:
                pass
            time.sleep(3)
                # print(name,price,counts)



if __name__ == '__main__':
    c = Comment()
    c.comment_json()

