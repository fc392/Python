import requests
from urllib.parse import urlencode
import json
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import pymongo
from jiepai.config import *

client=pymongo.MongoClient(mongo_url)
db=client[mongo_db]

def get_page_index(offset,keyword):
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1
    }
    url='https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None

def parse_page_index(html):
    data=json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求详细页失败',url)
        return None

def parse_page_detail(html,url):
    soup=BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text()
    image_pattern=re.compile('gallery:(.*),.*siblingList',re.S)
    result=re.search(image_pattern,html)
    if result:
        data=json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            images=[item.get('url') for item in sub_images]
            return{
                'title':title,
                'url':url,
                'images':images
            }

def save_to_mongo(result):
    if db[mongo_table].insert(result):
        print('Sucess')
        return True
    return False

def main():
    html1=get_page_index(0,'街拍')
    for url in parse_page_index(html1):
        html2=get_page_detail(url)
        if html2:
            result=parse_page_detail(html2,url)
            if result is None:
                continue
            else:
                save_to_mongo(result)

if __name__== '__main__':
    main()