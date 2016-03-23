#-*-coding:utf8-*- 
import re
import sys
import os
import urllib
from bs4 import BeautifulSoup
import requests
from lxml import etree
from threading import *
#设置屏幕锁
screenLock = Semaphore(value=1)

def get_pageNum(url,cookie):
  html = requests.get(url,headers = header,cookies = cookie).content
  selector = etree.HTML(html)
  pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
  return pageNum

def crawling_text():
  result = ""
  word_count = 1
  #文字爬取
  selector = etree.HTML(lxml)
  content = selector.xpath('//span[@class="ctt"]')
  for each in content:
    text = each.xpath('string(.)')
    if word_count == 4:
      text = "%d :"%(word_count-3) +text+"\n\n"
    else :
      text = text+"\n\n"
    result = result + text
    word_count += 1
  print "[+]第%d页文字爬取完毕\n"%page

def crawling_image(pageIndex,cookie):  
  #设置爬取的页码
  url = 'http://weibo.cn/u/%d?filter=1&page='%user_id + str(pageIndex)
  #获取lxml页面
  lxml = requests.get(url,headers = header,cookies = cookie).content
  #图片链接爬取
    #soup = BeautifulSoup(lxml, "lxml")
    #urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
  selector = etree.HTML(lxml)
  urllist = selector.xpath('//div[@class="c"]/div[2]/a[2]/@href')
  #设置本地保存路径
  image_savePath=os.getcwd()+'/weibo_image_%d'%user_id
  if os.path.exists(image_savePath) is False:
    os.mkdir(image_savePath)
  #开始下载每一个链接，保存到本地路径
  for imgurl in urllist:
    #取得跳转到的真实url
    real_url = requests.get(imgurl,headers = header,cookies = cookie).url
    #用url中的文件名命名下载的图片
    filename = re.search(r"(?<=/)[\d\w]*(?=.jpg)",real_url).group()+".jpg"
    savePath = image_savePath + "/" + filename
    #f = open(image_savePath+"/"+filename,"wb")
    try:
      urllib.urlretrieve(urllib.urlopen(real_url).geturl(),savePath)
      #content = requests.get(real_url,headers = header,cookies = cookie).text
      #f.write(content)
    except:
      screenLock.acquire()
      print "[+]第%d页某图片下载失败!"%pageIndex  
      screenLock.release()    
    finally:
      #f.close()
      pass
  screenLock.acquire()
  print "[*]第%d页下载完成"%pageIndex
  screenLock.release()

user_id = 1789505151
cookie = {"Cookie":"_T_WM=7cf37eb360836119ae09c9c81ef4597f; H5_INDEX=3; H5_INDEX_TITLE=__Nul1; APP_TIPS_HIDE=1; WEIBOCN_WM=5091_0026; SUB=_2A2576-iLDeRxGeVL71YW9yfMzzuIHXVZF4jDrDV6PUJbrdBeLWbZkW1LHet-s-2ORGfGtqSsk1lMeQc2KGGJFQ..; SUHB=0S7CkHUMB4bwEK; SSOLoginState=1458542811"}
header = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"}
url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id
pageNum = get_pageNum(url,cookie)
for page in xrange(1,pageNum+1):
  t = Thread(target=crawling_image,args=(page,cookie))
  t.start()