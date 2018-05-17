import scrapy
import re
from bs4 import BeautifulSoup


class GoodsSpider(scrapy.Spider):
    name = "goods"
    start_urls = [
        'https://search.jd.com/Search?keyword=手机&enc=utf-8&wq=手机&pvid=e8be70061dd340f9b79a795001bfde06'
    ]

    def parse(self, response):
        fileName = response.url.split('/')[-2]
        html = response.body
        
        soup = BeautifulSoup(html)
        goodsList = soup.select(".gl-i-wrap")
        print('\n\n-------------1---------------\n')
        print(type(html))
        List = []
        for item in goodsList:
            tempinfo = re.findall(r'>(.*?)<', str(item.select_one(".p-name.p-name-type-2 em"))) 
            tempprice = re.findall(r'[0-9]*\.[0-9]*', str(item.select_one(".p-price i")))
            if len(tempinfo[0]) <= 1:
                tempinfo[0] = tempinfo[1]
            if len(tempprice) == 0:
                continue
            List.append([tempinfo[0], tempprice[0]])
        print(List)
        with open(fileName, 'w', encoding='utf-8') as f:
            for item in List:
                f.writelines(str(item)+'\n')
