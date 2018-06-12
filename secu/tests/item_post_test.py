import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common
from common.json import json_by_result

class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/item'

    def setUp(self):
        super().setUp()
        self.data = {
            "title": "任务名称",
            "projectid": "a6523c40a08f481a92c25c6945dc7b40",
            "desp": "任务描述",
            "cat": "任务种类",
            "status": "任务状态",
            "priority": "优先级",
            "estimated_duration": "120",
            "person_in_charges": [
                {"itemstatus": "需求评审", "person_in_charge": "68AB8F2982D04D8AA75EF64A52E3301E"}, 
                {"itemstatus": "代码开发", "person_in_charge": "68AB8F2982D04D8AA75EF64A52E3301E"}
            ]
        }

    def test_by_correct_info(self):
        response = requests.post(self.url, json=self.data)
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select * from todo_person_in_charge;
        '''

        result = json_by_result(self.db.execute(query).fetchall())
        self.assertEqual(2, len(result))
