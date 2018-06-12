import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common


class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/underway'

    def setUp(self):
        super().setUp()
        self.data = {
            "itemid": "a6523c40a08f481a92c25c6945dc7b41",
            "userid": self.user['id']
        }

        query = '''
            insert into todo_underway(itemid, userid) values (:itemid, :userid);
        '''
        self.db.execute(query, self.data)
        self.db.commit()

    def test_by_correct_info(self):
        response = requests.delete(self.url, json={'itemid': self.data['itemid']})
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

        query = '''
            select count(1) from todo_underway where userid=:userid and itemid=:itemid;
        '''

        result = self.db.execute(query, self.data).scalar()

        self.assertEqual(0, result)
