# coding=utf-8
import requests
from bs4 import BeautifulSoup
from db import sendMail


class spiderXJP:
    def __init__(self,url=None,headers=None,cookies=None,json=None,verify = False):
        self._url = url
        self._headers = headers
        self._cookies = cookies
        self._json = json

    def updateURL(self,url):
        self._url = url

    def requests_web(self):
        try:
            content = requests.get(self._url,headers=self._headers)
            # content = requests.get(url)
            if content.status_code == 200:
                content.encoding = 'utf-8'
                return content.text
        except requests.RequestException as e:
            print(e)
            return None

    def jsRequstXH(self,endPoint,data):
        try:
            # here post and get can have same result
            response = requests.post(endPoint,params=data,headers=self._headers)
            if response.status_code == 200:
                print('200')
                # return the link of XiJinping page from XHR since the search result will redirect to a new particular page
                return (response.json()) #json() to get dict back
        except Exception:
            print('200 code but no result')

    def get_source_parserXH(self,content):
        soup = BeautifulSoup(content,'lxml')
        news = {}
        n = 1
        for fList in soup.find_all(class_='evt-wrap'):
            for item in fList.find_all('li'):
                eventDate = item.get('data-pt')+'('+str(n)+')'
                eventTitle = item.find('a').text
                eventLink = item.find('a').get('href')
                news[eventDate] = [eventTitle,eventLink]
                n += 1    # sort date in descending order
        keys = sorted(news.keys(), reverse=True)
        for key in keys:
            yield key,news[key][0],news[key][1]

    def get_particularWebRMZL(self,content):
        soup = BeautifulSoup(content, 'lxml')
        return (soup.find(class_="zt_banner fl").find('a').get('href'))

    def parser_webRMZL(self,content):
        soup = BeautifulSoup(content, 'lxml')
        news = {}
        n = 1
        for i in range(1, 3):
            for item in soup.find_all('ul')[i]:
                if item.find('i') != -1:
                    eTitle = item.find('span').text
                    eDate = item.find('i').text.removesuffix('】').split('【')[1] + '(' + str(n) + ')'
                    eUrl = self._url + item.find('a').get('href')
                    news[eDate] = [eTitle, eUrl]
                    n += 1
        keys = sorted(news.keys(), reverse=True)
        for key in keys:
            yield key, news[key][0], news[key][1]

def printText(text):
        for item in text:
            print(item)

def sortNewsNyield(news):
    keys =sorted(news.keys(),reverse=True)
    for key in keys:
        yield key,news[key][0],news[key][1]

def send2mail(text,cMail,sWord):
    mailBody = ''
    for item in text:
        mailBody += (item[0]+' | '+item[1]+' | '+item[2])+'\n'
    print('mailbody',mailBody)
    sendMail.sendmail(cMail, sWord + '动态追随', mailBody)

def main():
    sWord = input('type the Top leader\'s name in chinese: ' )
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko)'
                      'Chrome / 100.0.4896.127Safari / 537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    dataXH = {
        'keyword': sWord,
        'curPage': '1',
        'sortField': '0',
        'searchFields': '1',
        'lang': 'cn'
    }
    news = {}
    endPointXH = 'http://so.news.cn/getNews'  # real XINHUA search page
    spiderXH = spiderXJP(headers)
    jsContent = spiderXH.jsRequstXH(endPointXH,dataXH) #get the auto-redirect link from XHR of search result
    urlXHnew= jsContent['content']['recommendation']['url']
    spiderXH.updateURL(urlXHnew)
    contentXH = spiderXH.requests_web()
    textXH = spiderXH.get_source_parserXH(contentXH)
    for item in textXH:
        news[item[0]] = [item[1], item[2]]

    urlRM = 'http://www.people.com.cn/'
    spiderRMZL = spiderXJP(urlRM,headers)
    newLinkRMZL = spiderRMZL.get_particularWebRMZL(spiderRMZL.requests_web())
    spiderRMZL.updateURL(newLinkRMZL)
    textRMZL = spiderRMZL.parser_webRMZL(spiderRMZL.requests_web())
    for item in textRMZL:
        news[item[0]] = [item[1],item[2]]

    text = sortNewsNyield(news)
    # printText(text)
    # cMail = 'okmyfriendship@163.com'
    cMail = ['dongh@mun.ca','david.dong828@gmail.com']
    send2mail(text,cMail,sWord)

if __name__ == '__main__':
    main()
