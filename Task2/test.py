'''
实现百度图片爬取
'''
import requests
from bs4 import BeautifulSoup


def getHtml(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
        + 'like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'UTF-8'
    html = res.text
    return html


def setParam(param):
    temp = str(param)
    url = 'https://image.baidu.com/search/index?tn=baiduimage&word=' + temp
    return url


keyWorlds = str(input("请输入爬取图片的关键字:"))
soup = BeautifulSoup(getHtml(setParam(keyWorlds)), 'html.parser')
print(soup)
