import requests
from ..base.test import BaseTestCase, AuthorizedTestCase
import uuid
import common

class T(AuthorizedTestCase):

    @property
    def path(self):
        return '/service/secu/project-group'

    def setUp(self):
        super().setUp()

        # 添加用户
        user_data = {
            'id': 'a9490c270e544625a6ca906695a34b77',
            'username': 'Jack',
            'email': 'jack@qq.com',
            'mobile': '19988888888',
            'pwd': '123456',
            'fullname': '姚大力',
            'roles': '',
            'active': '1'
        }

        query = '''
            insert into secu_user(id, username, email, mobile, fullname, pwd, active) values 
            (:id, :username, :email, :mobile, :fullname, :pwd, :active);
        '''
        self.db.execute(query, user_data)

        # 添加项目
        project_data = {
            'id': 'a6523c40a08f481a92c25c6945dc7b40',
            'name': '项目名称',
            'desp': '项目描述',
            'cats': '项目任务种类',
            'statuses': '项目任务状态',
            'priorities': '项目优先级',
            'entry_user': self.user['id']
        }

        query = '''
            insert into todo_project(id, name, desp, cats, statuses, priorities, entry_user)values
            (:id, :name, :desp, :cats, :statuses, :priorities, :entry_user);
        '''

        self.db.execute(query, project_data)
        self.db.commit() 

        # 添加项目组
        self.data = {
            'userid': user_data['id'],
            'projectid': project_data['id'],
            # 'entry_user': self.user['id']
        }

        # query = '''
        #     insert into todo_project_group(userid, projectid, entry_user)values
        #     (:userid, :projectid, :entry_user);
        # '''

        # self.db.execute(query, self.data)
        # self.db.commit()           


    def test_by_correct_info(self):
        response = requests.post(self.url, json=self.data)
        self.assertNotEqual(response.text, '', '返回值为空！')
        resp = response.json()
        self.assertEqual('000', resp['code'])

