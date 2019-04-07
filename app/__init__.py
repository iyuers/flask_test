import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_gravatar import Gravatar
from werkzeug.routing import BaseConverter
from .views import init_views
from config import config


class RegexConverter(BaseConverter):
    """
    定义一个正则表达式的路由规则类
    """
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# 引入美化页面的插件
bootstrap = Bootstrap()

# 数据库实例化
db = SQLAlchemy()

# 登录插件实例化
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# 实例化PageDown
pagedown = PageDown()


def create_app(config_name='default'):
    app = Flask(__name__)

    # 初始化正则表达式路由规则类，就是在 app 里面添加 url_map
    app.url_map.converters['regex'] = RegexConverter

    # 即时更新网页
    app.debug = True

    # 关于表单提交的 csrf 跨站保护的设置
    app.config.from_pyfile('config.txt')

    # SQLite 数据库配置
    absdir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(absdir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 测试用的 调用 config.py 文件进行配置
    # app.config.from_object(config[config_name])

    # 引入美化导航栏
    nav = Nav()

    nav.register_element('top', Navbar('FlaskTest',
                                       View('主页', 'main.hello_world'),
                                       View('关于', 'main.about'),
                                       View('登录', 'auth.login'),
                                       View('上传', 'upload'),
                                       ))
    nav.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    Gravatar(app, size=64)

    init_views(app)
    from . import auth as auth_blueprint
    from . import main as main_blueprint
    app.register_blueprint(auth_blueprint.auth)
    app.register_blueprint(main_blueprint.main)

    return app






