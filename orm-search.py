import time

import pymysql
from flask import Flask,jsonify
import requests

app=Flask(__name__)#实例化类
app.secret_key="123abndhd"

@app.route('/search?text=周杰伦',methods=['GET'])
def search():
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
    all_rid=[]

    for i in range(1,18):
        page = i
        url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=周杰伦&pn={}&rn=30&httpsStatus=1&reqId=da11ad51-d211-11ea-b197-8bff3b9f83d2e'.format(page)

        response = requests.get(url, headers=headers1)
        response = response.json()
        music_list = response["data"]["list"]
        a = 1
        for music in music_list:
            singer = music["artist"]  # 歌手名
            name = music["name"]  # 歌曲名
            album=music["album"] #专辑
            duration=music["duration"] #时长

            rid = music["musicrid"]
            index = rid.find('_')
            rid = rid[index + 1:len(rid)]#切割

            data={
                'name':name,
                'artist':singer,
                'album':album,
                'duration':duration,
                'rid':rid
            }
            a =a+1
            time.sleep(1)
            all_rid.append(rid)
        return jsonify(code=200,message="success",list=data)

@app.route('/search/download/:<rid>')
def download(rid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'
    }
    url1 = 'https://link.hhtjim.com/kw/' + rid + '.mp3'
    data={
        'key': '周杰伦',
        'httpsStatus': '1',
        'reqId': '396bbb70 - ad1a - 11ed - a1a3 - 6185cb7fcadd'
    }
    res=requests.post(url=url1,headers=headers,params=data).content
    with open(res,'wb') as fp:
        fp.write(res)

