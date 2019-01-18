# Created by carryon on 19-1-16.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.validators import ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed


#写博客表单
class BlogForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    text = TextAreaField('正文', validators=[DataRequired()])
    submit = SubmitField('提交')


#评论表单
class CommentForm(FlaskForm):
    text = TextAreaField('say something:', validators=[DataRequired()])
    submit = SubmitField('评论')
