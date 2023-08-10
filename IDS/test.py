#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：project 
@File    ：test.py
@Author  ：wenzt
@Date    ：2023/7/16 11:39 
@脚本说明：
"""
import xml.etree.ElementTree as ET
import re
# 读取XML文件
tree = ET.parse("csrf.xml")
root = tree.getroot()
log_entry='Referer: http://192.168.11.130/\r\n'
host = '192.168.11.170'
# 遍历所有Expression元素
def check_sql_injection(log_entry):
    for expression in root.findall("Expression"):
        expression_text = expression.text
        match = re.match(expression_text, log_entry)
        if match:
            ip_address = match.group(1)
            print(ip_address)
            if ip_address != host:
                return True
        return False
if __name__ == '__main__':
    res=check_sql_injection(log_entry)
    if res:
        print("中了")