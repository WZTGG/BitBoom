#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：sys_IDS.py
@Author  ：wenzt
@Date    ：2023/7/16 16:29 
@脚本说明：
"""
from function import *
import paramiko
import time


# SSH连接参数
host = '192.168.11.170'
port = 22
username = 'root'
password = '123456'

# 远程文件路径
remote_path_mysql = '/etc/my.cnf'
remote_path_php = '/opt/lampp/etc/php.ini'
remote_folder='/opt/lampp/htdocs/crm17/pop'
remote_path_http = '/opt/lampp/etc/httpd.conf'


# 建立SSH连接
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host, port, username, password)



# 使用SFTP协议打开远程文件
sftp_client = ssh_client.open_sftp()
remote_file_php = sftp_client.open(remote_path_php)
remote_file_mysql = sftp_client.open(remote_path_mysql)
remote_file_http = sftp_client.open(remote_path_http)

def file_content():
    with open("/opt/lampp/htdocs/HIDS/file_content.txt","w") as file:
                file.write('')
    list1=''
    list2=''
    list3=''
    # 逐行读取远程文件内容
    for line1 in remote_file_php:
        if check_php(line1):  # 打印每行日志内容
            print("文件",remote_path_php)
            print("有不安全配置项",line1)
            list1+=line1
    with open("/opt/lampp/htdocs/HIDS/file_content.txt","a") as file:
                file.write(remote_path_php)
                file.write("\n")
                file.write(list1)
                file.write("\n")

    # 逐行读取远程文件内容
    for line2 in remote_file_mysql:
        if check_php(line2):  # 打印每行日志内容
            print("文件",remote_path_mysql)
            print("有不安全配置项",line2)
            list2+=line2
    with open("/opt/lampp/htdocs/HIDS/file_content.txt","a") as file:
                file.write(remote_path_mysql)
                file.write("\n")
                file.write(list2)
                file.write("\n")


    for line3 in remote_file_http:
        if check_php(line3):  # 打印每行日志内容
            print("文件",remote_path_http)
            print("有不安全配置项",line2)
            list3+=line3
    with open("/opt/lampp/htdocs/HIDS/file_content.txt","a") as file:
                file.write(remote_path_http)
                file.write("\n")
                file.write(list3)
                file.write("\n")



    with open("/opt/lampp/htdocs/HIDS/file_danger.txt","w") as file:
                file.write("")
    # 遍历文件夹并处理文件内容
    sftp_traverse_folder(sftp_client, remote_folder)
   





def monitor_remote_host():
    while True:
        with open("/opt/lampp/htdocs/HIDS/sys_info.txt","w") as file:
                file.write("")
        # 获取服务器系统信息
        _, sys_stdout, _ = ssh_client.exec_command("uname -a")
        # 读取并解码获取的输出，并去除首尾的空白字符。
        sys_line = sys_stdout.read().decode().strip()
        print("服务器系统信息")
        print(sys_line)
        

        # 获取CPU使用情况
        _, cpu_stdout, _ = ssh_client.exec_command("top -bn 1 | grep 'Cpu(s)'")
        # 读取并解码获取的输出，并去除首尾的空白字符。
        cpu_line = cpu_stdout.read().decode().strip()
        # 将获取的输出按空格进行分割，并提取出第二个元素，即CPU使用率
        cpu_usage = cpu_line.split()[1]
        # 将提取出的CPU使用率转换为浮点数类型。使用[:-1]切片操作去除最后的百分号字符
        cpu_usage = float(cpu_usage[:-1])
        print(f"CPU使用情况: {cpu_usage}%")

        # 获取内存使用情况
        _, mem_stdout, _ = ssh_client.exec_command("free -m | grep 'Mem'")
        mem_line = mem_stdout.read().decode().strip()
        # 将获取的输出按空格进行分割，并提取出第二个和第三个元素，即总内存和已使用内存
        mem_total, mem_used = map(int, mem_line.split()[1:3])
        # 计算内存使用率，即已使用内存除以总内存乘以100
        mem_usage = (mem_used / mem_total) * 100
        print(f"内存使用情况: {mem_usage:.2f}%")

        # 获取网络连接情况
        _, net_stdout, _ = ssh_client.exec_command("netstat -an | grep tcp")
        net_connections = net_stdout.read().decode().strip()
        print("网络连接情况: ")
        print(net_connections)

        # 执行netstat命令，获取所有网络连接情况
        _, net_port, _ = ssh_client.exec_command("netstat -an| grep tcp")
        net_openports = net_port.read().decode().strip()
        lines =net_openports.split('\n')
        port_set = set()

        # 提取端口号信息并添加到Set中
        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                local_addr = parts[3]
                local_port = local_addr.split(':')[-1]
                if '.' in local_addr:  # IPv4
                    port_set.add(local_port)
                elif ':' in local_addr:  # IPv6
                    ipv6_parts = local_addr.split(':')
                    if len(ipv6_parts) > 1:  # 去掉可能的IPv6补充字段
                        local_port = ipv6_parts[-1]
                        port_set.add(local_port)
        print("端口开放情况: ")
        print(port_set)
        with open("/opt/lampp/htdocs/HIDS/sys_info.txt","a") as file:
                file.write(str(sys_line))
                file.write("\n")
                file.write(str(cpu_usage))
                file.write("\n")
                file.write(str(mem_usage))
                file.write("\n")
                file.write(str(net_connections))
                file.write("\n")
                file.write(str(port_set))
        time.sleep(10)

# 调用函数开始监控
file_content()
monitor_remote_host()
