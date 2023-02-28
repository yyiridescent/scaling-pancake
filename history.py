from flask import request, Blueprint, jsonify
from 准备工作 import User_message,db,app,User_History
from user import Authorized

history=Blueprint('User_History',__name__)

@app.route('/user/history',methods=['DELETE'])
def message_delete(id):
    Authorization = request.headers.get('Authorization')
    delete=request.get_json()
    id=delete.get('id')
    type=delete.get('type')
    list=delete.get('list')
    if not Authorization:
        return jsonify(code=404,message='请先登录'),200
    else:
        token = Authorized(Authorization)
    if not token:
        return jsonify(code=403,message='无法检验token'),200
    if token:
        token_id = token.get("id")

        try:
            with app.app_context():
                if type == 0:
                    d_type0 = db.session.query(User_History).filter(user_id=token_id, history_id=id).first()
                    db.session.delete(d_type0)
                    db.session.commit()
                    return jsonify(code=200, message='success'), 200
                if type == 1:
                    for i in list:
                        d_type1 = db.session.query(User_History).filter(user_id=id, history_id=i).first()
                        db.session.delete(d_type1)
                        db.session.commit()
                    return jsonify(code=200, message='success'), 200
        except Exception as e:
            return jsonify(code=404, message=f'删除失败，{e}'), 200

@app.route('/user/history/lc',methods=['PUT'])
def update(id):
    Authorization = request.headers.get('Authorization')
    update_message=request.get_json()
    id=update_message.get('id')
    fav = update_message.get('fav')
    if not Authorization:
        return jsonify(code=404,message='请先登录'),200
    else:
        token = Authorized(Authorization)
    if not token:
        return jsonify(code=403,message='无法检验token'),200

    if token:
        token_id = token.get("id")

        try:
            with app.app_context():
                p=db.session.quary(User_History).filter(user_id=token_id,history_id=id).first()
                history=User_History.quary.get(id)
                if not p:
                    return jsonify(code=404,message='missing'),200
                else:
                    data = {
                        'name': history.name,
                        'artist': history.artist,
                        'album': history.album,
                        'duration': history.duration,
                        'rid': history.rid,
                        }
            return jsonify(code=200,data=data,message='success'),200
        except Exception as e:
            return jsonify(code=404,message=f'{e}'),200

@app.route('/user/history',methods=['GET'])
def get_message():
    Authorization = request.headers.get('Authorization')
    page=request.args.get('page')
    page=int(page)

    if not Authorization:
        return jsonify(code=404,message='请先登录'),200
    else:
        token=Authorized(Authorization)
    if not token:
        return jsonify(code=403,message='无法检验token'),200

    if token:
        id=token.get('id')
        try:
            with app.app_context():
                user=User_message.quary.get(id)
                history=user.history
                total=len(history)
                if total%10==0:
                    page=int(total/10)
                else:
                    page=int(total/10)+1
                quary=User_History.quary.filter(User_History.id.in_([history.id for history in history]))
                history_record=User_History.quary.filter(page=page,per_page=10).item
                for R in history_record:
                    r=db.seesion.quary(User_History).filter(user_id=id,history_id=R.id).first()
                    data={
                        'name':R.name,
                        'artist':R.artist,
                        'album':R.album,
                        'duration':R.duration,
                        'fav':r.fav,
                        'rid':r.rid
                    }
                    list=list+[data]
                data_list={
                    'list':list,
                    'count':page
                }
            return jsonify(code=200,message='success',data=data_list),200
        except Exception as e:
            return jsonify(code=404,message=f'{e}'),200

@app.errorhandler(Exception)
def error(e):
    return jsonify(code=200, message='请重新登录'), 200