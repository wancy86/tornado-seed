import requests
from ..base.test import BaseTestCase
import uuid
import common

class T(BaseTestCase):

    @property
    def path(self):
        return '/service/secu/login'

    def setUp(self):
        super().setUp()

        query = '''
            insert into secu_user(id, mobile, pwd)values(:id, :mobile, :pwd);
        '''        
        data = {
            'id': str(uuid.uuid4()).replace('-', ''),
            'mobile': '18665369920',
            'pwd': 'yaoguanwei'
        }

        self.db.execute(query, data)
        self.db.commit()
        self.data = data

    def test_by_correct_info(self):
        response = requests.post(self.url, json=self.data)
        resp =response.json()
        self.assertEqual('000', resp['code'])

    def test_by_correct_mobile_wrong_pwd(self):
        self.data['pwd'] = self.data['pwd'] + 'x'
        response = requests.post(self.url, json=self.data)

        resp =response.json()
        self.assertEqual('001', resp['code']) 
