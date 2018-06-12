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

        # 添加一条记录
        self.data = {
            'id': 'a266f06037d043fbb4575a75be87f4ba',
            'name': '添加项目',
            'description': '添加项目',
            'rights': '13afbe46cd374d3ab6b0130319bd7133,19c3864873aa42f98f38112336f7141b'
        }

        query = '''
            insert into secu_role(id, name, description, rights) values (:id, :name, :description, :rights);
        '''
        self.db.execute(query, self.data)

        # 添加10条记录
        for x in range(10):
            data = {
                'id': str(uuid.uuid4()).replace('-', ''),
                'name': '添加项目' + str(x),
                'description': '',
            }

            query = '''
                insert into secu_role(id, name, description) values (:id, :name, :description);
            '''
            self.db.execute(query, data)
        
        self.db.commit()


    def test_get_one_by_correct_id(self):
        response = requests.get(self.url, params={'ACTION': 'ONE', 'id': self.data['id']})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

    def test_get_query(self):
        response = requests.get(self.url, params={'ACTION': 'QUERY'})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])        
        self.assertEqual(11, len(resp['data']))
        

    def test_get_rights_by_correct_id(self):
        response = requests.get(self.url, params={'ACTION': 'RIGHTS', 'id': self.data['id']})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])        