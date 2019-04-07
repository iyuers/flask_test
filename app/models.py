from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from markdown import markdown


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    users = db.relationship('User', backref='role')

    @staticmethod
    def seed():
        """定义一个初始 Role 的方法，当创建数据库的时候，同时在数据库表单 roles 中添加两个成员"""
        db.session.add_all(map(lambda r: Role(name=r), ['Guest', 'Administrators']))
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    posts = db.relationship("Post", backref="author")
    comments = db.relationship("Comment", backref="author")

    @staticmethod
    def on_create(target, value, oldvalue, initiator):
        """
        数据库事件触发器的回调函数，当事件触发的时候，执行这个方法；
        将其外键，关联到 模型 Role 中的 'Guest'；
        """
        target.role = Role.query.filter_by(name='Guest').first()


# 挂钩 系统给自己调用，无需手动调用
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 定义数据库触发事件，当模型 User 新增时触发；
db.event.listen(User.name, 'set', User.on_create)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    body_html = db.Column(db.String)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    comments = db.relationship("Comment", backref="post")
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        """对存入的 body 进行 makedown 的格式化，并传递给 body_html"""
        if value is None or (value is ''):
            target.body_html = ''
        else:
            target.body_html = markdown(value)

db.event.listen(Post.body, 'set', Post.on_body_changed)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))









