import json

import pymysql
import requests
from flask import Flask, request
import SQLAlchemy

db=pymysql.connect(host='localhost',user='root',password='Yueye13084030',port=3306,charset='utf8',database='homework',autocommit=False)
cursor=db.cursor()
sql1='DROP DATABASE IF EXISTS loved_Music'
cursor.execute(sql1)
sql2='CREATE DATABASE loved_music'
cursor.execute(sql2)
sql3='USE loved_music'
cursor.execute(sql3)
sql4='''CREATE TABLE message (
        name VARCHAR(20) NOT NULL,
        artist varchar(50) NOT NULL,
        album varchar(100) NOT NULL,
        duration varchar(10) NOT NULL，
        rid INT NOT NULL,
        fav INT NOT NULL
'''
cursor.execute(sql4)
db.commit()

app = Flask(__name__)  # 实例化类
user='root'
password=' '
database='loved_music'
url='mysql+pymysql://%s:%s@localhost:3306/%s' %(id,password,database)
app.config['SQLALCHEMY_DATABASE_URL']=url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

@app.route('/user/history',methods=['DELETE'])
def message_delete(id):
    type = request.get(type)
    if type == 0:
        db.seesion.filter(id=id).delete()
    if type == 1:
        db.session.filter(list=list).delete()
    data={
        'code':200,
        'message':'success'
    }
    r = requests.post(data=data)
    return r.text

@app.route('/user/history/lc',methods=['PUT'])
def update(id):
    name=request.form.get('name')
    artist = request.form.get('artist')
    album = request.form.get('album')
    duration = request.form.get('duration')
    fav=request.form.get('fav')
    rid = request.form.get('rid')

    data={
        'name':name,
        'artist':artist,
        'album':album,
        'duration':duration,
        'fav':fav,
        'rid':rid,
        'id':id
    }
    r = requests.post(data=data)
    return r.text

@app.errorhandler(403)
def catch_except(e):
    return '无法检验token'

@app.route('/user/history/?page=<page>',methods=['GET'])
def get_message(page):
    result=db.session.quary(page=page)
    page=request.get('page')
    page_limit=result.quary.paginate(10,page).items
    data={
        'list':page_limit,
        'count':page
    }
    r = requests.post(data=data)
    return r.text

@app.errorhandler(403)
def catch_except(e):
    return '无法检验token'
