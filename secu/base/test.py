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
        return 'http://localhost:' + conf.TEST_PORT

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
        if obj['code'] != expected_code:
            print(obj)
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
                
                delete from todo_project;
                delete from todo_item;
                delete from todo_person_in_charge;
                delete from todo_work;
                delete from todo_underway;
                delete from todo_project_group;
                delete from todo_favorite_item;
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
            'id': '68AB8F2982D04D8AA75EF64A52E3301E',
            'username': 'root',
            'email': 'root@quanqingtouru.com',
            'mobile': '13988886666',
            'fullname': '全情投入',
            'pwd': common.encryption.MD5('quanqingtouru'),
            'password': 'quanqingtouru',
            'active': 1
        }

        session = {
            'session_id': '9077B0E7F9CA4B78B19725DAA76A3716',
            'update_date': datetime.now(),
            'entry_date': datetime.now(),
            'keep_time': 30,
            'k': 'userid',
            'v': user['id']
        }

        # 添加用户以作为当前登陆用户
        self.db.execute('insert into secu_user(id, username, email, mobile, fullname, pwd, active) values (:id, :username, :email, :mobile, :fullname, :pwd, :active);', user)

        # 添加session以模拟用户登陆
        self.db.execute('insert into session(id, update_date, entry_date, keep_time) values (:session_id, :update_date, :entry_date, :keep_time);', session)
        self.db.execute('insert into session_data(session_id, k, v) values (:session_id, :k, :v);', session)
        self.db.commit()

        # 将用户赋值给实例对象以便访问
        self.session_id = session['session_id']
        self.user = user
