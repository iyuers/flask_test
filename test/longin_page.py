from selenium import webdriver


class LoginPage(object):

    def __init__(self, c):
        self.client = c

    def get_title(self):
        return self.client.title

    def set_user_name(self, name):
        username = self.client.find_element_by_name('user')
        username.send_keys(name)

    def set_pwd(self, pwd):
        password = self.client.find_element_by_name('password')
        password.send_keys(pwd)

    def submit(self):
        submit = self.client.find_element_by_name('submit')
        submit.click()













