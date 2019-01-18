# Created by carryon on 19-1-15.
from flask import Blueprint, render_template, request, flash, get_flashed_messages, redirect, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import login_required

from app.models import Blog

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    # posts = Blog.query.filter_by().all()
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter_by().order_by(Blog.add_time.desc()).paginate(page, per_page=5,
                                                                                error_out=False)
    posts = pagination.items
    return render_template('main/index.html', posts=posts, pagination=pagination)

