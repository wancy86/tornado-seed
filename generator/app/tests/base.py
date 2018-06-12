import unittest
import requests
import json
import config as conf
import common
from importlib import import_module
from datetime import datetime

class BaseTestCase(unittest.TestCase):

    @property
    def host(self):
        return 'http://localhost:8888'

    @property
    def path(self):
        raise NotImplemented('Please override this property in the child class!')

    @property
    def url(self):
        return self.host + self.path

    @classmethod
    def setUpClass(cls):
        app = import_module(cls.__module__.split('.')[0])
        cls.db = common.db.DB(**conf.DATABASES[app.database][1]).session

    def check(self, response, status_code=200, expected_code='000', **kwargs):
        self.assertEqual(response.status_code, status_code, '请求失败，请检查您的代码！')
        obj = response.json()
        self.assertEqual(obj['code'], expected_code, '请求失败，请检查您代码的逻辑！')
        
        return obj

        

    def tearDown(self):
        # clear database for each test method
        self.db.execute('''
                set foreign_key_checks = 0; 

                delete from session;
                delete from session_data;

                delete from secu_user;
                delete from secu_role;
                delete from secu_right;    
                delete from secu_user_role;
                delete from secu_role_right;

                set foreign_key_checks = 1;  
        ''')
        self.db.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()


class AuthorizedTestCase(BaseTestCase):

    @property
    def url(self):
        return self.host + self.path + '?session_id=' + self.session_id

    def setUp(self):
        user = {
            'id': '68AB8F29-82D0-4D8A-A75E-F64A52E3301E',
            'email': 'root@quanqingtouru.com',
            'mobile': '13988886666',
            'full_name': '全情投入',
            'pwd':  'quanqingtouru',
            'active': 1
        }

        session = {
            'session_id': '9077B0E7-F9CA-4B78-B197-25DAA76A3716',
            'update_date': datetime.now(),
            'entry_date': datetime.now(),
            'keep_time': 30,
            'k': 'userid',
            'v': user['id']
        }

        # 添加用户以作为当前登陆用户
        self.db.execute('insert into secu_user(id, email, mobile, full_name, pwd, active) values (:id, :email, :mobile, :full_name, :pwd, :active);', user)

        # 添加session以模拟用户登陆
        self.db.execute('insert into session(id, update_date, entry_date, keep_time) values (:session_id, :update_date, :entry_date, :keep_time);', session)
        self.db.execute('insert into session_data(session_id, k, v) values (:session_id, :k, :v);', session)
        self.db.commit()

        # 将用户赋值给实例对象以便访问
        self.session_id = session['session_id']
