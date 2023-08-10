#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：function.py
@Author  ：wenzt
@Date    ：2023/7/13 16:34 
@脚本说明：
"""
import stat
import xml.etree.ElementTree as ET
import subprocess
import re

import paramiko


# SSH连接参数
host = '192.168.11.170'
port = 22
username = 'root'
password = '123456'

# 建立SSH连接
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host, port, username, password)


def check_php(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/check_php.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for check_php_patterns in root.findall("Expression"):
        check_php_patterns_text = check_php_patterns.text
        # 检查日志条目是否匹配任何文件包含规则
        if re.search(check_php_patterns_text, log_entry, re.IGNORECASE):
            return True
    return False

def sftp_traverse_folder(sftp, folder):
    files = sftp.listdir(folder)
    for file in files:  #遍历files列表中的每个项目
        file_path = folder + '/' + file  #将folder路径和file名称连接起来构建当前文件或文件夹的完整路径。结果路径存储在file_path变量中
        remote_attr = sftp.stat(file_path)  #通过将folder路径和file名称连接起来构建当前文件或文件夹的完整路径。结果路径存储在file_path变量中
        if stat.S_ISREG(remote_attr.st_mode):  #查文件是否是一个普通文件（不是目录或特殊文件）。它使用stat模块的stat.S_ISREG()函数根据文件的模式来判断
            # 处理文件内容
            handle_file_content(sftp, file_path)
            
        elif stat.S_ISDIR(remote_attr.st_mode):#检查文件是否是一个目录。使用stat.S_ISDIR()函数根据文件的模式来判断
            # 递归遍历子文件夹
            sftp_traverse_folder(sftp, file_path)

def handle_file_content(sftp, file_path):
    # 读取文件内容
    file = sftp.open(file_path)
    content = file.read()
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/file_content.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for file_content_patterns in root.findall("Expression"):
        file_content_patterns_text = file_content_patterns.text
        # 检查日志条目是否匹配任何规则
        if re.search(file_content_patterns_text, str(content), re.IGNORECASE):
            print("有危险函数")
            print("文件路径:", file_path)
            # print("文件内容:")
            # print(content)
            print("---------------------------------------")
            with open("/opt/lampp/htdocs/HIDS/file_danger.txt","a") as file:
                file.write(file_path)
                file.write("\n")
    file.close()

def check_sql_injection(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/sql.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for sql_injection_patterns in root.findall("Expression"):
        sql_injection_patterns_text = sql_injection_patterns.text
        # 检查日志条目是否匹配任何SQL注入规则
        if re.search(sql_injection_patterns_text, log_entry, re.IGNORECASE):
            return True
    return False

def check_xss_injection(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/xss.xml")  #使用ET.parse()函数加载名为"sql.xml"的XML文件，并将其解析为一个XML树
    root = tree.getroot()     #获取XML树的根元素，将其赋值给变量root
    # 遍历所有Expression元素
    for xss_injection_patterns in root.findall("Expression"):
        xss_injection_patterns_text = xss_injection_patterns.text
        # 检查日志条目是否匹配任何SQL注入规则
        if re.search(xss_injection_patterns_text, log_entry, re.IGNORECASE):
            return True
    return False

def check_CSRF_attack(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/csrf.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for patterns in root.findall("Expression"):
        patterns_text = patterns.text
        # 检查日志条目是否匹配任何CSRF规则
        match = re.match(patterns_text, log_entry)
        if match:
            ip_address = match.group(1)
            print(ip_address)
            if ip_address != host:
                return True
        return False

def check_file_include(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/file_include.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for file_include_patterns in root.findall("Expression"):
        file_include_patterns_text = file_include_patterns.text
        # 检查日志条目是否匹配任何文件包含规则
        if re.search(file_include_patterns_text, log_entry, re.IGNORECASE):
            return True
    return False

def check_file_upload(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/file_upload.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for file_upload_patterns in root.findall("Expression"):
        file_upload_patterns_text = file_upload_patterns.text
        # 检查日志条目是否匹配任何文件上传规则
        if re.search(file_upload_patterns_text, log_entry, re.IGNORECASE):
            return True
    return False

def check_unserialize(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/file_upload.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for check_unserialize_patterns in root.findall("Expression"):
        check_unserialize_patterns_text = check_unserialize_patterns.text
        # 检查日志条目是否匹配任何PHP反序列化规则
        if re.search(check_unserialize_patterns_text, log_entry, re.IGNORECASE):
            return True
    return False

def check_shell(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/check_shell.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for check_shell_patterns in root.findall("Expression"):
        check_shell_patterns_text = check_shell_patterns.text
        # 检查日志条目是否匹配反弹shell规则
        if re.search(check_shell_patterns_text, log_entry, re.IGNORECASE):
            return True
    return False


def block_ip(ip_address):
    command = f'iptables -I INPUT -s {ip_address} -j DROP'
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        return True
    else:
        return False

def unblock_ip(ip_address):
    command = f'iptables -D INPUT -s {ip_address} -j DROP'
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        return True
    else:
        return Falsee

def check_sql_statement(log_entry):
    # 读取XML文件
    tree = ET.parse("/opt/python/IDS/sql_statement.xml")
    root = tree.getroot()
    # 遍历所有Expression元素
    for check_sql_statement_patterns in root.findall("Expression"):
        check_sql_statement_patterns_text = check_sql_statement_patterns.text
        # 检查日志条目是否匹配反弹shell规则
        if re.search(check_sql_statement_patterns_text, log_entry, re.IGNORECASE):
            return True
    return False
