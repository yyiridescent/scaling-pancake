import os
import pymysql
import requests
from flask import Flask
import SQLAlchemy

db=pymysql.connect(host='localhost',user='root',password='Yueye13084030',port=3306,charset='utf8',database='homework',autocommit=False)
cursor=db.cursor()
sql1='DROP DATABASE IF EXISTS User_message'
cursor.execute(sql1)
sql2='CREATE DATABASE User_message'
cursor.execute(sql2)
sql3='USE User_message'
cursor.execute(sql3)
sql4='''CREATE TABLE users(
        id INT,
        user_name varchar(50)
        password varchar(100)
'''
cursor.execute(sql4)
db.commit()

app = Flask(__name__)  # 实例化类
user='root'
password=' '
database='User_message'
url='mysql+pymysql://%s:%s@localhost:3306/%s' %(id,password,database)
app.config['SQLALCHEMY_DATABASE_URL']=url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class User_message:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@app.route("/user", methods=["POST"])
def register():
    user_name = input('Please put in your user name: ')
    user_password = input('Please put in your password here: ')
    user_CheckPassword = input('Please put in your password again:')
    a = 1
    id=0

    if user_password == user_CheckPassword:
        id=id+1

    else:
        while a != 0:
            user_CheckPassword = input('Please put in your password again:')
            if user_password == user_CheckPassword:
                a = 0
                id=id+1

    Id=User_message(id,user_name,user_password)
    url=' http://127.0.0.1:8000/user'
    data={
        'id':id,
        'Username':user_name
    }
    r=requests.post(url=url,data=data)
    return r.text

@app.errorhandler(Exception)
def catch_all_except(e):
    return  str(e)

@app.route("/user/login", methods=["POST"])
def login():
    user_name = input('Please put in your user name: ')
    user_password = input('Please put in your password here: ')
    b = 1
    user_list = os.listdir('./users')
    for user in user_list:
        if user == user_name:
            b = 0
            file_name = './user/' + user_name
            file_user = open(file_name)
            user_info = eval(file_user.read())
            if user_password == user_info['u_password']:
                print("Success")
                break

    if b == 0:
        print('Please register first.')

    url = ' http://127.0.0.1:8000/user'
    data = {
        'id': id,
        'Username': user_name
    }
    r = requests.post(url=url, data=data)
    url1='http://127.0.0.1:8000/user/login'
    data1={
        "id":id,
        "username":user_name,
        "token":r.json()['data']['token']
    }
    r2=requests.post(url=url1,data=data1)
    return r2.text

@app.errorhandler(Exception)
def catch_all_except(e):
    return  str(e)