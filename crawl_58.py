#!/usr/bin/env python
#coding:utf8
from bs4 import BeautifulSoup
import requests,time
headers={"Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        'Connection':'keep-alive',
        "Cache-Control":"max-age=0",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        }
        
def get_detailsPage(homepage_url):    
    html = requests.get(homepage_url,headers=headers)
    soup = BeautifulSoup(html.text,"lxml")
    #而正常商品原始链接里直接就已经包含.shtml字样，以此作为从主页面筛选正常商品详情页链接的条件
    detailsPage_urls = [i.get("href") for i in soup.select("td.t > a.t") if ".shtml" in i.get("href")]
    return detailsPage_urls

def get_views(url):
    id = __import__("re").search("/(\d*?)x\.shtml",url).group(1)
    api = "http://jst1.58.com/counter?infoid={}".format(id)
    views = requests.get(api,headers=headers).text.split("=")[-1]
    return views

def get_detailsInfo(detailsPage_url):
    wb_data = requests.get(detailsPage_url,headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text,"lxml")
    detailInfo = dict(
        category = soup.select("div.breadCrumb.f12 > span")[-1].get_text(),
        title = soup.select("div.col_sub.mainTitle > h1")[0].get_text(),
        date = soup.select("li.time")[0].get_text(),
        price = soup.select("span.price.c_f50")[0].get_text()[:-1],
        quality = soup.select("div.col_sub.sumary > ul > li:nth-of-type(2) > div.su_con > span")[0].get_text().strip(),
        area = "".join(list(soup.select("span.c_25d")[0].stripped_strings)) if soup.find_all('span','c_25d') else None,
        views = get_views(detailsPage_url)
        )
    for key,value in detailInfo.items():
        print "%s:%s"%(key,value)
    print "----------------------------------------------"
    return detailInfo

def get_commodityInfo(startPage=1,endPage=1):
    all_data = []
    for pageIndex in xrange(startPage,endPage+1):
        homepage = "http://bj.58.com/pbdn/0/pn{}".format(str(pageIndex))
        detailsPage_urls = get_detailsPage(homepage)
        onepage_data = [get_detailsInfo(detailsPage_url) for detailsPage_url in detailsPage_urls]
        all_data.append(onepage_data)
    return all_data

if __name__ == '__main__':
    get_commodityInfo(1,100)