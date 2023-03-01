from flask import Flask, config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123@localhost:3306/Music"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/music'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(config)

db = SQLAlchemy(app)

class User_History(db.Model):  # 历史记录
    __tablename__ = 'user_history'
    id = db.Column(db.Integer, db.ForeignKey('user_message.id'), primary_key=True)
    fav = db.Column(db.Integer, nullable=False, default=0) #default默认值
    history = db.Column(db.Integer, db.ForeignKey('history.id'), primary_key=True)  # 外键


class User_message(db.Model):  # 登录&注册
    __tablename__ = 'user_message'
    id = db.Column(db.Integer, primary_key=True)  # integer 整型 32位
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    history = db.relationship('History', secondary='history', lazy='subquery',
                              backref=db.backref('user', lazy=True))  # relationship建立一对多（一）关系,使用子查询


@property  # 创建只读属性
def password(self):
    return self.password_hash


@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)  # 密码哈希处理


def check_password(self, checkpassword):
    return check_password_hash(self.password_hash, checkpassword)  # 密码验证的哈希处理


class History(db.Model):  # 历史记录的具体内容
    __tablename__ = 'history'
    name = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    rid = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)

with app.app_context():
    db.drop_all()
    db.create_all()
    name = User_message.query.filter(User_message.username == 'admin').first()
    if not name:
        admin = User_message(username='admin', password='123456')
        db.session.add(admin)
        db.session.commit()