#!/usr/bin python
#coding:utf-8
# @Date    : 2016-03-28
# @Author  : DshtAnger
import requests
from bs4 import BeautifulSoup

def crawl_cates_list():
    #爬取20个类目链接
    data = []
    url = "http://bj.ganji.com/wu/"
    req = requests.get(url)
    soup = BeautifulSoup(req.content,"lxml")
    for i in soup.select("dl.fenlei > dt > a"):
        data.append("http://bj.ganji.com"+i.get("href")+"a1o")
    return data