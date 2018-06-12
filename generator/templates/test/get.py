import requests
from .__init__ import Prepare

'''
本代码自动生成
'''
class T(Prepare):

    @property
    def path(self):
        return '/service/[app_name]/[model_name]'

    def test_action_one(self):
        self.BODY['ACTION'] = 'ONE'
        response = requests.get(self.url, params=self.BODY)

        # 检查状态码及返回码
        obj = self.check(response)

        # 检查返回的数据
        self.assertTrue(obj['data'] is not None)

    def test_action_all(self):
        self.BODY['ACTION'] = 'QUERY'
        response = requests.get(self.url, params=self.BODY)

        # 检查状态码及返回码
        obj = self.check(response)

        # 检查返回的数据
        self.assertTrue(len(obj['data']) > 0)        
