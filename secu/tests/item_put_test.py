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

        self.db.commit()   
    def test_by_correct_info(self):
        self.data["title"] = "新的任务名称"

        self.data["person_in_charges"] = [
            {"itemid": "337b70d58cf841759ca0469fe7109a2e", "itemstatus": "需求评审", "person_in_charge": "556a41ea4f48432d84a8e973bc03c3ec"}, 
            {"itemid": "337b70d58cf841759ca0469fe7109a2e", "itemstatus": "代码开发", "person_in_charge": "68AB8F2982D04D8AA75EF64A52E3301E"},
            {"itemid": "337b70d58cf841759ca0469fe7109a2e", "itemstatus": "代码评审", "person_in_charge": "9b06a4029b7a4fb1869b71a44c32e8b2"}
        ]

        response = requests.put(self.url, json=self.data)
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select title from todo_item;
        '''
        result = self.db.execute(query).scalar()
        self.assertEqual('新的任务名称', result)

        query = '''
            select * from todo_person_in_charge;
        '''
        result = json_by_result(self.db.execute(query).fetchall())
        self.assertEqual(3, len(result))