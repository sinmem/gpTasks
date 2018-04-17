'''
实现百度图片爬取
'''
import requests
# from bs4 import BeautifulSoup
import os
import re


def getHtml(url):
    headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'image.baidu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'UTF-8'
    return requests.get(url, headers=headers).text


def setParam(keyWorlds, np):
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+keyWorlds+'&pn='+np+'&ct=&ic=0&lm=-1&width=0&height=0'
    return url


def saveFile(page, localPath, keyWorlds):
    if not os.path.exists(localPath):
        os.mkdir(localPath)
    # 通过正则表达式取得每张图片的原图链接
    tempList = re.findall(r'"objURL":"(.*?)",', page)
    item = 0
    error = 0
    for imgurl in tempList:
        try:
            pic = requests.get(imgurl, timeout=20)
        except Exception as e:
            # tempList[item] = "[失败]图片"+str(item+1)+"+下载失败"+str(tempList[item])
            print(e)
            error += 1
            continue
        item += 1
        fileName = localPath+keyWorlds+'_'+str(item+1)+'.png'
        with open(fileName.encode('utf-8'), "wb") as ftemp:
            ftemp .write(pic.content)
        print(imgurl)
    print("success:%-4d   failed:%-4d" % ((item), error))
    print("------------------------------------------\n该页下载完成\n")


keyWorlds = str(input("请输入爬取图片的关键字:"))
np = int(input("请输入需要下载的页数(一页大概60张):"))
localPath = "F:/SWrk/gpTasks/download/"
for i in range(0, np):
    print("开始下载第%d页\n------------------------------------------\n" % (i+1))
    saveFile(getHtml(setParam(keyWorlds, str(i))), localPath, keyWorlds)
