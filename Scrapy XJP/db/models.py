# coding=utf-8
import multiprocessing

import requests,re
from bs4 import BeautifulSoup
from db import db_handlers


class spider:
    def __init__(self,url=None,headers=None,cookies=None,json=None):
        self._url = url
        self._headers = headers
        self._cookies = cookies
        self._json = json

    def updateURL(self,url):
        self._url = url

    def requests_web(self):
        try:
            content = requests.get(self._url,headers=self._headers,cookies=self._cookies)
            # content = requests.get(url)
            if content.status_code == 200:
                content.encoding = 'utf-8'
                return content.text
        except requests.RequestException as e:
            print(e)
            return None

class spiderXJP_XH(spider):
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

class spiderXJP_RM(spider):
    def get_particularWebRMZL(self,content):
        soup = BeautifulSoup(content, 'lxml')
        # return the link to the particular page of XJP
        return (soup.find(class_="zt_banner fl").find('a').get('href'))

    def get_source_webRMZL(self,content):
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

class spider_housePrice(spider):
    def parser_web(self,soup):
        for fList in soup.find_all(class_='card card--listing-card js-listing js-property-details'):
            if len(fList.find(class_='listing-meta listing-meta--small').find_all('span')) == 2:
                houseID = fList.get('data-id')
                houseLink = fList.find(class_='card__media').find('a').get('href')
                houseAddress = fList.find(class_='b-lazy').get('alt')
                houseType = fList.find(class_='listing-meta listing-meta--small').find('span').text
                houseSizeOld = fList.find(class_='listing-meta listing-meta--small').find_all('span')[1].text.strip()
                houseSize = ''.join(houseSizeOld.split())
                housePrice = fList.find(class_='currency').find_previous('span').text.strip()
                houseCity = houseLink.split('/')[6]
                yield (houseCity,houseID, houseType, houseSize, housePrice, houseAddress, houseLink)

class spider_mun(spider):
    # func: return viewContent page link from initial page source
    # @content: page source, used to be anaylized by BeautifulSoup,(from requests.get)
    def get_view_link(self,content):
        try:
            viewLinkList = []
            soup = BeautifulSoup(content, 'lxml')
            # replace invalid characters in file/folder name to _
            folderName = re.sub('[/\:*?"<>|]', '_', soup.find('title').string)

            # viewContent Page Link is included in tag (class_='d2l-link'), but needed to be filtered out(by keyword 'viewContent')
            for item in soup.find_all(class_='d2l-link'):
                if 'viewContent' in item.get('href'):
                    viewLinkList.append('https://online.mun.ca' + (item.get('href')))
            return viewLinkList,folderName
        except Exception as e:
            print(e,'Get empty viewContent link')

    # func: return file name List, file download link List
    # @url: viewContent page link, get from function get_view_link()
    # @basePath: used to join new link later with relative links in tag
    def get_download_link(self,url, basePath):
        try:
            self.updateURL(url)
            content = self.requests_web()  # get viewContent page source

            soup = BeautifulSoup(content, 'lxml')
            item = (soup.find(class_="d2l-fileviewer-pdf-pdfjs")) # pdf files are under tag with class="d2l-fileviewer-pdf-pdfjs"
            # in case there's no pdf file, another kind of files - Video
            if not item:
                # invoke func to get video link with viewContent page source
                # if data return, unpack the Name list and Link list and return; otherwise notify users
                if self.get_download_link_video(soup, basePath):
                    videoNameList, videoLinkList = self.get_download_link_video(soup, basePath)
                    return videoNameList, videoLinkList
                else:
                    print('No data feedback from Page! Skip')
                    return None
            # to set empty Lists for pdf file name and links
            pdfNameList = []
            pdfLinkList = []
            pdfNameList.append(item.get('data-title') + '.pdf')
            pdfLinkList.append(basePath + item.get('data-location'))
            return pdfNameList, pdfLinkList
        except requests.RequestException as e:
            print(e,'Get Blank download link ')
            return None

    # func: return video name List, video download link List
    # soup: viewContent page source
    # @basePath: used to join new link later with relative links in tag
    def get_download_link_video(self,soup, basePath):
        videoNameList = []
        videoLinkList = []
        try:
            # video name and download link are under tag with class = 'd2l-fileviewer-text'
            item = soup.find(class_='d2l-fileviewer-text')
            # if file exists,process; otherwise notify users
            if item:
                viewLink = basePath + item.get('data-location') # get real video page URL with join relative link
                self.updateURL(viewLink)
                soup = BeautifulSoup(self.requests_web(), 'lxml') # get real video page source
                # video name is under tag<h2>, video link under tag<a>
                # using if-else to filter out empty data page
                if soup.find_all('h2') and soup.find_all('a'):
                    for videoName in soup.find_all('h2'):
                        videoNameList.append(re.sub('[\\/?*<>:"|]+', '-',
                                            videoName.string) + '.mp4')  # remove invalid characters in filename
                    for video in soup.find_all('a'):
                        baseVideoLink = '/'.join(viewLink.rsplit('/')[:-2]) # get main URL of current real video page
                        # relative link of download file is in <href>
                        # get absolute URL by joining main URL of real video page and the relative link of download file
                        videoLinkList.append(baseVideoLink + video.get('href').lstrip('.'))
                    return videoNameList, videoLinkList
                else:
                    print('No download link, check if you open the page you need in browser')
                    return None
            else:
                print('No file under <class=d2l-fileviewer-text> of viewContent page')
                return None
        except Exception as e:
            print('get video download link error', e)
            return None

    # func: get download file then invoke func saveMUNfile() to save
    # @folderName: valid folder name
    # @fileName: valid file name
    # @fileLink: absolute file download link
    def download_file(self,folderName,fileName, fileLink):
        try:
            myfile = requests.get(fileLink)
            if myfile.status_code == 200:
                db_handlers.saveMUNfile(folderName,fileName, myfile)
            else:
                print(myfile.status_code, 'Link is invalid')
        except Exception as e:
            print(e, 'Download files failed')