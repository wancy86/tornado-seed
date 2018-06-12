import requests
from .__init__ import Prepare

'''
本代码自动生成
'''
class T(Prepare):

    @property
    def path(self):
        return '/service/[app_name]/[model_name]'

    # 常规流程   
    def test_general_process(self):
        response = requests.post(self.url, json=self.BODY)
        obj = self.check(response)

        # 检查数据库更新
        result = self.db.execute('[CHECKSQL]', self.BODY).scalar()
        self.assertEqual(result, 1)
    

