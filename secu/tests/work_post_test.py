import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common
from common.json import json_by_result

class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/work'

    def setUp(self):
        super().setUp()
        self.data = {
            "itemid": "938a2bf88b2b48fa9ccb92ec4dc5cbfd",
            "desp": "工作内容",
            "duration": "120"
        }

    def test_by_correct_info(self):
        response = requests.post(self.url, json=self.data)
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select * from todo_work where itemid=:itemid;
        '''

        result = json_by_result(self.db.execute(query, self.data).fetchall())
        self.assertEqual(1, len(result))

    def test_by_invalid_duration(self):
        self.data['duration'] = 500
        response = requests.post(self.url, json=self.data)
        resp = response.json()
        self.assertEqual('100', resp['code'])

        query = '''
            select * from todo_work where itemid=:itemid;
        '''

        result = json_by_result(self.db.execute(query, self.data).fetchall())
        self.assertEqual(0, len(result))        
