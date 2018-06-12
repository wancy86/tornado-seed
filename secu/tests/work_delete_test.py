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
            "id": "2df55516c635408c954f230240877f2a",
            "itemid": "938a2bf88b2b48fa9ccb92ec4dc5cbfd",
            "desp": "工作内容",
            "duration": "120",
            "entry_user": self.user['id']
        }

        query = '''
            insert into todo_work(id, itemid, desp, duration, entry_user)values(:id, :itemid, :desp, :duration, :entry_user);
        '''

        self.db.execute(query, self.data)
        self.db.commit()

    def test_by_correct_info(self):
        response = requests.delete(self.url, json={"id": self.data["id"]})
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select * from todo_work where itemid=:itemid;
        '''

        result = json_by_result(self.db.execute(query, self.data).fetchall())
        self.db.commit()
        self.assertEqual(0, len(result))

    def test_by_no_exist_id(self):
        response = requests.delete(self.url, json={"id": str(uuid.uuid4()).replace('-', '')})
        resp = response.json()
        self.assertEqual('001', resp['code'])

        query = '''
            select * from todo_work where itemid=:itemid;
        '''

        result = json_by_result(self.db.execute(query, self.data).fetchall())
        self.db.commit()
        self.assertEqual(1, len(result))        

  
