# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main.py
   Description :  运行主函数
   Author :       JHao
   date：          2017/4/1
-------------------------------------------------
   Change Activity:
                   2017/4/1:
-------------------------------------------------
"""
__author__ = 'JHao'

from multiprocessing import Process

# sys.path.append('../')

from package.api.ProxyApi import run as proxy_api_run
from package.schedule.ProxyValidSchedule import run as valid_run
from package.schedule.ProxyRefreshSchedule import run as refresh_run


def run():
    p_list = list()
    p1 = Process(target=proxy_api_run, name='ProxyApiRun')
    p_list.append(p1)
    p2 = Process(target=valid_run, name='ValidRun')
    p_list.append(p2)
    p3 = Process(target=refresh_run, name='RefreshRun')
    p_list.append(p3)

    for p in p_list:
        p.daemon = True
        p.start()
    for p in p_list:
        p.join()


if __name__ == '__main__':
    run()
