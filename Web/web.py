from flask import Flask, render_template, jsonify
import pymysql
from flask_cors import CORS
import subprocess
import time
import shlex

app = Flask(__name__)
CORS(app, origins='*')  # 设置CORS头为允许任意主机
# 连接到 MySQL 数据库
def conn():
    connection = pymysql.connect(
        host="192.168.11.30",
        user="root",
        password="123456",
        database="IDS"
    )
    cursor = connection.cursor()
    return cursor
# 定义数据库查询语句



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_web_log')
def get_web_log():
    
    while True:
        cursor=conn()
        # 创建游标对象
        
        query = "SELECT id,ip, class,url ,status_code,time FROM weblog;"
        # 执行数据库查询
        cursor.execute(query)

        # 获取查询结果
        results = cursor.fetchall()

        # 将查询结果转换成 JSON 格式
        data = [{'id': id,'ip': ip, 'class': class_, 'url': url, 'status_code': status_code,'time': times} for id, ip, class_, url, status_code,times in results]
        # print(data)
        # 返回 JSON 数据给前端页面

        # 返回 JSON 数据给前端页面
        time.sleep(5)
        return jsonify(data)
        

@app.route('/get_sys_log')
def get_sys_log():
    
    while True:
        cursor=conn()
        # 创建游标对象
        
        query = "SELECT id,ip, class,time FROM syslog;"
        # 执行数据库查询
        cursor.execute(query)

        # 获取查询结果
        results = cursor.fetchall()

        # 将查询结果转换成 JSON 格式
        data = [{'id': id,'ip': ip, 'class': class_,  'time': times} for id,ip, class_,  times in results]
        # print(data)
        # 返回 JSON 数据给前端页面

        # 返回 JSON 数据给前端页面
        time.sleep(5)
        return jsonify(data)

@app.route('/get_mysql_log')
def get_mysql_log():
    
    while True:
        cursor=conn()
        # 创建游标对象
        
        query = "SELECT id, ip, content,class,time FROM mysqllog;"
        # 执行数据库查询
        cursor.execute(query)

        # 获取查询结果
        results = cursor.fetchall()

        # 将查询结果转换成 JSON 格式
        data = [{'id': id,'ip': ip, 'content': content,'class': class_,  'time': times} for id,ip,content, class_,  times in results]
        # print(data)
        # 返回 JSON 数据给前端页面

        # 返回 JSON 数据给前端页面
        time.sleep(5)
        return jsonify(data)


# 获取远程系统信息
def get_system_info():
    # 获取到的系统信息
    with open("/opt/lampp/htdocs/HIDS/sys_info.txt", "r") as file:
        lines = file.readlines()
    info= lines[0].strip()       #系统信息
    cpu_usage = lines[1].strip()  # CPU使用率
    memory_usage = lines[2].strip()  # 内存使用率
    port_open = lines[-1].strip()  # 开放的端口号列表
    network_connections =lines[3:-1]
    # 返回系统信息数据
    return {
        'sysinfo':info,
        'cpu': cpu_usage,
        'memory': memory_usage,
        'portOpen': port_open,
        'networkConnections': network_connections
    }

@app.route('/get_system_info', methods=['GET'])
def get_system_info_endpoint():
    # 调用获取系统信息的函数
    system_info = get_system_info()
    return jsonify(system_info)

@app.route('/get_file_info', methods=['GET'])
def get_file_info_endpoint():
    # 调用获取系统信息的函数
    file_info = get_file_info()
    return jsonify(file_info)
def get_file_info():
    # 获取到文件信息
    with open("/opt/lampp/htdocs/HIDS/file_content.txt", "r") as file:
        lines = file.readlines()
    file_content= lines[0:-1]       
    file_content.append(lines[-1].strip())
    
    with open("/opt/lampp/htdocs/HIDS/file_danger.txt", "r") as file:
        liness = file.readlines()
    file_path= liness[0:-1]
    file_path.append(liness[-1].strip())

    # 返回数据
    return {
        'fileContent':file_content,
        'filePath': file_path
        
    }

@app.route('/get_file_change', methods=['GET'])
def get_file_change_endpoint():
    # 调用获取系统信息的函数
    file_change = get_file_change()
    return jsonify(file_change)
def get_file_change():
    with open("/opt/lampp/htdocs/HIDS/file_change.txt", "r") as file:
        liness = file.readlines()
    file_change= liness[0:-1]
    file_change.append(liness[-1].strip())

    # 返回数据
    return {
        'filechange':file_change,
        
    }



# 添加其他标签页的后端接口
# ... (其他标签页的后端接口)


@app.route('/run_python_script')
def run_python_script():
        # 运行第二条命令
        command1=['/usr/bin/python3', '/opt/python/IDS/MYSQL_HIDS.py']
        subprocess.run(command1, check=True)

        # 运行第三条命令
        command2= ['/usr/bin/python3', '/opt/python/IDS/sys_IDS.py']
        subprocess.run(command2, check=True)

        # 运行第四条命令
        command3= ['/usr/bin/python3', '/opt/python/IDS/HIDS.py']
        subprocess.run(command3, check=True)

        # 运行第五条命令
        command4='/usr/bin/python3 /opt/python/IDS/file_IDS.py'
        subprocess.run(command4, check=True)

        # 其他命令...
        
        print("多条命令已成功运行！")
        return "多条命令已成功运行！"





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
