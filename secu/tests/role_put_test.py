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

    def test_role_update_by_correct_id(self):
        self.data['ACTION'] = 'ROLE'
        self.data['description'] = '添加项目，通常用以区分不同的客户。'
        response = requests.put(self.url, json=self.data)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select description from secu_role where id=:id;
        '''
        result = self.db.execute(query, self.data).scalar()
        self.assertEqual('添加项目，通常用以区分不同的客户。', result)

    def test_change_right(self):
        # 第一次添加权限
        first = {
            'ACTION': 'ADD-RIGHT',
            'id': 'a266f06037d043fbb4575a75be87f4ba',
            'right': '13afbe46cd374d3ab6b0130319bd7133' 
        }
        response = requests.put(self.url, json=first)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select rights from secu_role where id=:id;
        '''
        result = self.db.execute(query, first).scalar()
        self.db.commit()
        self.assertEqual('13afbe46cd374d3ab6b0130319bd7133', result)    

        # 第二次添加权限
        second = {
            'ACTION': 'ADD-RIGHT',
            'id': 'a266f06037d043fbb4575a75be87f4ba',
            'right': '19c3864873aa42f98f38112336f7141b' 
        }
        response = requests.put(self.url, json=second)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select rights from secu_role where id=:id;
        '''
        result = self.db.execute(query, second).scalar()
        self.db.commit()
        self.assertEqual('13afbe46cd374d3ab6b0130319bd7133,19c3864873aa42f98f38112336f7141b', result)      

        # 第三次删除权限
        third = {
            'ACTION': 'REMOVE-RIGHT',
            'id': 'a266f06037d043fbb4575a75be87f4ba',
            'right': '19c3864873aa42f98f38112336f7141b' 
        }
        response = requests.put(self.url, json=third)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select rights from secu_role where id=:id;
        '''
        result = self.db.execute(query, third).scalar()
        self.db.commit()
        self.assertEqual('13afbe46cd374d3ab6b0130319bd7133', result)                    

        