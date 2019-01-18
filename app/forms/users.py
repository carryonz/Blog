# Created by carryon on 19-1-15.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.validators import ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User  # 自定义验证函数 用户提交检测数据中是否存在
from app.exts import photos  # 只能上传图片


# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 20, message="用户名必须在6到20位之间")])
    email = StringField('Email', validators=[Email(message="邮箱格式不正确")])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须在6到20位之间")])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message="两次密码不一致")])
    verify_code = StringField('验证码', validators=[DataRequired()])
    submit = SubmitField('立即注册')


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 20, message="用户名必须在6到20位之间")])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须在6到20位之间")])
    verify_code = StringField('验证码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')


# 用户上传表单
class UploadForm(FlaskForm):
    icon = FileField("头像", validators=[FileRequired(), FileAllowed(photos, message="只能上传图片类型")])
    submit = SubmitField('立即上传')


# 修改密码表单
class ChpwForm(FlaskForm):
    oldpassword = PasswordField('旧密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须在6到20位之间")])
    password = PasswordField('新密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须在6到20位之间")])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message="两次密码不一致")])
    submit = SubmitField('提交')


# 重置密码请求
class PwrtquetForm(FlaskForm):
    email = StringField('Email', validators=[Email(message="邮箱格式不正确")])
    submit = SubmitField('提交')


# 重置密码
class PwrtForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须在6到20位之间")])
    submit = SubmitField('提交')
