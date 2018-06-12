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
            'id': 'af33f6c395ed430da8ade19bc75f5049',
            'username': 'myao',
            'email': '1343030803@qq.com',
            'mobile': '18665369920',
            'pwd': '123456',
            'fullname': '姚贯伟',
            'roles': '',
            'active': '1'
        }

        query = '''
            insert into secu_user(id, username, email, mobile, fullname, pwd, active) values (:id, :username, :email, :mobile, :fullname, :pwd, :active);
        '''
        self.db.execute(query, self.data)
        self.db.commit()

    def test_by_correct_info(self):
        response = requests.delete(self.url, json={'id': self.data['id']})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select count(1) from secu_user where id=:id;
        '''

        result = self.db.execute(query, self.data).scalar()

        self.assertEqual(0, result)