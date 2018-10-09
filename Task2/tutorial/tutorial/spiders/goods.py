import scrapy
import re
from bs4 import BeautifulSoup


class GoodsSpider(scrapy.Spider):
    # 设置spider名字
    name = "goods"
    # 设置爬取链接
    start_urls = [
        'https://search.jd.com/Search?keyword=手机&enc=utf-8&wq=手机&pvid=e8be70061dd340f9b79a795001bfde06'
    ]
    # 解析内容
    def parse(self, response):
        # 获取到"search.jd"这个字符串
        fileName = response.url.split('/')[-2]
        html = response.body
        # 通过soup选择器选择到.gl-i-wrap类(商品类)
        soup = BeautifulSoup(html)
        goodsList = soup.select(".gl-i-wrap")
        print('\n\n-------------1---------------\n')
        print(type(html))
        List = []
        for item in goodsList:
            # 正则解析到商品简介和商品价格
            tempinfo = re.findall(r'>(.*?)<', str(item.select_one(".p-name.p-name-type-2 em"))) 
            tempprice = re.findall(r'[0-9]*\.[0-9]*', str(item.select_one(".p-price i")))
            if len(tempinfo[0]) <= 1:
                tempinfo[0] = tempinfo[1]
            if len(tempprice) == 0:
                continue
            # 将解析内容存到list中
            List.append([tempinfo[0], tempprice[0]])
        print(List)
        # 保存内容
        with open(fileName, 'w', encoding='utf-8') as f:
            for item in List:
                f.writelines(str(item)+'\n')
