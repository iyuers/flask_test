import unittest
from app import create_app, db
from app.models import Role, User
from forgery_py import internet, basic
from flask import url_for


class TestModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.app_client = self.app.test_client()

        db.drop_all()
        db.create_all()
        Role.seed()

    def tearDown(self):
        self.app_ctx.pop()

    def test_role_user_set(self):
        db.session.add(User(name=internet.user_name(),
                            email=internet.email_address(),
                            password=basic.text()))
        db.session.commit()

        self.assertEqual(User.role.name, 'Guests')

    def test_hello_world(self):
        response = self.app_client(url_for('.hello_word'))
        self.assertEqual(response.status_code, 200)











