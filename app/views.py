import os
from flask import render_template, redirect, make_response, abort, request, url_for
from werkzeug.utils import secure_filename
from flask_login import current_user


def init_views(app):
    # 自定义过滤器
    @app.template_filter('md')
    def markdown(txt):
        from markdown import markdown
        return markdown(txt)

    def read_md(filename):
        with open(filename) as fn:
            content = fn.readlines()
        return content

    # 模板可以应用其传送的 本文件定义的函数
    @app.context_processor
    def inject_methods():
        return dict(read_md=read_md, current_user=current_user)


    @app.route('/user/<username>')
    def user(username):
        return 'user: %s' % username

    @app.route("/passwd/<regex('\d{6,9}'):passwd>")
    def passwd(passwd):
        return 'passwd: %s' % passwd

    @app.route('/upload', methods=["GET", "POST"])
    def upload():
        if request.method == "POST":
            f = request.files['file']
            abspath = os.path.abspath(os.path.dirname(__file__))
            upload_path = os.path.join(abspath, 'static\\upload')

            # save 方法只能有一个参数，就是带有文件名的路径
            f.save(os.path.join(upload_path, secure_filename(f.filename)))
            return redirect(url_for('upload'))
        return render_template('upload.html')

    @app.route('/cookie')
    def cookie():
        abort(404)
        cookie = request.cookies
        response = make_response(render_template('index.html'))
        response.set_cookie('username', 'iyuers', 'say', 123)
        print(cookie)
        return response

    @app.errorhandler(404)
    def page_not_found(error):
        print(error)
        return render_template('404.html'), 404

    # 自定义测试函数
    @app.template_test('current_url')
    def is_current_url(href):
        return href == request.path



