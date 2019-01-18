# Created by carryon on 19-1-15.
from flask import Blueprint, render_template, url_for, request, flash, get_flashed_messages, redirect, jsonify
from flask_login import login_required, current_user

from app.exts import db
from app.forms import BlogForm, CommentForm
from app.models import Blog, Comment, Blogcol

posts = Blueprint('posts', __name__)


@posts.route('/collect/', methods=['GET', 'POST'])
@login_required
def collect():
    uid = request.args.get("uid", "")
    bid = request.args.get("bid", "")
    # print(uid, bid)
    blogcol = Blogcol.query.filter_by(
        user_id=int(uid),
        blog_id=int(bid)
    ).first()
    if blogcol:
        db.session.delete(blogcol)
        db.session.commit()
        data = dict(ok=0)
    else:
        blogcol = Blogcol(user_id=int(uid), blog_id=int(bid))
        db.session.add(blogcol)
        db.session.commit()
        data = dict(ok=1)
    return jsonify(data)


@posts.route('/search/', methods=['GET', 'POST'])
def search():
    some = request.args.get('some')
    print(some)
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter(Blog.text.contains(some)).order_by(Blog.add_time.desc()).paginate(page, per_page=5,
                                                                                                     error_out=False)
    posts = pagination.items
    return render_template('posts/search.html', posts=posts, pagination=pagination)


@posts.route('/write/', methods=['GET', 'POST'])
@login_required
def write():
    form = BlogForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()
        p = Blog(title=form.title.data, text=form.text.data, user=user)
        db.session.add(p)
        return redirect(url_for('main.index'))
    return render_template('posts/write.html', form=form)


@posts.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter(Blog.uid == current_user.id).order_by(Blog.add_time.desc()).paginate(page,
                                                                                                        per_page=5,
                                                                                                        error_out=False)
    posts = pagination.items
    return render_template('posts/index.html', posts=posts, pagination=pagination)


@posts.route('/single/<_id_>', methods=['GET', 'POST'])
def single(_id_):
    form = CommentForm()
    if form.validate_on_submit():
        comm = Comment(content=form.text.data, user_id=current_user.id, blog_id=_id_)
        blog = Blog.query.filter(Blog.id == _id_).first()
        blog.commentnum += 1
        db.session.add(blog)
        db.session.add(comm)
        return redirect(url_for('posts.single', _id_=_id_))
    post = Blog.query.filter(Blog.id == _id_).first()
    comments = Comment.query.filter(Comment.blog_id == _id_).all()
    return render_template('posts/single.html', post=post, form=form, comments=comments)

