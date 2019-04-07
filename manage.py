from livereload import Server
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import create_app, db
from app.models import Role, User, Post, Comment


app = create_app()

migrate = Migrate(app, db)

# 初始化Manager
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def dev():
    live_sever = Server(app.wsgi_app)
    live_sever.watch('**/*.*')
    live_sever.serve(open_url_delay=True)


@manager.command
def test():
    import unittest
    # 指定测试目录
    tests = unittest.TestLoader().discover('test')
    # 执行测试项目
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    upgrade()
    Role.seed()


@manager.command
def forged():
    from forgery_py import basic, lorem_ipsum, name, internet, date
    from random import randint

    db.drop_all()
    db.create_all()

    Role.seed()

    guests = Role.query.first()

    def generate_comment(func_author, func_post):
        return Comment(body=lorem_ipsum.paragraphs(),
                       created=date.date(past=True),
                       author=func_author(),
                       post=func_post())

    def generate_post(func_author):
        return Post(title=lorem_ipsum.title(),
                    body=lorem_ipsum.paragraphs(),
                    created=date.date(),
                    author=func_author())

    def generate_user():
        return User(name=internet.user_name(),
                    email=internet.email_address(),
                    password=basic.text(6, at_least=6, spaces=False),
                    role=guests)

    users = [generate_user() for i in range(0, 5)]
    db.session.add_all(users)

    random_user = lambda: users[randint(0, 4)]

    posts = [generate_post(random_user) for i in range(0, randint(50, 200))]
    db.session.add_all(posts)

    random_post = lambda: posts[randint(0, len(posts) - 1)]

    comments = [generate_comment(random_user, random_post) for i in range(0, randint(2, 100))]
    db.session.add_all(comments)

    db.session.commit()

if __name__ == '__main__':

    manager.run()


