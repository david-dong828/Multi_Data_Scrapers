
import requests,json,os
from bs4 import BeautifulSoup
import xmltodict,browser_cookie3,re

# header for mun.online
headers = {
    'authority': 'online.mun.ca',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'fpestid=5xR0E-oAWvN3XfRuTSv2rLCkM5jYCOrrxLPMXDOJn_H_JwSHdnFQhXf27k4DNrYO3XzeJg; oup-cookie=1_16-1-2022; optimizelyEndUserId=oeu1642340257226r0.6277137220040656; _ga_GLF90ZEMKF=GS1.1.1642444259.2.0.1642444259.0; amp_d4783f_mun.ca=wJBpy4kJRq-MZRaK8Km4MA...1fq12p2f2.1fq12p8sl.2.0.2; _hjSessionUser_1518123=eyJpZCI6ImEwOWY4NDY3LWIxYTEtNWI2Mi04ODJlLWZkM2NiZjgyNDEyYyIsImNyZWF0ZWQiOjE2NDI4NzAzNjQ2MDUsImV4aXN0aW5nIjpmYWxzZX0=; AMCV_1B6E34B85282A0AC0A490D44%40AdobeOrg=-1124106680%7CMCIDTS%7C19016%7CMCMID%7C25462898076912503000242951517070305099%7CMCAAMLH-1643538704%7C7%7CMCAAMB-1643538704%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1642941104s%7CNONE%7CMCAID%7C309C64E80252CFD8-600019A321E637FB%7CvVersion%7C5.2.0; lastRskxRun=1642933910746; rskxRunCookie=0; rCookie=qs8j9ord06n82pq0fddz74kyr4fisf; _vwo_uuid=D6DF3B5F3E549C68B42CCFE710278C14A; _hjSessionUser_2580298=eyJpZCI6IjMyOWY3OWU5LWM5M2QtNTY2Mi1hOWU4LWYwYjM4NGJlZTE4ZiIsImNyZWF0ZWQiOjE2NDMxMzg4NDAwOTIsImV4aXN0aW5nIjp0cnVlfQ==; amp_d4783f=wJBpy4kJRq-MZRaK8Km4MA...1fqa1v9kf.1fqa1v9kg.5.0.5; amplitude_id_9f6c0bb8b82021496164c672a7dc98d6_edmmun.ca=eyJkZXZpY2VJZCI6Ijc0ZTEyZDM2LTkxYWMtNGI0OC04ZmQzLTU0MzMxZTI4NDIzOVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY0MzIwNTUxNjg2OCwibGFzdEV2ZW50VGltZSI6MTY0MzIwNTUxNjg4NCwiZXZlbnRJZCI6MTAsImlkZW50aWZ5SWQiOjMxLCJzZXF1ZW5jZU51bWJlciI6NDF9; amplitude_id_408774472b1245a7df5814f20e7484d0mun.ca=eyJkZXZpY2VJZCI6IjYzYzZjMTNiLWFhZDQtNGZkMC05OTJmLTZjMmJiMjMxZDhkMSIsInVzZXJJZCI6bnVsbCwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNjQzMjA1NTE2OTQ0LCJsYXN0RXZlbnRUaW1lIjoxNjQzMjA1NTE2OTUwLCJldmVudElkIjoxMjAsImlkZW50aWZ5SWQiOjExNSwic2VxdWVuY2VOdW1iZXIiOjIzNX0=; MAID=vItdmEvWJjbrfRJ1qwcFkg==; MACHINE_LAST_SEEN=2022-03-06T10%3A10%3A39.098-08%3A00; _hjSessionUser_1283988=eyJpZCI6ImJjNTNiZDQ1LTNmOTctNWY2My05MjY5LWI1MTFhOTE3OGE3YyIsImNyZWF0ZWQiOjE2NDY1OTAyNDcwNDgsImV4aXN0aW5nIjpmYWxzZX0=; _gid=GA1.2.74533370.1654174352; _clck=1u22byc|1|f21|0; d2lSessionVal=znj25swePqr2Nd0ghvUkHS2ux; d2lSecureSessionVal=D2NJw3PjyPxRTAHlUnfgetngM; _ga=GA1.2.447171953.1652483937; _uetsid=de55fec0e27211ec82af6d40b605e507; _uetvid=102aad40d31311eca495e9ad9e5595df; _clsk=b1xlas|1654341627403|1|1|d.clarity.ms/collect; _ga_EE64Q85813=GS1.1.1654341626.34.0.1654341629.0',
    'pragma': 'no-cache',
    'referer': 'https://online.mun.ca/d2l/home',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}

# return current page cookies
def get_cookie():
    return browser_cookie3.load(domain_name='online.mun.ca')

# return requested page source
def requests_web(url,cookieJar):
    try:
        content = requests.get(url,headers=headers,cookies=cookieJar)
        if content.status_code == 200:
            content.encoding = 'utf-8'
            return content.text
    except requests.RequestException as e:
        print(e)
        return None

# download files into 'C:\downloads' folder
def download_file(fileName,fileLink):
    # BASE_PATH =os.path.dirname(__file__)
    downloadPath = 'C:\downloads'
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)
    USER_PATH = os.path.join(downloadPath,fileName)

    try:
        myfile = requests.get(fileLink)
        if myfile.status_code == 200:
            open(USER_PATH,'wb').write(myfile.content)
            print('Download %s successfully'%fileName)
        else:
            print(myfile.status_code,'Link is invalid')
    except Exception as e:
        print(e,'Download files failed')

# func: return viewContent page link from initial page source
# @content: page source, used to be anaylized by BeautifulSoup,(from requests.get)
def get_view_link(content):
    viewLinkList = []
    soup = BeautifulSoup(content,'lxml')
    # replace invalid characters in file/folder name to _
    folderName = re.sub('[\\/?*<>:"|]+','_',soup.find('title').string)

    # viewContent Page Link is included in tag (class_='d2l-link'), but needed to be filtered out(by keyword 'viewContent')
    for item in soup.find_all(class_='d2l-link'):
        if 'viewContent' in item.get('href'):
            viewLinkList.append('https://online.mun.ca'+(item.get('href')))
    return viewLinkList,folderName

# func: return video name List, video download link List
# soup: viewContent page source
# @cookieJar: current page cookie
# @basePath: used to join new link later with relative links in tag
def get_download_link_video(soup,cookieJar,basePath):
    videoNameList = []
    videoLinkList = []
    invalidKeywords = ['/','\\',':','<','>','*','?','"','|']
    try:
        # video name and download link are under tag with class = 'd2l-fileviewer-text'
        item = soup.find(class_='d2l-fileviewer-text')
        # if file exists,process; otherwise notify users
        if item:
            viewLink = basePath + item.get('data-location') # get real video page URL with join relative link
            soup = BeautifulSoup(requests_web(viewLink,cookieJar),'lxml') # get real video page source
            # video name is under tag<h2>, video link under tag<a>
            # using if-else to filter out empty data page
            if soup.find_all('h2') and soup.find_all('a'):
                for videoName in soup.find_all('h2'):
                    # remove invalid characters in filename and add into video Name list
                    videoNameList.append(re.sub('[\\/?*<>:"|]+','-',videoName.string)+'.mp4')
                for video in soup.find_all('a'):
                    baseVideoLink = '/'.join(viewLink.rsplit('/')[:-2]) # get main URL of current real video page
                    # relative link of download file is in <href>
                    # get absolute URL by joining main URL of real video page and the relative link of download file
                    videoLinkList.append(baseVideoLink+video.get('href').lstrip('.'))
                return videoNameList, videoLinkList
            else:
                print('No download link, check if you open the page you need in browser')
                return None
        else:
            print('No file under <class=d2l-fileviewer-text> of viewContent page')
            return None
    except Exception as e:
        print('get video download link error',e)
        return None

# func: return file name List, file download link List
# @url: viewContent page link, get from function get_view_link()
# @cookieJar: current page cookie
# @basePath: used to join new link later with relative links in tag
def get_download_link(url,cookieJar,basePath):
    try:
        content = requests.get(url, cookies=cookieJar, headers=headers)
        if content.status_code == 200:
            content.encoding = 'utf-8'
            soup = BeautifulSoup(content.text,'lxml')
            item = (soup.find(class_="d2l-fileviewer-pdf-pdfjs")) # pdf files are under tag with class="d2l-fileviewer-pdf-pdfjs"
            # in case there's no pdf file, another kind of files - Video
            if not item:
                # invoke func to get video link with viewContent page source
                # if data return, unpack the Name list and Link list and return; otherwise notify users
                if get_download_link_video(soup,cookieJar,basePath):
                    videoNameList,videoLinkList = get_download_link_video(soup,cookieJar,basePath)
                    return videoNameList, videoLinkList
                else:
                    print('No data feedback from Page! Skip')
                    return None
            # to set empty Lists for pdf file name and links
            pdfNameList = []
            pdfLinkList = []
            pdfNameList.append(item.get('data-title')+'.pdf')
            pdfLinkList.append(basePath+item.get('data-location'))
            return pdfNameList,pdfLinkList
    except requests.RequestException as e:
        return None

def main():
    # url = 'https://online.mun.ca/d2l/le/content/473399/Home'
    # url = 'https://online.mun.ca/d2l/le/content/452700/Home'
    url = input('Copy the URL 0f the Course Content Page where you can find the PDFs or Videos: ').strip()
    basePath = 'https://online.mun.ca'
    cookieJar = get_cookie()
    content = requests_web(url,cookieJar)

    viewLinkList,folderName = get_view_link(content)

    for vLink in viewLinkList:
        if get_download_link(vLink,cookieJar,basePath):
            fileNameList,fileLinkList = get_download_link(vLink,cookieJar,basePath)
            if fileLinkList:
                for i in range(len(fileLinkList)):
                    download_file(fileNameList[i],fileLinkList[i])
            else:
                print('No download link!')


if __name__ == '__main__':
    main()

