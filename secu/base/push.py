import jpush

import config
from config import JPUSH

class Jpushhelper:

    def __init__(self, app_key, master_secret, db=None, **kwargs):
        self._jpush = jpush.JPush(app_key, master_secret)
        # self._jpush.set_logging("DEBUG")
        self.db = db

    def all(self, alert, extras):
        ''' 发送推送给所有用户
            alert  消息内容
            extras 附带参数(给前端做业务逻辑判断)'''
        push = self._jpush.create_push()
        push.audience = jpush.all_
        android = jpush.android(alert=alert, extras=extras)
        ios = jpush.ios(alert=alert, extras=extras)
        push.notification = jpush.notification(alert=alert, android=android, ios=ios)
        push.platform = jpush.all_
        try:
            response = push.send()
            print(response)
            return '000'
        except Exception:
            print(Exception)
            return '002'

    def alias(self, alert, extras, alias=[]):
        ''' 发送推送给指定用户
            alert  消息内容
            extras 附带参数(给前端做业务逻辑判断)
            alias  用户(电话号码)'''
        push = self._jpush.create_push()
        push.audience = jpush.audience({"alias": alias})
        push.options = {"apns_production": config.APNS_PRODUCTION}
        android = jpush.android(alert=alert, extras=extras)
        ios = jpush.ios(alert=alert, extras=extras)
        push.notification = jpush.notification(alert=alert, android=android, ios=ios)
        push.platform = jpush.all_
        try:
            response = push.send()
            print(response)
            return '000'
        except Exception:
            print(Exception)
            return '002'

# Jpushhelper().all('Hello world with audience!', {'state': 'a/b/c'})
# print(Jpushhelper().alias('Hello world with audience!', {'state': 'a/b/c'}, ['18577766626']))

push = Jpushhelper(**JPUSH)

# print(push.alias('111!', {'state': 'a/b/c'}, ['15659862720']))
# print(push.all('Hello world with audience!', {'state': 'a/b/c'}))