# coding=utf-8
import datetime

from scrapy import scrapy
from db import db_handlers
from conf import setting

def general_spider():
    pass

def spider_top_china_XH():
    leaderName = input('Please type a Chinese leader Name: ').strip()
    uLink = 'http://so.news.cn/getNews'  # real XINHUA search page
    scrapy.scrapy_XH(uLink,leaderName)

def spider_top_china_RM():
    print('stay tuned')
    pass

def spider_XJP_RM():
    leaderName = '习近平'
    urlRM = 'http://www.people.com.cn/'
    scrapy.scrapy_XJP_RMZW(urlRM,leaderName)

def sendMail():
    mailAddress = input('Type your email: ').strip()
    leaderName = input('Please type the Chinese leader Name whose news you want to send: ' ).strip()
    mSubject = '%s 领导人动态跟随'%leaderName +'--' + str(datetime.date.today())
    filePath = db_handlers.checkFile(leaderName)
    text = db_handlers.sortTextFile(filePath)
    sortedText = db_handlers.sortNewsNyield(text)
    mailBody = ''
    for item in sortedText:
        mailBody += (item[0] + ' | ' + item[1] ) + '\n'
    # print('mailBody',mailBody)
    db_handlers.sendmail(mailAddress,mSubject,mailBody)

def spider_HousePrice_Canada():
    while True:
        print(
            '''
            ========= Welcome to Quary Canada Real Estate Price ========
                    1. Toronto
                    2. Ottawa
                    3. Hamilton
                    4. Vancouver
                    5. Calgary 
                    6. Edmonton
                    7. Halifax
                    8. St.John's
                    9. Exit
            =================== END ===================
            '''
        )

        city_dict = {
            '1':'toronto',
            '2':'ottawa',
            '3':'hamilton',
            '4':'vancouver',
            '5':'calgary',
            '6':'edmonton',
            '7':'halifax',
            '8':'st-johns',
            '9':'exit'
        }
        choice = input('Please select the number: ').strip()
        if choice not in city_dict:
            print('Wrong Number! Please select a new one')
            continue
        if choice == '9':
            break
        scrapy.scrapy_canada_house(city_dict.get(choice))

def spider_MUNonLine():
    # get user's input and invoke scrapy_mun function
    urlInput = input('Copy the URL 0f the Course Content Page where you can find the PDFs or Videos: ').strip()
    scrapy.scrapy_mun(urlInput)