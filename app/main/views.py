from flask import render_template, request, redirect, url_for, current_app, abort
from . import main
from ..models import Post, Comment
from .forms import PostForm, CommentForm
from .. import db
from flask_login import login_required, current_user


@main.route('/')
def hello_world():
    # 获取传递的页面值数据
    page_index = request.args.get('page', 1, type=int)

    # 将 Post 中的数据 进行排序
    query = Post.query.order_by(Post.created.desc())

    # 分页规范，每页显示多少行
    pagination = query.paginate(page_index, per_page=20, error_out=False)

    # 将分页数据表示出来
    posts = pagination.items
    return render_template("index.html", title="<h1>hello iyuers<h1>", posts=posts, pagination=pagination)


@main.route('/about')
def about():
    return 'about'


@main.route('/test')
def test():
    return 'test'


@main.route('/post/<int:id>', methods=["GET", "POST"])
def post(id):
    """进入帖子详情里面的，视图函数"""
    post = Post.query.get_or_404(id)
    # 评论窗体
    form = CommentForm()
    # 保存评论
    if form.validate_on_submit():

        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user
                          )
        db.session.add(comment)
        db.session.commit()
    # 评论列表

    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit(id=0):
    """编辑帖子的视图函数"""
    form = PostForm()

    if id == 0:
        # 新增
        post = Post(author=current_user)
    else:
        # 修改
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post', id=post.id))

    title = '添加新文章'
    if id > 0:
        title = '编辑 - {}'.format(post.title)

    return render_template('posts/edit.html',
                           title=title,
                           form=form,
                           post=post)


@main.route('/shutdown')
def shutdown():
    # 只有测试时，才能使用这个视图函数
    if not current_app.testing:
        abort(404)

    shoutdown = request.environ.get('werkzeug.server.shutdown')
    if shoutdown:
        abort(505)

    shoutdown()
    return "关闭服务器中...."



















