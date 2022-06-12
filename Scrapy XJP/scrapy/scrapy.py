# coding=utf-8
import concurrent
import multiprocessing
import time

from db import models
from db import db_handlers
import datetime,xmltodict,browser_cookie3,re
from bs4 import BeautifulSoup
from multiprocessing import Pool
from concurrent import futures
from functools import partial


def scrapy_XH(uLink,sWord):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko)'
                      'Chrome / 100.0.4896.127Safari / 537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    jsdataXH = {
        'keyword': sWord,
        'curPage': '1',
        'sortField': '0',
        'searchFields': '1',
        'lang': 'cn'
    }

    spiderXH= models.spiderXJP_XH(headers)
    jscontent = spiderXH.jsRequstXH(uLink,jsdataXH)
    urlXHnew = jscontent['content']['recommendation']['url'] #get the auto-redirect link from XHR of search result
    spiderXH.updateURL(urlXHnew)
    contentXH = spiderXH.requests_web()
    textXH = spiderXH.get_source_parserXH(contentXH)
    for item in textXH:
        db_handlers.save2text(sWord,item)
    print('Save to Text successfully from XINHUA',datetime.date.today())

def scrapy_XJP_RMZW(uLink,sWord):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko)'
                      'Chrome / 100.0.4896.127Safari / 537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    news = {}
    spiderRMZL = models.spiderXJP_RM(uLink,headers)
    newLinkRMZL = spiderRMZL.get_particularWebRMZL(spiderRMZL.requests_web())
    spiderRMZL.updateURL(newLinkRMZL)
    textRMZL = spiderRMZL.get_source_webRMZL(spiderRMZL.requests_web())
    for item in textRMZL:
        db_handlers.save2text(sWord, item)
    print('Save to Text successfully from RENMINZHUANWANG', datetime.date.today())

def get_house_price(url):
    cookies = {
        'rlp_lang': 'en',
        'analytics_id': '148-83b3d0a3-695d-4f53-b7ac-278a6c420489',
        '_ga': 'GA1.2.1259353374.1653349932',
        '_gid': 'GA1.2.1685415159.1653349932',
        'csrftoken': 'P2MrthSicV0kv2kH93Nuy6f1SKz4wPf6Q93Nq5HLBVe5gsHcosSQCSLbEOqfMT4X',
        'analytics_session': '40afaefa9109',
        '_gcl_au': '1.1.81388791.1653349933',
        'll-visitor-id': 'f8acaf4f-0445-46cf-8428-0f34cfbb8f9a',
        'rlp_lang': 'en',
        'll-heatmaps-selection': 'pedestrian_friendly',
        'll-commute-mode': 'car',
        'll-ls-onboarding': 'onboarding-dismissed',
        'll-discover-count': '3',
        '_gat': '1',
    }
    headers = {
        'authority': 'www.royallepage.ca',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'rlp_lang=en; analytics_id=148-83b3d0a3-695d-4f53-b7ac-278a6c420489; _ga=GA1.2.1259353374.1653349932; _gid=GA1.2.1685415159.1653349932; csrftoken=P2MrthSicV0kv2kH93Nuy6f1SKz4wPf6Q93Nq5HLBVe5gsHcosSQCSLbEOqfMT4X; analytics_session=40afaefa9109; _gcl_au=1.1.81388791.1653349933; ll-visitor-id=f8acaf4f-0445-46cf-8428-0f34cfbb8f9a; rlp_lang=en; ll-heatmaps-selection=pedestrian_friendly; ll-commute-mode=car; ll-ls-onboarding=onboarding-dismissed; ll-discover-count=3; _gat=1',
        'pragma': 'no-cache',
        'referer': 'https://www.royallepage.ca/en/search/homes/on/toronto/?search_str=Toronto%2C+ON%2C+CAN&csrfmiddlewaretoken=Bt99FyNcMwn5mQSJbxJbatgkaQzwkIhHCAqvCmCFbwBQ7gfeqWOxefMuWUqHAM6y&property_type=&house_type=&features=&listing_type=&lat=43.65352400000006&lng=-79.38390699999997&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=Toronto&method=homes&address_type=city&city_name=Toronto&prov_code=ON&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=&sortby=',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }
    spider_house = models.spider_housePrice(headers,cookies)
    spider_house.updateURL(url)
    soup = BeautifulSoup(spider_house.requests_web(),'lxml')
    text = spider_house.parser_web(soup)
    for itme in text:
        cityName = itme[0]
        db_handlers.save2text(cityName, itme)
        # convert tuple to List so that itme[4] could be changed from str to int then to be saved in SQL accordingly
        itemList = []
        for i in range(len(itme)):
            item = itme[i]
            if i == 4 and itme[4].replace(',', '').strip('$').isnumeric():
                item = int(itme[4].replace(',', '').strip('$'))
            itemList.append(item)
        db_handlers.save2sql(itemList,'canadahouseprice','david')
        # print(itme)
        print('Save to Text successfully for city %s'%cityName, datetime.date.today())

def scrapy_canada_house(cityName):
    urls = []
    url_dict = {
        'toronto': 'https://www.royallepage.ca/en/search/homes/on/toronto/?search_str=Toronto%2C+ON%2C+CAN&csrfmiddlewaretoken=Bt99FyNcMwn5mQSJbxJbatgkaQzwkIhHCAqvCmCFbwBQ7gfeqWOxefMuWUqHAM6y&property_type=&house_type=&features=&listing_type=&lat=43.65352400000006&lng=-79.38390699999997&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=Toronto&method=homes&address_type=city&city_name=Toronto&prov_code=ON&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=&sortby=',
        'ottawa': 'https://www.royallepage.ca/en/search/homes/on/ottawa/?search_str=Ottawa%2C+ON%2C+CAN&csrfmiddlewaretoken=2UrRBKA71wTnVam8VzSEm7Q3KDpq5gIi31IdyypAqw78GAJDaYX0qTmdwHgBlkx9&property_type=&house_type=&features=&listing_type=&lat=45.425226000000066&lng=-75.69996299999997&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=Ottawa&method=homes&address_type=city&city_name=Ottawa&prov_code=ON&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=&sortby=%27',
        'hamilton': 'https://www.royallepage.ca/en/search/homes/on/hamilton/?search_str=Hamilton%2C+ON%2C+CAN&csrfmiddlewaretoken=oyhqc5V46iU8xmVNpEa650wn2gjYM3PRpFyM9TKxvi8TiMiiE3fs9M2xOka927EI&property_type=&house_type=&features=&listing_type=&lat=43.255490000000066&lng=-79.87337599999995&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=Hamilton&method=homes&address_type=city&city_name=Hamilton&prov_code=ON&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=&sortby=%27',
        'vancouver': 'https://www.royallepage.ca/en/search/homes/bc/vancouver/?search_str=Vancouver%2C+BC%2C+CAN&csrfmiddlewaretoken=LYjR1kBQWLeUF2WDAd1jV66JPHfivzutM5AdY8qjlLsFqsj8PC6FZSCTBL6tLDjk&property_type=&house_type=&features=&listing_type=&lat=49.26163600000007&lng=-123.11334999999997&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=Vancouver&method=homes&address_type=city&city_name=Vancouver&prov_code=BC&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=&sortby=%27',
        'calgary': 'https://www.royallepage.ca/en/search/homes/ab/calgary/?search_str=Calgary%2C+AB%2C+CAN&csrfmiddlewaretoken=26KOFjpTXrZW2K0xOoMaWtFdQYpYRyXi3d1aC7emmrdHNan23NRw0fbnC2g97CM9&property_type=&house_type=&features=&listing_type=&lat=51.04511300000007&lng=-114.05714099999994&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=Calgary&method=homes&address_type=city&city_name=Calgary&prov_code=AB&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&archive_status=All&archive_timespan=6&keyword=&sortby=%27',
        'edmonton': 'https://www.royallepage.ca/en/search/homes/ab/edmonton/?search_str=Edmonton%2C+AB%2C+CAN&csrfmiddlewaretoken=NE02MlDJzoahXvCwigvhLEFvKDF7weCEOLhoJ9scYoo2IVZ1xFADPqbFwHwiMirv&property_type=&house_type=&features=&listing_type=&lat=53.54545000000007&lng=-113.49013999999994&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=Edmonton&method=homes&address_type=city&city_name=Edmonton&prov_code=AB&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&archive_status=All&archive_timespan=6&keyword=&sortby=%27',
        'halifax': 'https://www.royallepage.ca/en/search/homes/ns/halifax/?search_str=Halifax%2C+NS%2C+CAN&csrfmiddlewaretoken=rjQ3hK4FWFHxcXCYwZzyVMPmGpW0Qfk3sq7peyT8lFViXnZtLoEUZylwstNb6j9U&property_type=&house_type=&features=&listing_type=&lat=44.648881000000074&lng=-63.57531199999994&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=Halifax&method=homes&address_type=city&city_name=Halifax&prov_code=NS&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=&sortby=%27',
        'st-johns': 'https://www.royallepage.ca/en/search/homes/nl/st-johns/?search_str=St.+John%27s%2C+NL%2C+CAN&csrfmiddlewaretoken=bi0AbsiEwzp9JKGRMcZnmP1Lb7hZfdvWcphW8g77VzDUua3m1B4JqBxVXb8avhkN&property_type=&house_type=&features=&listing_type=&lat=47.56148500000006&lng=-52.71267499999993&upper_lat=&upper_lng=&lower_lat=&lower_lng=&bypass=&radius=&zoom=&display_type=gallery-view&travel_time=false&travel_time_min=30&travel_time_mode=drive&travel_time_congestion=&da_id=&segment_id=&tier2=False&tier2_proximity=0&address=St.+John%27s&method=homes&address_type=city&city_name=St.+John%27s&prov_code=NL&school_id=&min_price=0&max_price=5000000%2B&min_leaseprice=0&max_leaseprice=5000%2B&beds=0&baths=0&transactionType=SALE&keyword=&sortby='

    }
    print('Starting print | save %s city house price....'%cityName)
    url = url_dict.get(cityName)
    for i in range(1, 3):
        if i == 1:
            urls.append(url)
        urls.append(url[:(url.find(cityName) + len(cityName))] + '/' + str(i) + url[(url.find(cityName) + len(cityName)):])
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(get_house_price, urls)
    pool.close()
    pool.join()
    print('Done print | save %s city house price'%cityName)

def scrapy_mun(uLink):
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
    } # header for mun.online
    basePath = 'https://online.mun.ca' # for join link afterwords
    domain_name = 'online.mun.ca'
    cookieJar = browser_cookie3.load(domain_name=domain_name) # get current page cookies

    #create spider for current page cookies & update user's link
    spiderMUN = models.spider_mun(headers=headers,cookies=cookieJar)
    spiderMUN.updateURL(uLink)

    #get each module's viewContent Page Link List from user's link page
    #folderName= each module's name, used to create folder to classify files
    viewLinkList,folderName = spiderMUN.get_view_link(spiderMUN.requests_web())

    # get each download file link and file name for each viewContent page
    for vLink in viewLinkList:
        #if the vLink have data feedback, then receive it; otherwise Notify user
        if spiderMUN.get_download_link(vLink,basePath):
            fileNameList,fileLinkList = spiderMUN.get_download_link(vLink,basePath)

            # if file links on viewContent page exists, then download them.
            # each viewContent could contain >=1 files, so get them repeatedly
            if fileLinkList:
                workers = min(10,len(fileLinkList)) # create multithreads to download files
                download_file_partial = partial(spiderMUN.download_file,folderName)
                for i in range(len(fileLinkList)): # make sure fileName - fileLink: one-to-one correspondence
                    with futures.ThreadPoolExecutor(workers) as executor:
                        executor.map(download_file_partial(fileNameList[i],fileLinkList[i]))
            else:
                print('No download link! Check if you open the page you need in browser')


