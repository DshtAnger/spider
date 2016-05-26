#!/usr/bin python
#coding:utf-8
# @Date    : 2016-03-28
# @Author  : DshtAnger
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from channel import crawl_cates_list
from get_page import crawl_card_list,crawl_item_info,url_list,item_info

all_urls = set([item['url'] for item in url_list.find()])
finished_urls = set([item['url'] for item in item_info.find()])
rest_urls = list(all_urls - finished_urls)
#57273

if __name__ == '__main__':
    channel_list = crawl_cates_list()

    #约半小时爬取57343个链接
    # pool = Pool(processes=4)
    # pool.map(crawl_card_list,channel_list)
    # pool.join()
    # pool.close()

    #不中断地一秒一个大约要爬15个小时
    pool = Pool(processes=4)
    pool.map(crawl_item_info,rest_urls)
    pool.join()
    pool.close()