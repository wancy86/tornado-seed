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
            'id': 'a266f06037d043fbb4575a75be87f4ba',
            'name': '添加项目',
            'description': '添加项目',
        }

        query = '''
            insert into secu_role(id, name, description) values (:id, :name, :description);
        '''
        self.db.execute(query, self.data)
        self.db.commit()

    def test_by_correct_id(self):
        response = requests.delete(self.url, json={'id': self.data['id']})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select count(1) from secu_role where id=:id;
        '''
        result = self.db.execute(query, self.data).scalar()
        self.assertEqual(0, result)

    def test_by_wrong_id(self):
        response = requests.delete(self.url, json={'id': 'wrongid'})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('001', resp['code'])

        query = '''
            select count(1) from secu_role;
        '''
        result = self.db.execute(query, self.data).scalar()
        self.assertEqual(1, result)        