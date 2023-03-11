from flask import request, Blueprint, jsonify
from ready import User_message, db, app, History, User_History
from user import Authorized

history = Blueprint('history', __name__)

@history.route('/user/history', methods=['DELETE'])
def message_delete(id):
    authorization = request.headers.get('Authorization')
    delete = request.get_json()
    id = delete.get('id')
    type = delete.get('type')
    list = delete.get('list')

    if not authorization:
        return jsonify(code=404, message='请先登录'), 200
    else:
        token = Authorized(authorization)
    if not token:
        return jsonify(code=404, message='无法检验token'), 200
    if token:
        token_id = token.get("id")
        try:
            with app.app_context():
                if type == 0:
                    d_type0 = db.session.query(User_History).filter_by(user=token_id, history=id).first()
                    db.session.delete(d_type0)
                    db.session.commit()
                    return jsonify(code=200, message='success'), 200
                if type == 1:
                    for i in list:
                        d_type1 = db.session.query(User_History).filter(user=id, history=i).first()
                        db.session.delete(d_type1)
                        db.session.commit()
                    return jsonify(code=200, message='success'), 200
        except Exception as e:
            return jsonify(code=404, message=f'删除失败，{e}'), 200


@history.route('/user/history/lc', methods=['PUT'])
def update(id):
    Authorization = request.headers.get('Authorization')
    update_message = request.get_json()
    id = update_message.get('id')
    fav = update_message.get('fav')
    if not Authorization:
        return jsonify(code=404, message='请先登录'), 200
    else:
        token = Authorized(Authorization)
    if not token:
        return jsonify(code=403, message='无法检验token'), 200
    if token:
        token_id = token.get("id")
        try:
            with app.app_context():
                p = db.session.query(History).filter_by(id=token_id, history=id).first()
                history = History.query.get(id)
                if not p:
                    return jsonify(code=404, message='missing'), 200
                else:
                    data = {
                        'name': history.name,
                        'artist': history.artist,
                        'album': history.album,
                        'duration': history.duration,
                        'rid': history.rid,
                    }
            return jsonify(code=200, data=data, message='success'), 200
        except Exception as e:
            return jsonify(code=404, message=f'{e}'), 200


@history.route('/user/history', methods=['GET'])
def query():
    authorize = request.headers.get('Authorization')
    page = int(request.args.get('page'))

    if not authorize:
        return jsonify(code=404, message='请先登录'), 200
    else:
        token = Authorized(authorize)

    if not token:
        return jsonify(code=404, message='登录认证失败，请重新登录'), 200
    if token:
        id = token.get('id')
        list = []
        try:
            with app.app_context():
                user = User_message.query.get(id)
                HISTORY = user.history
                total = len(HISTORY)
                if total % 10 == 0:
                    page = int(total / 10)
                if total == 0:
                    return jsonify(code=404, message='没有下载历史'), 200
                else:
                    page = int(total / 10) + 1
                Query = History.query.filter(History.id.in_([HISTORY.id for HISTORY in HISTORY]))
                history_record = Query.paginate(page=page, per_page=10).items

                for R in history_record:
                    r = db.session.query(User_History).filter_by(id=id, history=R.id).first()
                    data = {
                        'name': R.name,
                        'artist': R.artist,
                        'album': R.album,
                        'duration': R.duration,
                        'fav': r.fav,
                        'rid': R.rid,
                        'id':R.id
                    }
                    list = list + [data]
                data_list = {
                    'list': list,
                    'count': page
                }
            return jsonify(code=200, message='success', data=data_list), 200
        except Exception as e:
            return jsonify(code=404, message=f'{e}'), 200


@history.errorhandler(Exception)
def error(e):
    return jsonify(code=200, message='请重新登录'), 200
