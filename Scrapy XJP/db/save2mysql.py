# coding=utf-8

import pymysql

class eDatabase:
    def __init__(self,database=None):
        self._database = database
        self._db = pymysql.connect(host='localhost', user='root', password='1234', port=3306, charset='utf8',database=database)
        self._cursion = self._db.cursor()

    def showDB(self):
        self._cursion.execute('show databases')
        data = self._cursion.fetchall()
        print('it has databases: ',data)
        self._db.commit()

    def showTables(self):
        self._cursion.execute('show tables')
        data = self._cursion.fetchall()
        print('this %s database has tables: '%self._database,data)
        self._db.commit()

    def newDB(self,newDBname):
        try:
            sql = 'create database %s'%newDBname
            self._cursion.execute(sql)
            self._db.commit()
        except  Exception as e:
            print(e)

    def newTable(self,tableName):
        try:
            self._cursion.execute('create table %s' % tableName)
            self._db.commit()
        except Exception as e:
            print(e)

    def setTable(self):
        pass

    def queryTable(self, tableName):
        try:
            sql = "select * from (%s)" % (tableName)
            self._cursion.execute(sql)
            tableData = self._cursion.fetchall()
            print(tableData)
        except Exception as e:
            print(e)

    def insertDB(self, tableName,items):
        try:
            sql = "insert into %s values ('%s','%s','%s')" % (tableName,items[0], items[1], items[2])
            self._cursion.execute(sql)
            self._db.commit()
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

# return db,cursion
# if no specific database, then return the mySQL-server, cursion
def connectDB(database = None):
    db = pymysql.connect(host='localhost', user='root', password='1234', port=3306, charset='utf8', database=database)
    cursion = db.cursor()
    return db,cursion

def showDB(db, cursion):
    try:
        # db, cursion =connectDB()
        sql = 'show databases;'
        cursion.execute(sql)
        data = cursion.fetchall()
        print(data)
        db.commit()
    except Exception as e:
        print(e)

# create a new database
def newDB(db, cursion,newDBname):
    try:
        # db, cursion = connectDB()
        sql = 'create database %s'%newDBname
        cursion.execute(sql)
        db.commit()
    except  Exception as e:
        print(e)

# create a default table with 1 column- 'ID'(varchar(50))
def newTable(db, cursion,tableName):
    try:
        # db, cursion = connectDB(database)
        cursion.execute('create table if not exists %s ( %s varchar(50))'%(tableName,'ID'))
        db.commit()
    except Exception as e:
        print(e)

def addColumninTable(db, cursion,tableName,columnName,colunmType):
    try:
        cursion.execute('alter table %s add column %s %s'%(tableName,columnName,colunmType))
        db.commit()
    except Exception as e:
        print(e)

def setColumn(db, cursion,tableName,columnName,newcolumnName,newcolunmType):
    cursion.execute('alter table %s change column %s %s %s' % (tableName, columnName,newcolumnName,newcolunmType))
    db.commit()

# show tables Names in current connected Database
def showTables(db, cursion):
    try:
        # db, cursion = connectDB()
        cursion.execute('show tables')
        data = cursion.fetchall()
        print(data)
        db.commit()
    except Exception as e:
        print(e)

# show table structure
def describeTable(db, cursion,table):
    cursion.execute('desc %s'%table)
    data = cursion.fetchall()
    print(data)
    db.commit()

# show All data from the table in current connected database
def queryTable(db, cursion,tableName):
    try:
        # db, cursion = connectDB(database)
        sql ="select * from (%s)"%(tableName)
        cursion.execute(sql)
        tableData = cursion.fetchall()
        print(tableData)
        db.commit()
    except Exception as e:
        print(e)

# insert all column data accordingly. Now is being set 7 columns
def insertDataToTable(db,cursion,items,tableName):
    try:
        sql = 'insert into {} values {}'.format(tableName,(items[0],items[1],items[2],items[3],items[4],items[5],items[6]))
        print(sql)
        cursion.execute(sql)
        db.commit()

    except Exception as e:
        db.rollback()
        print(e)

# insert table 1 data into table2
def insterTable1ToTable2(db,cursion,table1,table2):
    try:
        sql = "insert into %s select * from %s"%(table2,table1)
        cursion.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

#delete all data from the table
def deleteAllTableData(db,cursion,table):
    try:
        sql = "delete from %s"%(table)
        cursion.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

# delete a column from a table
def deleteColumn(db,cursion,columnName,table):
    cursion.execute('alter table %s drop column %s'%(table,columnName))
    db.commit()

# def save2SQL(items):
#     db = pymysql.connect(host='localhost',user='root',password='1234',database='david',port=3306,charset='utf8')
#     cursion = db.cursor()
#     insertDataToTable(db,cursion,items)
#     cursion.close()
#     db.close()

def main():
    # testDB = eDatabase()
    # testDB.showDB()
    # testDB = eDatabase('david')
    # testDB.showTables()

    db,cursion = connectDB()
    # print(showDB(db,cursion))
    db, cursion = connectDB('david')
    # print(showTables(db, cursion),'tables')
    # newTable(db, cursion,'canadaHousePrice')
    # print(showTables(db, cursion), 'tables')
    # describeTable(db,cursion,'xjpinxh')
    # addColumninTable(db,cursion,'canadahouseprice','city','varchar(50)')
    # addColumninTable(db, cursion, 'canadahouseprice', 'houseID', 'varchar(15)')
    # addColumninTable(db, cursion, 'canadahouseprice', 'houseType', 'varchar(30)')
    # addColumninTable(db, cursion, 'canadahouseprice', 'houseSize', 'varchar(50)')
    # addColumninTable(db, cursion, 'canadahouseprice', 'housePrice', 'varchar(20)')
    # addColumninTable(db, cursion, 'canadahouseprice', 'houseLocation', 'text')
    # addColumninTable(db, cursion, 'canadahouseprice', 'houseLink', 'text')
    # deleteColumn(db,cursion,'ID','canadahouseprice')
    # setColumn(db,cursion,'canadahouseprice','houseID','houseID','varchar(15)')
    setColumn(db, cursion, 'canadahouseprice', 'housePrice', 'housePrice', 'int')
    # describeTable(db,cursion,'canadahouseprice')

    testData = ["toronto", "17825564", "House", "4bds,3bths", "$6,285,000", "259 FOREST HILL RD  Toronto, ON M5P 2N5", "https://www.royallepage.ca/en/property/ontario/toronto/259-forest-hill-rd/17825564/mlsc5639031/"]
    # insertDataToTable(db,cursion,testData,'canadahouseprice')
    queryTable(db,cursion,'canadahouseprice')

if __name__ == '__main__':
    main()