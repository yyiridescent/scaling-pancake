import os
import requests
from flask import Flask, jsonify, Blueprint, request, send_file
from 准备工作 import User_message,db,app,User_History
from user import Authorized

def info(rid):
    detailurl = f'http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={rid}&httpsStatus=1'
    detail = requests.get(detailurl).json()['data']['songinfo']
    return detail

search=Blueprint('search',__name__)
@app.route('/search',methods=['GET'])
def search():
    Authorization=request.headers.get('Authorization')
    text=request.args.get('text')
    #search
    if not Authorization:
        return jsonify(code=404,message='请先登录'),200
    else:
        token=Authorized(Authorization)
    if not text:
        return jsonify(code=404,message='请先输入'),200
    elif token:
        url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord'
        headers1 = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': '_ga=GA1.2.1500987479.1595755923; _gid=GA1.2.568444838.1596065504; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1595755923,1596065505; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1596078189; _gat=1; kw_token=IJATWHHGI8',
            'csrf': 'IJATWHHGI8',
            'Host': 'www.kuwo.cn',
            'Referer': 'http://www.kuwo.cn/search/list?key=%E6%A2%A6%E7%9A%84%E5%9C%B0%E6%96%B9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
             }
        param={
            'key':text,
            'pn':1,
            'rn':10,
            'httpsStatus':1
        }
        response = request.get(url, headers=headers1,params=param)
        response = response.json()
        music_list = response["data"]["list"]
        all=int(music_list)
        if all==0:
            return jsonify(code=404,message=f'没有找到与{text}有关的内容'),200
        if all%10==0:
            page=int(all/10)
        else:
            page=int(all/10)+1
        list=[]
        for music in music_list:
            rid=music['rid']
            detailurl = f'http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={rid}&httpsStatus=1'
            message = requests.get(detailurl).json()['data']['songinfo']
            data={
                'name':message["name"],
                'artist':message["artist"],
                'album':message["album"],
                'duration':message["duration"],
                'rid':message['musicrid']
            }
            list=list+[data]
            musiclist={
                'list':list,
                'count':page
            }
            return jsonify(code=200,message='success',data=musiclist),200

@app.route('/search/download/:<rid>',methods=['GET'])
def download(rid):
    try:
        os.makedirs('Music')
    except Exception as e:
        print(e)
    detailurl = f'http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={rid}&httpsStatus=1'
    detail = requests.get(detailurl).json()['data']['songinfo']
    Authorization = request.headers.get('Authorization')
    if not Authorization:
        return jsonify(code=404,message='请先登录'),200
    token=Authorized(Authorization)
    id=token.get('id')
    if not token:
        return jsonify(code=404,message='请重新登录'),200
    if token:
        try:
            with app.app_context():
                user=User_message.quary.get(id)
                quary=User_History.quary.filter(User_History.rid==rid).first()
                if not quary:
                    add=User_History(name=detail['songName'],artist=detail['artist'],album=detail['album'],duration=detail['songTimeMinutes'],rid=detail['id'])
                    db.session.add(add)
                    user.history.append(add)
                    db.session.commit()
                else:
                    user.history.append(quary)
                    db.session.commit()
                title=f'{detail["songName"]}-{detail["artist"]}'
                file_path=f'music/{title}.mp3'
                if os.path.exists(file_path):
                    return send_file(file_path,as_attachment=True)
                else:
                    infourl=f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'
                    musicurl=requests.get(infourl).json()['data']['url']
                    musicdata=requests.get(musicurl).content
                    with open(file_path,'wb') as f:
                        f.write(musicdata)
                    return send_file(file_path,as_attachment=True)
        except Exception as e:
            return jsonify(code=404,message='{e}'),200

@app.errorhandler(Exception)
def error(e):
    return jsonify(code=200, message='请重新登录'), 200