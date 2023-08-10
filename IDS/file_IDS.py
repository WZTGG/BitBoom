#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：file_IDS.py
@Author  ：wenzt
@Date    ：2023/7/16 21:09 
@脚本说明：
"""
import paramiko
import time
import os
import requests
import json
import re

# 远程主机连接信息
host = '192.168.11.170'
username = 'root'
password = '123456'
remote_folder_path = '/tmp'

# 创建SSH客户端
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接到远程主机
ssh.connect(host, username=username, password=password)

# 初始化文件状态
file_status = {}

def get_remote_file_status():
    _, stdout, _ = ssh.exec_command(f"find {remote_folder_path} -type f -printf '%T@ %p\n'")
    output = stdout.read().decode()
    files = output.strip().split('\n')
    file_status = {}
    for file_info in files:
        file_parts = file_info.split()
        if len(file_parts) == 2:
            modified_time, file_path = file_parts
            modified_time = float(modified_time)
            file_status[file_path] = modified_time
    return file_status

# 获取初始文件状态
file_status = get_remote_file_status()


while True:
    # 检查文件变化
    new_file_status = get_remote_file_status()

    # 检查新增文件
    for file_path in new_file_status:
        if file_path not in file_status:
            # 新增文件
            print(f"新增文件: {file_path}")
            _, stdout, _ = ssh.exec_command(f"cat {file_path}")
            file_contents = stdout.read().decode('latin-1').strip()
            print(f"文件内容:\n{file_contents}")
            # 远程下载文件
            remote_url = f'http://192.168.11.170{file_path}'
            local_dir = r'/tmp/upload'
            # 取文件名
            patterns = r'^/.*/(\S+\.\S+)'
            match = re.match(patterns, file_path)
            file_name=match.group(1)
            print(file_name)
            local_file = os.path.join(local_dir, file_name)
            response = requests.get(remote_url)
            with open(local_file, 'wb') as f:
                f.write(response.content)

            url = 'https://api.threatbook.cn/v3/file/upload'
            fields = {
                'apikey': '6b61900bcdc34b539cc22f46f6eeb69911d09e4a752243a3ad5ed6a38d7154b1',
                'sandbox_type': 'centos_7_x64',
                'run_time': 60
            }
            file_dir = '/tmp/upload'
            print(file_name)
            files = {
                'file': (file_name, open(os.path.join(file_dir, file_name), 'rb'))
            }
            response = requests.post(url, data=fields, files=files)
            print(files)
            # 将响应结果转换为字符串
            result_str = json.dumps(response.json())
            # print(result_str)
            # 使用正则表达式匹配网址部分
            match2 = re.search(r'"permalink": "([^"]+)"', result_str)
            if match2:
                url = match2.group(1)
                print(url)
                with open("/opt/lampp/htdocs/HIDS/file_change.txt","a") as file:
                    file.write(f'新增文件{file_path}')
                    file.write("\n")
                    file.write(f'检测报告{url}')
                    file.write("\n")
                    file.write('------------------------')
                    file.write("\n")
            else:
                print('No match found.')

    # 检查修改文件
    for file_path in file_status:
        if file_path in new_file_status and file_status[file_path] != new_file_status[file_path]:
            # 修改文件
            print(f"修改文件: {file_path}")
            _, stdout, _ = ssh.exec_command(f"cat {file_path}")
            file_contents = stdout.read().decode().strip()
            print(f"文件内容:\n{file_contents}")
            with open("/opt/lampp/htdocs/HIDS/file_change.txt","a") as file:
                    file.write(f'修改文件{file_path}')
                    file.write("\n")
                    file.write(f'文件内容{file_contents}')
                    file.write('------------------------')
                    file.write("\n")

    # 检查删除文件
    for file_path in file_status:
        if file_path not in new_file_status:
            # 删除文件
            print(f"删除文件: {file_path}")
            with open("/opt/lampp/htdocs/HIDS/file_change.txt","a") as file:
                    file.write(f'删除文件{file_path}')
                    file.write("\n")
                    file.write('------------------------')
                    file.write("\n")

    # 更新文件状态
    file_status = new_file_status

    # 延时五秒
    time.sleep(5)

# 关闭SSH连接
ssh.close()


