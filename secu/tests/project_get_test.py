import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
from common.json import json_by_result


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
            'entry_user': self.user['id']
        }

        query = '''
            insert into todo_project(id, name, desp, cats, statuses, priorities, entry_user)values
            (:id, :name, :desp, :cats, :statuses, :priorities, :entry_user);
        '''

        self.db.execute(query, self.data)
        self.db.commit()

    def test_get_data_by_missing_action(self):
        response = requests.get(self.url)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('缺失参数ACTION', resp['msg'])

    def test_get_data_by_correct_id(self):
        response = requests.get(self.url, params={'ACTION': 'ONE', 'id': self.data['id']})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual(None, resp['msg'])
        self.assertEqual('000', resp['code'])

    def test_get_data_by_wrong_id(self):
        response = requests.get(self.url, params={'ACTION': 'ONE', 'id': str(uuid.uuid4).replace('-', '')})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('你查询的记录不存在！', resp['msg'])
        self.assertEqual('001', resp['code'])   

    def test_get_data_list(self):
        response = requests.get(self.url, params={'ACTION': 'QUERY'})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()

    def test_get_options(self):
        response = requests.get(self.url, params={'ACTION': 'OPTIONS'})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()        
        self.assertEqual('000', resp['code'])