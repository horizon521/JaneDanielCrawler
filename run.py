# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
from requests.exceptions import RequestException
import os
from hashlib import md5
from multiprocessing import Pool

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Referer':'http://jandan.net/ooxx',
    'Referer':'http://jandan.net/ooxx',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Cookie':'__cfduid=d0f8f8aef303ad3b55cd071a426e7a59c1504854664; _ga=GA1.2.986719823.1501079288; _gid=GA1.2.1585289570.1506061387',
}

def get_page(url):
    response=requests.get(url,headers=headers)
    try:
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
    doc=pq(html)
    links=doc('.commentlist .row .text p a')
    for link in links:
        image_url='http:'+pq(link).attr('href')
        yield image_url

def download_image(url):
    response=requests.get(url,headers=headers)
    try:
        if response.status_code==200:
            return response.content
        return None
    except RequestException:
        return None

def save_image(content):
    path_name='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(path_name):
        with open(path_name,'wb') as f:
            f.write(content)
            f.close()

def main(page):
    print('===============开始抓取第%r页==============='%page)
    url = 'http://jandan.net/ooxx/page-{}#comments'.format(page)
    html=get_page(url)
    if html:
        urls=parse_page(html)
        for url in urls:
            print('正在下载:%r'%url)
            content=download_image(url)
            save_image(content)

if __name__=='__main__':
    pool=Pool()
    pool.map(main,[page*1 for page in range(1,137)])
