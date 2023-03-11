from datetime import timedelta,datetime
import jwt
from flask import request, Blueprint, jsonify
from ready import User_message,db,app

user = Blueprint('user_message',__name__)
ALGORITHM='HS256'
SECRET_KEY='culchyufrtedt'

@user.route("/user", methods=["POST"])
def register():
    get_data = request.get_json()
    user_name = get_data.get("username")
    user_password = get_data.get("password")
    user_CheckPassword = get_data.get("CheckPassword")
    with app.app_context():
        name=User_message.query.filter(User_message.username==user_name).first()#搜索
        if name:
            return jsonify(code=404,message='该用户已存在'),200
        else:
            if user_password==user_CheckPassword:
                try:
                    with app.app_context():
                        register=User_message(username=user_name,
                                              password=user_password)
                        db.session.add(register)#添加记录
                        db.session.flush()
                        db.session.commit()
                        dict ={'id':register.id,
                              'username':user_name
                              }
                    return jsonify(code=200,message='success',data=dict),200
                except Exception as e:
                    return jsonify(code=404,message=f'{e}'),200
            else:
                return jsonify(code=404,message='密码不一致'),200

@user.route("/user/login", methods=["POST"])
def login():
    try:
        get_data = request.get_json()
        user_name = get_data.get("username")
        user_password = get_data.get("password")
        with app.app_context():
            name = User_message.query.filter(User_message.username == user_name).first()
            if name:
                login = name.check_password(user_password)#hash
                if login:
                    access_token_expires = timedelta(minutes=60)
                    expire = datetime.utcnow() + access_token_expires
                    payload = {
                        "id": name.id,
                        "name": user_name,
                        "exp": expire
                    }
                    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)#token
                    dict = {
                        "id": name.id,
                        "username": user_name,
                        "token": access_token
                    }
                    return jsonify(code=200, message='success', data=dict), 200
                else:
                    return jsonify(cose=404, message='密码错误'), 200
            else:
                return jsonify(code=404, message='该用户名不存在'), 200
    except Exception as e:
        return jsonify(code=404,message=f'{e}'),200

def Authorized(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("name")
        with app.app_context():
            name = User_message.query.filter(User_message.username == username).first()
        if name:
            return payload
    except Exception as e:
        return False

    @user.errorhandler(Exception)
    def error(e):
        return jsonify(code=200, message='请重新登录'), 200
