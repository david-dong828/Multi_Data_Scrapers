# coding=utf-8
import datetime,json,os,requests
from conf import setting
from interface import user_interface
from db import save2mysql
from db import matplot_handlers

# save @text as .txt with Today's date as name into the folder named @sWord that's a subfolder of db
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

# save @item into tableName@ in @database
def save2sql(item,tableName,database):
    try:
        db,cursion = save2mysql.connectDB(database) # conncect @database
        #invoke insertDataToTable() to save into MySQL
        save2mysql.insertDataToTable(db, cursion, item, tableName)
        print('Save to MySQL successfully')
    except Exception as e:
        print(e,'Save to MySQL failed')

# draw charts: each chart contains one of (min/max/avg/median) for all cities
# @city_dict: a dictionary of all cities
def drawHousingPricechart(city_dict):
    # create empty lists for city,average/min/max/median price of all cities
    x_city,avgPrice_city, maxPrcie_city, minPrice_city, medianPrice_city = [], [], [], [],[]
    # create a dict to combine price type and price type list
    city_price_dict ={
        'avg':avgPrice_city,'max':maxPrcie_city,
        'min':minPrice_city,'median':medianPrice_city
    }
    db, cursion = save2mysql.connectDB('david') # invoke func to connect MySql 'david' database
    # set the loop only in cities since city_dict has more than cities
    for i in range(1,len(city_dict)-2+1):
        # add cities in List
        x_city.append(city_dict.get(str(i)))
        # get 4 types of price of the city then add them into according List
        for item in ['avg','max','min','median']:
            data = save2mysql.queryColumnStatic(db, cursion, item, 'canadahouseprice', 'housePrice', 'city',
                                                city_dict.get(str(i)))
            city_price_dict.get(item).append(data[0][0])
    # invoke chart drawing func to draw bar charts
    for priceType in city_price_dict.keys():
        matplot_handlers.bar_draw(x_city,city_price_dict.get(priceType),priceType,'EACH CITY %s HOUSE PRICE'%priceType)

# save @myfile with @fileName into @folderName
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

# send email to @clientMail with @mSubject and content @mBody
def sendmail(clientMail,mSubject,mBody):
    try:
        username = 'infopush.auto@gmail.com' #sent mail user name
        password = 'rqlepdhohratpdmy' #sent mail password(it's not normal password)
        mail_from = 'infopush.auto@gmail.com' #sent mail user name
        mail_bcc = clientMail # it can be 'bcc' or 'cc' or 'to'
        mail_subject = mSubject # mail subject
        mail_body = mBody # mail content

        mimemsg = MIMEMultipart() # invoke MIMEMultipart() to process Sending
        mimemsg['From'] = mail_from
        # mimemsg['To'] = mail_to
        mimemsg['Bcc'] = mail_bcc # it can be 'Bcc' or 'Cc' or 'To'
        mimemsg['Subject'] = mail_subject # mail subject
        mimemsg.attach(MIMEText(mail_body,'plain')) # mail content attached as plain format

        connection = smtplib.SMTP(host='smtp.gmail.com',port=587) #connect mail server
        connection.starttls()
        connection.login(username,password) # login server
        connection.sendmail(mail_from,mail_bcc,mimemsg.as_string()) # send mail
        connection.quit() # disconnect server after sending
        print('Send mail successfully',datetime.date.today())
    except Exception as e:
        print(e)

# return the path of  the latest file of @leaderName
def checkFile(leaderName):
    FOLD_PATH = os.path.join(setting.DB_PATH,leaderName)
    # if the @leaderName folder doesnt exist, then suggest user to scrapy data thru option 2 on Menu
    if not os.path.exists(FOLD_PATH):
        return 'No this leaders data.You can search it thru option 2'
    # if @leaderName folder exists but the file is not latest, then automatically scrapy data
    if not os.path.exists(os.path.join(FOLD_PATH,str(datetime.date.today())+'.txt')):
        print('The data is not latest! Now Scrapy latest data! ')
        if leaderName == '习近平':  # if @leaderName='习近平' then invoke those 2 funcs to scrapy from XINHUA and RINMIN nets
            user_interface.spider_top_china_XH()
            user_interface.spider_XJP_RM()
        else:  # if @leaderName is not '习近平' then invoke 1 func to scrapy from XINHUA
            user_interface.spider_top_china_XH()
        print('Now data is ready! Sending Now...')
    return os.path.join(FOLD_PATH,str(datetime.date.today())+'.txt')

# yield data(tuple) after sorting the @news(dict format)
def sortNewsNyield(news):
    keys = sorted(news.keys(),reverse=True)
    for key in keys:
        yield key,news[key]

# return sorted text (dict format) of @filePath
def sortTextFile(filePath):
    news = {}
    with open(filePath,'r',encoding='utf-8') as f:
        for line in f.readlines():
            # remove List brackets and split each list into 3 items
            line =line.strip().strip('[').strip(']').split(',')
            # 1st item as key that can be sorted soon in sortNewsNyield() func
            news[json.loads(line[0])]= json.loads((line[1]))+' | '+json.loads(line[2])
    return news

def main():
    city_dict = {
        '1': 'toronto',
        '2': 'ottawa',
        '3': 'hamilton',
        '4': 'vancouver',
        '5': 'calgary',
        '6': 'edmonton',
        '7': 'halifax',
        '8': 'st-johns'}
    drawHousingPricechart(city_dict)

if __name__ == '__main__':
    main()