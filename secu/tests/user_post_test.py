import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common

class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/user'

    def setUp(self):
        super().setUp()
        self.data = {
            'username': 'myao',
            'email': '1343030803@qq.com',
            'mobile': '18665369920',
            'pwd': '123456',
            'fullname': '姚贯伟',
            'roles': ''
        }

    def test_by_correct_info(self):
        response = requests.post(self.url, json=self.data)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])