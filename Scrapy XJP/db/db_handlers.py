# coding=utf-8
import datetime,json,os,requests
from conf import setting
from interface import user_interface
from db import save2mysql

def save2text(sWord,text):
    # to make path of folder in db folder,if not there then create it
    USER_PATH = os.path.join(setting.DB_PATH, sWord)
    if not os.path.exists(USER_PATH):
        os.mkdir(USER_PATH)
    # using today as file name, then create file absolute path
    fName = str(datetime.date.today())+'.txt'
    filePath = os.path.join(USER_PATH,fName)
    with open(filePath, 'a', encoding='utf-8') as f:
        f.write(json.dumps(text, ensure_ascii=False) + '\n')
    print('Save Text file %s successfully to folder %s'%(fName,sWord))

def save2sql(item,tableName,database):
    try:
        db,cursion = save2mysql.connectDB(database)
        save2mysql.insertDataToTable(db, cursion, item, tableName)
        print('Save to MySQL successfully')
    except Exception as e:
        print(e,'Save to MySQL failed')

def saveMUNfile(folderName,fileName, myfile):
    # to make path of folder in db folder,if not there then create it
    USER_PATH = os.path.join(setting.DB_PATH,folderName)
    if not os.path.exists(USER_PATH):
        os.mkdir(USER_PATH)
    # to create absolute file path in folder created before
    filePath = os.path.join(USER_PATH,fileName)
    # write file(pdf/video) into designed file place
    with open(filePath, 'wb') as f:
        f.write(myfile.content)
    print('Download %s successfully' % fileName)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendmail(clientMail,mSubject,mBody):
    try:
        username = 'infopush.xxx@gmail.com'
        password = 'xxxxxxx'
        mail_from = 'infopush.xxx@gmail.com'
        mail_bcc = clientMail
        mail_subject = mSubject
        mail_body = mBody

        mimemsg = MIMEMultipart()
        mimemsg['From'] = mail_from
        # mimemsg['To'] = mail_to
        mimemsg['Bcc'] = mail_bcc
        mimemsg['Subject'] = mail_subject
        mimemsg.attach(MIMEText(mail_body,'plain'))

        connection = smtplib.SMTP(host='smtp.gmail.com',port=587)
        connection.starttls()
        connection.login(username,password)
        connection.sendmail(mail_from,mail_bcc,mimemsg.as_string())
        connection.quit()
        print('Send mail successfully',datetime.date.today())
    except Exception as e:
        print(e)

def checkFile(leaderName):
    FOLD_PATH = os.path.join(setting.DB_PATH,leaderName)
    if not os.path.exists(FOLD_PATH):
        return 'No this leaders data.You can search it thru option 2'
    if not os.path.exists(os.path.join(FOLD_PATH,str(datetime.date.today())+'.txt')):
        print('The data is not latest! Now Scrapy latest data! ')
        if leaderName == '习近平':
            user_interface.spider_top_china_XH()
            user_interface.spider_XJP_RM()
        else:
            user_interface.spider_top_china_XH()
        print('Now data is ready! Sending Now...')
    return os.path.join(FOLD_PATH,str(datetime.date.today())+'.txt')

def sortNewsNyield(news):
    keys = sorted(news.keys(),reverse=True)
    for key in keys:
        yield key,news[key]

def sortTextFile(filePath):
    news = {}
    with open(filePath,'r',encoding='utf-8') as f:
        for line in f.readlines():
            line =line.strip().strip('[').strip(']').split(',')
            news[json.loads(line[0])]= json.loads((line[1]))+' | '+json.loads(line[2])
    return news
