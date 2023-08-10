#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：MYSQL_HIDS.py
@Author  ：wenzt
@Date    ：2023/7/16 16:38 
@脚本说明：
"""
from function import *
import paramiko
import time
import re
from mysql_connent import *
# SSH连接参数
host = '192.168.11.170'
port = 22
username = 'root'
password = '123456'

# 远程文件路径
remote_path_mysql = '/var/log/mysql.log'

# 建立SSH连接
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host, port, username, password)

# 使用SFTP协议打开远程文件
sftp_client = ssh_client.open_sftp()
remote_file_mysql = sftp_client.open(remote_path_mysql)

remote_file_mysql.seek(0,2)

count_list = []
item_counts = {}

while True:
    try:
        list = remote_file_mysql.readlines()        # 每一次均读取最新内容
        if len(list) > 0:
            for line in list:
                # print(line)
                # 定义正则表达式模式
                patterns = r"^\d+.*Connect.+Access denied for user '(\w+)'@'(\S+)'.*"
                patternss=r'^\d+.*Query\s+(.*)'
                # 提取IP地址、用户名
                match = re.match(patterns,line)
                # 提取sql语句
                match2= re.match(patternss,line)
                if match:
                    user= match.group(1)
                    ip_address = match.group(2)
                    print(f'{ip_address}远程登录{user}用户失败')
                    count_list.append(ip_address)
                    if count_list:
                        for item in count_list:
                            item_counts[item] = item_counts.get(item, 0)+1
                            if item_counts[item] == 55:
                                Mysql().mysqllog(ip_address, user, '疑似mysql登录爆破')
                                print("IP:%s 疑似爆破" % ip_address)
                                count_list = []
                                item_counts = {}
                                if block_ip(ip_address):
                                    print("IP:%s 已被封禁" % ip_address)

                if match2:
                    sql_statement= match2.group(1)
                    if check_sql_statement(sql_statement):
                        Mysql().mysqllog('localhost', sql_statement, '数据库语句有敏感操作')
                        print("数据库语句有敏感操作",sql_statement)
        time.sleep(5)
    except:
        #关闭文件和SSH连接
        remote_file_mysql.close()
        sftp_client.close()
        ssh_client.close()
