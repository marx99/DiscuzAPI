# -*- coding: utf-8 -*-
import pymysql

class mysqlAPI:
    def __init__(self, db):
        ''' 初始化mysql '''
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1',db=db,charset='utf8')

    def insert_mysql(self,sql,rows):    
        
        cur = self.conn.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute("SET CHARACTER_SET_CLIENT=utf8")
        cur.execute("SET CHARACTER_SET_RESULTS=utf8")
        self.conn.commit()
    
        aa=cur.executemany(sql,rows)
        print('insert',aa)
        cur.close()
        self.conn.commit()
#        self.conn.close() 
        
    def select_mysql(self,url):
        cur = self.conn.cursor()
        aa=cur.execute(url)
        info=cur.fetchmany(aa)
        cur.close()
        self.conn.commit()
#        self.conn.close()
        return info
        
    def close_mysql(self):
        self.conn.close()