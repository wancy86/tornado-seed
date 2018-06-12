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
        self.data['desp'] = str(uuid.uuid4())
        response = requests.put(self.url, json=self.data)
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select desp from todo_work where id=:id;
        '''

        result = self.db.execute(query, self.data).scalar()
        self.db.commit()
        self.assertEqual(self.data['desp'], result)