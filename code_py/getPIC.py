#!/usr/bin/env python3

import requests, urllib
import os
from bs4 import BeautifulSoup


def getHTMLText(url):
    '''
    Get the code of the url page
    :param url:
    :return: string
    '''
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36"
        }
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "link exception"


def getText(url, selector):
    '''
    通过url和selector爬取指定内容，返回list
    :param url:
    :param selector:
    :return: list
    '''
    soup = BeautifulSoup(getHTMLText(url), 'lxml')
    data = soup.select(selector)
    return data


def getPic(url, path, filename=''):
    '''
    通过url，获取图片
    :param url:
    :param pathfile:
    :return:
    '''
    if filename == '':
        filename = os.path.basename(url)
    urllib.request.urlretrieve(url, path + '/' + filename)

if __name__ == '__main__':
    url = "https://22xyz.xyz"
    savePath = "/opt/a"
    # 每个板块的url
    baseurl = url + "/pic/4/"
    # 网页页数
    startnum = 1
    stopnum = 329
    if stopnum >= startnum:
        if startnum == 1:
            urlList = [baseurl + "index_" + str(i) + ".html" for i in range(2, stopnum + 1)]
            urlList.insert(0, baseurl)
        else:
            urlList = [baseurl + "index_" + str(i) + ".html" for i in range(startnum, stopnum + 1)]
    else:
        print("开始页码大于结束页码")
        exit()
    # 图片列表
    ls = "body > div > div > div.wrap.mt20 > div > ul"
    # 图片seletor
    imgs = "body > div > div > div.content > p"
    imgUrlList = []
    for suburl in urlList:
        data = getText(suburl, ls)
        if data == []:
        	break
        for i in data:
            for j in i.find_all('a'):
                h = j.get('href')
                imgUrlList.append(url + h)
    print("共爬取{}个链接".format(len(imgUrlList)))
    # 开始的链接序号，第一个默认为1
    startindex = 1
    for index in range(startindex, len(imgUrlList)):
        data = getText(imgUrlList[index - 1], imgs)
        print("从第{}个链接开始，链接：{}".format(index, imgUrlList[index - 1]))
        imgnum = 1
        for i in data:
            for j in i.find_all('img'):
                imgurl = j.get('src')
                getPic(imgurl, savePath, filename=str(index) + "_" + str(imgnum) + ".jpg")
                print("正在下载第{}个图片".format(imgnum))
                imgnum += 1
        print("已完成第{}个链接".format(index))

