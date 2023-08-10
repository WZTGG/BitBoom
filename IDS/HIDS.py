#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：HIDS.py
@Author  ：wenzt
@Date    ：2023/7/9 15:05 
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
remote_path_get = '/opt/lampp/logs/access_log'
remote_path_post = '/opt/lampp/logs/error_log'
remote_path_sys ='/var/log/secure'

# 建立SSH连接
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host, port, username, password)

# 使用SFTP协议打开远程文件
sftp_client = ssh_client.open_sftp()
remote_file_get = sftp_client.open(remote_path_get)
remote_file_post = sftp_client.open(remote_path_post)
remote_file_sys = sftp_client.open(remote_path_sys)

remote_file_get.seek(0,2)
remote_file_post.seek(0,2)
remote_file_sys.seek(0,2)
count_list = []
item_counts = {}


while True:
    try:
        list = remote_file_get.readlines()        # 每一次均读取最新内容
        list += remote_file_post.readlines()
        list += remote_file_sys.readlines()
        if len(list) > 0:
            for line in list:
                # print(line)
                # 定义正则表达式模式
                patterns = r'^(\S+) \S+ \S+ \[(.+)\] "(.+)" (\d+) '
                patternss=r'^\[(\S+\s+\S+\s+\d+\s+\d+:\d+:\d+\.\d+)\s+\d+\] \[dumpio:trace7\] \[.*\] mod_dumpio.c\(\d+\): \[client (\S+):\d+\] .+\(data-HEAP\): (\S+.*)'
                syspatterns=r'^\S+\s\d+\s\S+\s\S+\ssshd\S+\sFailed password for\s(\S+)\sfrom\s(\S+)\sport\s\d+\s(\S+)'
                # 提取IP地址、时间、URL地址和状态码
                match = re.match(patterns,line)
                match2 = re.match(patternss,line)
                match3 = re.match(syspatterns,line)
                if match3:
                    user = match3.group(1)
                    ip = match3.group(2)
                    sshh = match3.group(3)
                    if re.search(r"^ssh", sshh):
                        count_list.append(ip)
                        if count_list:
                          for item in count_list:
                              item_counts[item] = item_counts.get(item, 0) + 1
                              if item_counts[item] == 5:  #1+2+3...+10=55 满10次
                                print("IP:%s 疑似ssh爆破" %ip)
                                Mysql().syslog(ip,f'疑似ssh登录爆破用户{user}')
                                count_list = []
                                item_counts = {}
                                if block_ip(ip_address):
                                    print("IP:%s 已被封禁" %ip_address)
                if match:
                    ip_address = match.group(1)
                    timestamp = match.group(2)
                    url = match.group(3)
                    status_code = match.group(4)
                    if re.search(r"404|408|^3", status_code):
                        count_list.append(status_code)
                        if count_list:
                          for item in count_list:
                              item_counts[item] = item_counts.get(item, 0) + 1
                              if item_counts[item] == 55:  #1+2+3...+10=55 满10次
                                print("IP:%s 疑似爆破" %ip_address)
                                Mysql().weblog(ip_address,url,'疑似爆破',status_code)
                                count_list = []
                                item_counts = {}
                                if block_ip(ip_address):
                                    print("IP:%s 已被封禁" %ip_address)
                if match2:
                    timestamp2 = match2.group(1)
                    ip_address2 = match2.group(2)
                    datas = match2.group(3)
                    print(datas)
                    if check_sql_injection(datas):
                        Mysql().weblog(ip_address2, datas, '疑似SQL注入，等级7', '')
                        print("疑似SQL注入，等级7")
                        print("时间戳:", timestamp2)
                        print("IP地址:", ip_address2)
                        print("http请求头值:", datas)
                        print('------------------')
                        count_list.append(ip_address2)
                        if count_list:
                            for item in count_list:
                                item_counts[item] = item_counts.get(item, 0) + 1
                                if item_counts[item] == 55:
                                    print("IP:%s 疑似爆破" % ip_address2)
                                    count_list = []
                                    item_counts = {}
                                    if block_ip(ip_address2):
                                        print("IP:%s 已被封禁" % ip_address2)
                    if check_xss_injection(datas):
                        Mysql().weblog(ip_address2, datas, '疑似XSS注入，等级7', '')
                        print("疑似XSS注入，等级7")
                        print("时间戳:", timestamp2)
                        print("IP地址:", ip_address2)
                        print("http请求头值:", datas)
                        print('------------------')
                        count_list.append(ip_address2)
                        if count_list:
                            for item in count_list:
                                item_counts[item] = item_counts.get(item, 0) + 1
                                if item_counts[item] == 55:
                                    print("IP:%s 疑似爆破" % ip_address2)
                                    count_list = []
                                    item_counts = {}
                                    if block_ip(ip_address2):
                                        print("IP:%s 已被封禁" % ip_address2)
                    if check_CSRF_attack(datas):
                        Mysql().weblog(ip_address2, datas, '疑似CSRF，等级7', '')
                        print("疑似CSRF，等级7")
                        print("时间戳:", timestamp2)
                        print("IP地址:", ip_address2)
                        print("http请求头值:", datas)
                        print('------------------')
                        count_list.append(ip_address2)
                        if count_list:
                            for item in count_list:
                                item_counts[item] = item_counts.get(item, 0) + 1
                                if item_counts[item] == 55:
                                    print("IP:%s 疑似爆破" % ip_address2)
                                    count_list = []
                                    item_counts = {}
                                    if block_ip(ip_address2):
                                        print("IP:%s 已被封禁" % ip_address2)
                    if check_file_include(datas):
                        Mysql().weblog(ip_address2, datas, '疑似文件包含，等级7', '')
                        print("疑似文件包含，等级7")
                        print("时间戳:", timestamp2)
                        print("IP地址:", ip_address2)
                        print("http请求头值:", datas)
                        print('------------------')
                        count_list.append(ip_address2)
                        if count_list:
                            for item in count_list:
                                item_counts[item] = item_counts.get(item, 0) + 1
                                if item_counts[item] == 55:
                                    print("IP:%s 疑似爆破" % ip_address2)
                                    count_list = []
                                    item_counts = {}
                                    if block_ip(ip_address2):
                                        print("IP:%s 已被封禁" % ip_address2)
                    if check_file_upload(datas):
                        Mysql().weblog(ip_address2, datas, '疑似木马上传，等级7', '')
                        print("疑似木马上传，等级7")
                        print("时间戳:", timestamp2)
                        print("IP地址:", ip_address2)
                        print("http请求头值:", datas)
                        print('------------------')
                        count_list.append(ip_address2)
                        if count_list:
                            for item in count_list:
                                item_counts[item] = item_counts.get(item, 0) + 1
                                if item_counts[item] == 55:
                                    print("IP:%s 疑似爆破" % ip_address2)
                                    count_list = []
                                    item_counts = {}
                                    if block_ip(ip_address2):
                                        print("IP:%s 已被封禁" % ip_address2)
                    if check_unserialize(datas):
                        Mysql().weblog(ip_address2, datas, '疑似反序列化，等级7', '')
                        print("疑似反序列化，等级7")
                        print("时间戳:", timestamp2)
                        print("IP地址:", ip_address2)
                        print("http请求头值:", datas)
                        print('------------------')
                        count_list.append(ip_address2)
                        if count_list:
                            for item in count_list:
                                item_counts[item] = item_counts.get(item, 0) + 1
                                if item_counts[item] == 55:
                                    print("IP:%s 疑似爆破" % ip_address2)
                                    count_list = []
                                    item_counts = {}
                                    if block_ip(ip_address2):
                                        print("IP:%s 已被封禁" % ip_address2)
                    if check_shell(datas):
                        Mysql().weblog(ip_address2, datas, '疑似反弹shell，等级10', '')
                        print("疑似反弹shell，等级10")
                        print("时间戳:", timestamp2)
                        print("IP地址:", ip_address2)
                        print("http请求头值:", datas)
                        print('------------------')
                        count_list.append(ip_address2)
                        if count_list:
                            for item in count_list:
                                item_counts[item] = item_counts.get(item, 0) + 1
                                if item_counts[item] == 55:
                                    print("IP:%s 疑似爆破" % ip_address2)
                                    count_list = []
                                    item_counts = {}
                                    if block_ip(ip_address2):
                                        print("IP:%s 已被封禁" % ip_address2)

        time.sleep(5)
    except:
        # 关闭文件和SSH连接
        remote_file_get.close()
        sftp_client.close()
        ssh_client.close()
