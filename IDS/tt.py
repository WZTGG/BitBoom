#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：tt.py
@Author  ：wenzt
@Date    ：2023/7/16 19:49 
@脚本说明：
"""
import paramiko
import time

# 远程主机连接信息
host = '192.168.11.170'
username = 'root'
password = '123456'
remote_folder_path = '/tmp'

# 创建SSH客户端
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

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

    # 检查修改文件
    for file_path in file_status:
        if file_path in new_file_status and file_status[file_path] != new_file_status[file_path]:
            # 修改文件
            print(f"修改文件: {file_path}")
            _, stdout, _ = ssh.exec_command(f"cat {file_path}")
            file_contents = stdout.read().decode().strip()
            print(f"文件内容:\n{file_contents}")

    # 检查删除文件
    for file_path in file_status:
        if file_path not in new_file_status:
            # 删除文件
            print(f"删除文件: {file_path}")

    # 更新文件状态
    file_status = new_file_status

    # 延时五秒
    time.sleep(5)

# 关闭SSH连接
ssh.close()





