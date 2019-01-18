# Created by carryon on 19-1-15.
from app.exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from app.exts import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(64), default='default.jpg')

    blogs = db.relationship('Blog', backref='user', lazy="dynamic")
    comment = db.relationship('Comment', backref='user', lazy="dynamic")
    blogcols = db.relationship('Blogcol', backref='user', lazy="dynamic")

    # 密码不能读 而且永不返回
    @property
    def password(self):
        raise AttributeError("密码不可读的帅哥")

    # 设置密码的时候  保存的是加密后的hash值
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 校验密码是否正确 正确 true 错误 false
    # 先加密 再跟数据库比较
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成token   通过邮箱发送给用户
    def generate_active_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    def is_active(self):
        return True

    # 验证token 方法
    @staticmethod
    def check_active_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        # 这个id是从 token中解析出来的  然后根据id 到数据库中查找  对应的数据进行更新
        u = User.query.get(data.get('id'))
        if not u:
            flash("该用户不存在")
            return False
        if not u.confirmed:
            u.confirmed = True
            db.session.add(u)
        return True

    @staticmethod
    def check_reset_token(token, password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        # 这个id是从 token中解析出来的  然后根据id 到数据库中查找  对应的数据进行更新
        u = User.query.get(data.get('id'))
        if not u:
            flash("该用户不存在")
            return False
        u.password = password
        db.session.add(u)
        db.session.commit()
        return True


# 登录成功以后 执行以下方法 回调函数 获取登录用户的相关信息
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# 博客信息
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    text = db.Column(db.Text)  # 内容
    commentnum = db.Column(db.BigInteger, default=0)  # 评论人数
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 写博客的时间
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))

    comment = db.relationship('Comment', backref='blog')
    blogcols = db.relationship('Blogcol', backref='blog')



# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 收藏博客的时间


# 博客收藏
class Blogcol(db.Model):
    __tablename__ = 'blogcol'
    id = db.Column(db.Integer, primary_key=True)  # 编号

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 收藏博客的时间

