# Created by carryon on 19-1-15.
import os

from PIL import Image
from flask import Blueprint, render_template, url_for, request, flash, get_flashed_messages, redirect, make_response, \
    session, current_app
from io import BytesIO
from app.forms import RegisterForm, LoginForm, UploadForm, ChpwForm, PwrtquetForm, PwrtForm
from app.models import User, Comment, Blogcol
from app.exts import db, photos
from app.email import send_mail
from app import code
from flask_login import login_required, login_user, logout_user, current_user

users = Blueprint('users', __name__)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if session.get('image') != form.verify_code.data:
            flash('验证码错误')
            return render_template('user/register.html', form=form)
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash("用户名已被占用")
            return render_template('user/register.html', form=form)

        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            flash("邮箱已被注册过，不能重复注册")
            return render_template('user/register.html', form=form)

        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(u)
        db.session.commit()

        # 生成token  用u对象调用模型中的方法
        token = u.generate_active_token()
        send_mail(u.email, '账户激活', 'email/activate', username=u.username, token=token)
        flash("恭喜注册成功,请点击邮件中的链接完成激活")
        return redirect(url_for('users.login'))
    return render_template('user/register.html', form=form)


# 这个方法用来验证token  给用户邮箱发送过去一个完整的url
@users.route('/active/<token>', methods=['GET', 'POST'])
def active(token):
    if User.check_active_token(token):
        flash("账户激活成功")
        return redirect(url_for('users.login'))
    else:
        flash("账户激活失败")
        return redirect(url_for('main.index'))


@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if session.get('image') != form.verify_code.data:
            flash('验证码错误')
            return render_template('user/login.html', form=form)

        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            # flash('验证通过，登录成功')
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('用户名或者密码不正确')
            return render_template('user/login.html', form=form)

    return render_template('user/login.html', form=form)


@users.route('/getcode/')
def getcode():
    image, str = code.validate_picture()
    # 将验证码图片以二进制形式写入在内存中，防止将图片都放在文件夹中，占用大量磁盘
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把二进制作为response发回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = str
    return response


@users.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("退出登录成功")
    return redirect(url_for('main.index'))


@users.route('/changeimg/', methods=['GET', 'POST'])
@login_required
def changeimg():
    img_url = ''
    form = UploadForm()
    if form.validate_on_submit():
        # 获取文件后缀
        suffix = os.path.splitext(form.icon.data.filename)[1]
        # 随机文件名  拼接
        filename = random_string() + suffix
        photos.save(form.icon.data, name=filename)
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        img = Image.open(pathname)
        img.thumbnail((128, 128))
        img.save(pathname)
        if current_user.icon != 'default.jpg':
            path = current_app.config['UPLOADED_PHOTOS_DEST'] + current_user.icon
            os.remove(path)
        current_user.icon = filename  # 将新上传的文件名 赋值给 用户的头像
        db.session.add(current_user)  # 保存在数据库中
        flash("头像上传成功")
        return redirect(url_for("users.changeimg"))
    img_url = photos.url(current_user.icon)
    return render_template('user/changeimg.html', form=form, img_url=img_url)


def random_string(length=10):
    import random
    base_str = 'abc123defhijklmnopqrstuvwxyz4567890'
    return ''.join(random.choice(base_str) for i in range(length))


# 个人中心 待补充
@users.route('/index/', methods=['GET', 'POST'])
def index():
    return render_template('user/index.html')


@users.route('/change_pw/', methods=['GET', 'POST'])
@login_required
def change_pw():
    form = ChpwForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("密码修改成功")
            logout_user()
            return redirect(url_for('users.login'))
        else:
            flash("密码错误")
            return redirect(url_for('users.change_pw'))
    return render_template('user/change_pw.html', form=form)


@users.route('/reset_pw/', methods=['GET', 'POST'])
def password_request():
    form = PwrtquetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_active_token()
            send_mail(user.email, '重置密码', 'email/resetpw', username=user.username, token=token)
            flash("邮件已发送,点击邮件的链接完成密码重置")
            return redirect(url_for('users.login'))
        else:
            flash("没有用户注册过这个邮箱！")
            return redirect(url_for('users.login'))
    return render_template('user/reset_pw.html', form=form)


@users.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    form = PwrtForm()
    if form.validate_on_submit():
        if User.check_reset_token(token, form.password.data):
            flash("密码重置成功")
            return redirect(url_for('users.login'))
        else:
            flash("密码重置失败")
            return redirect(url_for('users.login'))
    return render_template('user/change_pw.html', form=form)


@users.route('/collect/')
def collect():
    page = request.args.get('page', 1, type=int)
    pagination = Blogcol.query.filter(Blogcol.user_id == current_user.id).order_by(Blogcol.add_time.desc()).paginate(page,
                                                                                                        per_page=5,
                                                                                                        error_out=False)
    posts = pagination.items
    return render_template('user/collect.html', posts=posts, pagination=pagination)
