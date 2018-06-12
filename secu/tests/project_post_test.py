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
            'name': '项目名称',
            'desp': '项目描述',
            'cats': '项目任务种类',
            'statuses': '项目任务状态',
            'priorities': '项目优先级',
        }

    def test_by_correct_info(self):
        response = requests.post(self.url, json=self.data)
        resp =response.json()
        self.assertEqual('000', resp['code'])

    def test_by_missing_desp(self):
        del self.data['desp']
        response = requests.post(self.url, json=self.data)
        resp = response.json()
        self.assertEqual('100', resp['code'])     

    def test_by_invalid_desp(self):
        desp = ''
        for i in range(1001):
            desp = desp + str(i)
        self.data['desp'] = desp    
        response = requests.post(self.url, json=self.data)
        resp = response.json()
        self.assertEqual('100', resp['code'])      
