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

        # 插入一条记录
        self.data = {
            "id": "337b70d58cf841759ca0469fe7109a2e",
            "projectid": "a6523c40a08f481a92c25c6945dc7b40", 
            "title": "任务名称",
            "desp": "任务描述",
            "cat": "任务种类",
            "status": "任务状态",
            "priority": "优先级",
            "estimated_duration": "120",
            "person_in_charges": [
                {"itemid": "337b70d58cf841759ca0469fe7109a2e", "itemstatus": "需求评审", "person_in_charge": "556a41ea4f48432d84a8e973bc03c3ec"}, 
                {"itemid": "337b70d58cf841759ca0469fe7109a2e", "itemstatus": "代码开发", "person_in_charge": "68AB8F2982D04D8AA75EF64A52E3301E"}
            ]
        }

        query = '''
            insert into todo_item(id, projectid, title, desp, cat, status, priority, estimated_duration)values
            (:id, :projectid, :title, :desp, :cat, :status, :priority, :estimated_duration);
        '''
        self.db.execute(query, self.data)

        query = '''
            insert into todo_person_in_charge(itemid, itemstatus, person_in_charge)values
            (:itemid, :itemstatus, :person_in_charge);
        '''
        for x in self.data['person_in_charges']:
            self.db.execute(query, x)        

        # 插入30条记录
        for x in range(30):
            data = {
                "id": str(uuid.uuid4()).replace('-', ''),
                "projectid": "a6523c40a08f481a92c25c6945dc7b40", 
                "title": "第一任务名称",
                "desp": "任务描述",
                "cat": "任务种类",
                "status": "任务状态",
                "priority": "优先级",
                "estimated_duration": "120",
                "person_in_charges": [
                    {"itemid": str(uuid.uuid4()).replace('-', ''), "itemstatus": "需求评审", "person_in_charge": "556a41ea4f48432d84a8e973bc03c3ec"}, 
                    {"itemid": str(uuid.uuid4()).replace('-', ''), "itemstatus": "代码开发", "person_in_charge": "68AB8F2982D04D8AA75EF64A52E3301E"}
                ]
            }

            query = '''
                insert into todo_item(id, projectid, title, desp, cat, status, priority, estimated_duration)values
                (:id, :projectid, :title, :desp, :cat, :status, :priority, :estimated_duration);
            '''
            self.db.execute(query, data)

            query = '''
                insert into todo_person_in_charge(itemid, itemstatus, person_in_charge)values
                (:itemid, :itemstatus, :person_in_charge);
            '''
            for x in data['person_in_charges']:
                self.db.execute(query, x)      
        self.db.commit()  

    def test_by_action_one(self):
        response = requests.get(self.url, params={ 'ACTION': 'ONE', 'id': self.data['id']})
        resp = response.json()
        self.assertEqual('000', resp['code'])
        self.assertEqual(len(resp['data']['person_in_charges']), 2)

    def test_by_action_query(self):
        response = requests.get(self.url, params={'ACTION': 'QUERY', 'title': '第一'})
        resp = response.json()
        self.assertEqual('000', resp['code'])
        self.assertEqual(resp['data']['count'], 30)
