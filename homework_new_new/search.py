import os
import requests
from flask import jsonify, Blueprint, request, send_file
from ready import User_message,db,app,History
from user import Authorized

def info(rid):
    detailurl = f'http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={rid}&httpsStatus=1'
    detail = requests.get(detailurl).json()['data']['songinfo']
    return detail

new_search=Blueprint('search',__name__)

@new_search.route('/search',methods=['GET'])
def Search():
    authorization = request.headers.get('Authorization')
    text = request.args.get('text')
    page = request.args.get('page')
    print(1)
    if not authorization:
        return jsonify(code=404,message='请先登录'),200
    else:
        token=Authorized(authorization)

    if not text:
        return jsonify(code=404,message='请先输入'),200

    elif token:

        url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord'
        headers1 = {
            'Cookie': 'kw_token=XFXKUH6WB',
            'csrf': 'XFXKUH6WB',
            'Referer': 'http://www.kuwo.cn/search/list',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'
        }
        params = {
            'key': text,
            'pn': page,
            'rn': 10,
            'httpsStatus': '1',
            'reqId': '53027fb0 - bfb2 - 11ed - a428 - 7fb8c7b7de6e'
        }
        response = requests.get(url=url, headers=headers1, params=params)
        json = response.json()
        total = int(json['data']['total'])
        print(total)
        if total == 0:
            return jsonify(code=404, message=f'没有找到与{text}有关的内容'), 200
        if total % 10 == 0:
            pages = int(total / 10)
        else:
            pages = int(total / 10) + 1
        list1=[]
        json_list = json['data']['list']
        print(json_list)
        for music in json_list:
            rid = music['rid']
            message = info(rid)
            dict = {
                "name": message['songName'],
                "artist": message['artist'],
                "album": message['album'],
                "duration": message['songTimeMinutes'],
                "rid": message['id']
            }
            list1 += [dict]
        music_list = {'list': list1}
        print(music_list)
        return jsonify(code=200, message='success', data=music_list), 200
    else:
        return jsonify(code=404, message='登录认证失败，请重新登录'), 200

@new_search.route('/search/download/<rid>',methods=['GET'])
def download(rid):
    try:
        os.makedirs('Music')
    except Exception as e:
        print(e)
    detail=info(rid)
    authorization = request.headers.get('Authorization')
    if not authorization:
        return jsonify(code=404,message='请先登录'),200
    token=Authorized(authorization)
    id=token.get('id')
    if not token:
        return jsonify(code=404,message='请重新登录'),200
    if token:
        try:
            with app.app_context():
                user=User_message.query.get(id)
                query=History.query.filter(History.rid == rid).first()
                if not query:
                    add=History(name=detail['songName'],artist=detail['artist'],album=detail['album'],duration=detail['songTimeMinutes'],rid=detail['id'])
                    db.session.add(add)
                    user.history.append(add)
                    db.session.commit()
                else:
                    user.history.append(query)
                    db.session.commit()

                title=f'{detail["songName"]}-{detail["artist"]}'
                file_path=f'music/{title}.mp3'
                if os.path.exists(file_path):
                    return send_file(file_path,as_attachment=True)
                else:
                    infourl=f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'
                    musicurl=requests.get(infourl).json()['data']['url']
                    musicdata=requests.get(musicurl).content
                    with open(file_path,mode='wb') as f:
                        f.write(musicdata)
                    return send_file(file_path,as_attachment=True)
        except Exception as e:
            return jsonify(code=404,message='{e}'),200

@new_search.errorhandler(Exception)
def error(e):
    return jsonify(code=200, message='请重新登录'), 200