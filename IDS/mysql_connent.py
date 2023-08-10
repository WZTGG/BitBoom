#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：mysql_connent.py
@Author  ：wenzt
@Date    ：2023/7/17 10:26 
@脚本说明：
"""
import pymysql
from datetime import datetime
class Mysql:
    host="192.168.11.130"
    port=3306
    user= "root"
    password= "123456"
    database="IDS"
    charset = "utf8"
    def weblog(self, ip, url, classs, status_code):
        current_datetime = datetime.now()
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, charset=self.charset)
        mycursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into weblog (ip,url,class,status_code,time) values (%s,%s,%s,%s,%s)"
        try:
            mycursor.execute(sql, (ip, url, classs, status_code,current_datetime))
            conn.commit()
            print("成功")
            conn.close()
        except:
            print("失败")
            conn.close()

    def mysqllog(self, ip, content, classs):
        current_datetime = datetime.now()
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, charset=self.charset)
        mycursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into mysqllog (ip,content,class,time) values (%s,%s,%s,%s)"
        try:
            mycursor.execute(sql, (ip, content, classs, current_datetime))
            conn.commit()
            print("成功")
            conn.close()
        except:
            print("失败")
            conn.close()

            

    def syslog(self, ip, classs):
        current_datetime = datetime.now()
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, charset=self.charset)
        mycursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into syslog (ip,class,time) values (%s,%s,%s)"
        try:
            mycursor.execute(sql, (ip, classs, current_datetime))
            conn.commit()
            print("成功")
            conn.close()
        except:
            print("失败")
            conn.close()
if __name__ == '__main__':
    Mysql().mysqllog('192.168.11.170','GET /muma.php?code=phpinfo(); HTTP/1.1','sql注入')