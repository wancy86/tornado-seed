import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common
import copy
from random import randint
from common.json import json_by_result
from datetime import datetime, timedelta

class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/work'

    def setUp(self):
        super().setUp()
        self.data = {
            "id": "2df55516c635408c954f230240877f2a",
            "itemid": "938a2bf88b2b48fa9ccb92ec4dc5cbfd",
            "desp": "工作内容",
            "duration": "120",
            "entry_user": self.user['id'],
            "entry_date": datetime.now()
        }

        query = '''
            insert into todo_work(id, itemid, desp, duration, entry_date, entry_user)values(:id, :itemid, :desp, :duration, :entry_date, :entry_user);
        '''

        # 添加一条记录
        self.db.execute(query, self.data)


        # 添加31条记录
        data = copy.copy(self.data)
        for x in range(31):
            data['id'] = str(uuid.uuid4()).replace('-', '')
            data['desp'] = str(randint(10, 15))
            data['entry_date'] = datetime.now() - timedelta(days=x)
            self.db.execute(query, data)

        self.db.commit()

    def test_get_one(self):
        response = requests.get(self.url, params={ "ACTION": "ONE", "id": self.data["id"]})
        resp = response.json()
        self.assertEqual('000', resp['code'], resp['msg'])
        self.assertEqual('工作内容', resp['data']['desp'])

    def test_get_list(self):
        response = requests.get(self.url, params={ "ACTION": "QUERY", "itemid": self.data["itemid"]})
        resp = response.json()
        self.assertEqual('000', resp['code'], resp['msg'])
        self.assertEqual(32, resp['data']['count'])      


    def test_get_myown_list_with_no_filter(self):
        params = {
            "ACTION": "MYLOGS",
        }
        response = requests.get(self.url, params=params)
        self.assertNotEqual(response.text, '', '无返回')
        resp = response.json()
        self.assertEqual('000', resp['code'], resp['msg'])
        self.assertEqual(10, len(resp['data']['list']))    

    def test_get_myown_list_with_filter(self):
        params = {
            "ACTION": "MYLOGS",
            "min_entry_date": "2018-3-1",
            "max_entry_date": "2018-3-3"
        }
        response = requests.get(self.url, params=params)
        self.assertNotEqual(response.text, '', '无返回')
        resp = response.json()
        self.assertEqual('000', resp['code'], resp['msg'])
        self.assertEqual(3, len(resp['data']['list']))                      


  
