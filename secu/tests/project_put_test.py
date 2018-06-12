import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common


class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/project'

    def setUp(self):
        super().setUp()
        self.data = {
            'id': 'a6523c40a08f481a92c25c6945dc7b40',
            'name': '项目名称',
            'desp': '项目描述',
            'cats': '项目任务种类',
            'statuses': '项目任务状态',
            'priorities': '项目优先级',
        }

        query = '''
            insert into todo_project(id, name, desp, cats, statuses, priorities)values
            (:id, :name, :desp, :cats, :statuses, :priorities)
        '''

        self.db.execute(query, self.data)
        self.db.commit()

    def test_by_correct_info(self):
        self.data['name'] = '项目新名称'
        response = requests.put(self.url, json=self.data)
        self.assertNotEqual(response.text, '', '返回值为空！')

        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select name from todo_project where id = :id;
        '''

        result = self.db.execute(query, self.data).scalar()
        self.assertEqual('项目新名称', result)

    def test_by_wrong_id(self):
        self.data['id'] = str(uuid.uuid4()).replace('-', '')
        response = requests.put(self.url, json=self.data)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('001', resp['code'])        
