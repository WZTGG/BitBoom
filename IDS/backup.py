#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：backup.py
@Author  ：wenzt
@Date    ：2023/7/10 20:37 
@脚本说明：
"""


import paramiko
import time


# SSH连接参数
host = '192.168.11.170'
port = 22
username = 'root'
password = '123456'

# 远程文件路径
remote_path_get = '/opt/lampp/logs/access_log'

# 建立SSH连接
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host, port, username, password)

# 使用SFTP协议打开远程文件
sftp_client = ssh_client.open_sftp()
remote_file_get = sftp_client.open(remote_path_get)

remote_file_get.seek(0,2)
while True:
    try:
        list = remote_file_get.readlines()
        if len(list) > 0:
            for line in list:
                with open('access_log.txt','a') as file:
                    file.write(line)
        time.sleep(5)
    except:
        # 关闭文件和SSH连接
        remote_file_get.close()
        sftp_client.close()
        ssh_client.close()