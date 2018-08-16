# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utilFunction.py
   Description :  tool function
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 添加robustCrawl、verifyProxy、getHtmlTree
                   2018/08/16: 添加validUsefulProxy       A.L.
-------------------------------------------------
"""
import requests
import time
from lxml import etree

from package.utils.WebRequest import WebRequest


# logger = LogHandler(__name__, stream=False)


class getCurrentOutIp(object):

    @staticmethod
    def get_current_out_ip():
        """
        获取公网IP
        :param
        :return:
        """
        response = requests.get(url='http://httpbin.org/ip')
        if response.status_code == 200:
            content_str = response.content.decode('utf8')
            outer_ip = content_str.split('"')
            return outer_ip[3]
        else:
            raise Exception("httpbin挂了！")


# noinspection PyPep8Naming
def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass
            # logger.info(u"sorry, 抓取出错。错误原因:")
            # logger.info(e)

    return decorate


# noinspection PyPep8Naming
def verifyProxyFormat(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


# noinspection PyPep8Naming
def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """

    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    wr = WebRequest()

    # delay 2s for per request
    time.sleep(2)

    html = wr.get(url=url, header=header).content
    return etree.HTML(html)


def tcpConnect(proxy):
    """
    TCP 三次握手
    :param proxy:
    :return:
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


# noinspection PyPep8Naming
def validUsefulProxy(proxy):
    """
    检验代理是否是可用的高匿代理
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过10秒的代理就不要了
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200:
            response_ip = r.content.decode('utf8')
            current_out_ip = getCurrentOutIp.get_current_out_ip()
            # 如果不是高匿服务器就不要了
            if response_ip.find(current_out_ip) < 0:
                return True
            else:
                print(response_ip + "is not NG")
                return False
            # logger.info('%s is ok' % proxy)
        else:
            print("proxy {proxy} failed".format(proxy=proxies))
            return False
    except Exception as e:
        # logger.error(str(e))
        print(str(e))
        return False


def validTest(proxy):
    """
    检验代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过10秒的代理就不要了

        # r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        r = requests.get('http://ip.chinaz.com/', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200:
            print(r.content)
            print(r.content.decode('utf-8'))
    except Exception as e:
        # logger.error(str(e))
        print(str(e))
        return False


if __name__ == '__main__':
    validTest('')
