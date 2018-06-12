import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common

class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/role'

    def setUp(self):
        super().setUp()
        self.data = {
            'name': '添加项目',
            'description': '添加项目',
        }

    def test_by_correct_info(self):
        response = requests.post(self.url, json=self.data)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select id from secu_role where name = :name;
        '''

        result = self.db.execute(query, self.data).scalar()

        self.assertEqual(32, len(result))