import unittest
from app import create_app, db
from app.models import Role, User
from selenium import webdriver
import threading
import re
from forgery_py import internet, basic


class SeleniumLogin(unittest.TestCase):
    client = None
    app_ctx = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        if cls.client:
            cls.app = create_app('test')
            cls.app_ctx = cls.app.app_context()
            cls.app_ctx.push()

            db.drop_all()
            db.create_all()
            Role.seed()
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        # 关闭服务器
        cls.client.get("http://localhost:5000/shutdown")
        cls.client.close()

        cls.app_ctx.pop()
        db.session.remove()

    def setUp(self):
        # 检查 web 浏览器 是否启动
        if self.client:
            self.skipTest('略过测试')

    def tearDown(self):
        pass

    # 测试登录方法
    def test_user_login(self):
        # 建立一个模拟用户
        new_user = User(name=internet.user_name(),
                        email=internet.email_address(),
                        password=basic.text())
        db.session.add(new_user)
        db.session.commit()

        # 获取登录界面
        self.client.get("http://localhost:5000/auth/login")
        self.assertTrue('登录' in self.client.title)

        # 设置登录用户名和密码
        user_name = self.client.find_element_by_name('user')
        user_name.send_keys(new_user.name)

        pwd = self.client.find_element_by_name('password')
        pwd.send_keys(new_user.password)

        submit = self.client.find_element_by_name('submit')
        submit.click()

        # 获得登录跳转页面的信息
        self.assertTrue(re.search(r'', self.client.page_source))

        # # 另一种方式
        # from .longin_page import LoginPage
        # page = LoginPage(self.client)
        # self.assertTrue('登录' in page.get_title())
        #
        # page.set_user_name(new_user.name)
        # page.set_pwd(new_user.password)
        # page.submit()











