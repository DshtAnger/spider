#!/usr/bin python
#coding:utf-8
# @Date    : 2016-03-28
# @Author  : DshtAnger
from bs4 import BeautifulSoup
import requests,pymongo,time

client = pymongo.MongoClient('127.0.0.1', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']

headers={"Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        'Connection':'keep-alive',
        'Host':'bj.ganji.com',
        "Cache-Control":"max-age=0",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"}
cookie = {"Cookie":"statistics_clientid=me; citydomain=bj; ganji_uuid=9638516748377369954232; ganji_xuuid=1c5d2bbd-c733-4069-899b-c65ec0b3f328.1459257912990; GANJISESSID=d8c452ac4f5e73b954070b403e553637; crawler_uuid=145986903342398415133356; _gj_txz=MTQ1OTg2OTYzOTpQYLO5ne6cEq+UXiJjGovck38KQw==; __utmt=1; statistics_clientid=me; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A75567610463%7D; __utma=32156897.1301605670.1459257906.1459861170.1459869044.5; __utmb=32156897.16.10.1459869044; __utmc=32156897; __utmz=32156897.1459869044.5.4.utmcsr=ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/sorry/confirm.php"}

#爬取某个类目下所有帖子链接
def crawl_card_list(cate_url):
    current_cate_name = cate_url.split("/")[-2]
    for page_index in xrange(1,10000):
        #组装当前类目下带页码的某一具体页
        url = cate_url + str(page_index)
        #检测页面是否为验证机器人的页面
        is_robot = True
        while is_robot:
            #进入此处表明当前页面是验证机器人页面，不断等待并尝试重新访问该类目该页的链接
            time.sleep(2)          
            req = requests.get(url,headers=headers,cookies=cookie)
            soup = BeautifulSoup(req.content,"lxml")            
            is_robot = len(soup.select(".error-tips1"))!=0        
        #当前未触发机器人验证,或已通过循环等待通过了机器人严重
        #检测该页面是否存在跳页按钮,作为是否结束翻页的条件
        pageLink = soup.select("ul.pageLink.clearfix")
        if len(pageLink)!=0:
            #存在跳页按钮,获取该页的所有链接
            for link in soup.select("a.ft-tit"):
                #过滤zhuanzhuan之类的链接
                if "bj.ganji.com" in link.get("href"):
                    url_list.insert_one({'url':link.get("href")})
                else:
                    continue
        else:
            break
    print("[*]%s crawl finished! last pageindex is %d"%(current_cate_name,page_index))

def crawl_item_info(card_url):
        is_robot = True
        while is_robot:
            #进入此处表明当前页面是验证机器人页面，不断等待并尝试重新访问该类目该页的链接
            time.sleep(1)          
            req = requests.get(card_url,headers=headers,cookies=cookie)
            soup = BeautifulSoup(req.content,"lxml")            
            is_robot = len(soup.select(".error-tips1"))!=0        
        #当前未触发机器人验证,或已经历循环等待通过了机器人验证
        #爬取具体页面信息
        title = soup.select(".title-name")[0].get_text()
        pub_date = '2016.'+soup.select(".pr-5")[0].get_text().strip().split(" ")[0].replace("-",".")
        cates = [i.get_text() for i in soup.select("div.crumbs.clearfix > a")[1:]]
        url = req.url
        price = int(soup.select(".f-type")[0].get_text())
        temp = soup.select(".det-infor > li:nth-of-type(3) > a")[1:]
        area = [i.get_text() for i in temp] if temp!=[] else ['不明']
        try:
            temp = soup.select(".second-det-infor > li:nth-of-type(1)")[0].get_text(strip=True)[5:]
        except IndexError:
            temp = []
        finally:
            look = temp if temp!=[] else '-'
        data = {"title":title,"pub_date":pub_date,"cates":cates,"area":area,
                "url":url,"price":price,"look":look}
        item_info.insert_one(data)