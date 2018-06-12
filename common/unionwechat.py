
import copy
import uuid
import encryption
import requests

# appid=00000000
# &body=商品名称
# &cusid=990440153996000
# &key=43df939f1e7f5c6909b3f4b63f893994
# &paytype=0
# &randomstr=1450432107647
# &remark=备注信息
# &reqsn=1450432107647
# &trxamt=1

UnifieOrderRequest = {
    'appid': '00000000', # 公众账号ID
    'cusid': '990440153996000', # 商户号
    'key': '43df939f1e7f5c6909b3f4b63f893994',
    'notify_url': 'http://www.quanqingtouru.com/lesson-order', # 交易结果通知地址
}

class WechatPay:

    def __init__(self, orderid, orderprice, clientip, *args, **kwargs):
        self.url = 'https://vsp.allinpay.com/apiweb/unitorder/pay' # 统一订单请求地址
        self.UOR = copy.copy(UnifieOrderRequest)

        # 交易信息
        self.UOR['paytype'] = 'W02' # 交易方式
        self.UOR['reqsn'] = orderid # 商户交易订单号
        self.UOR['trxamt'] = orderprice * 100 # 交易金额(分)

        # 辅助信息
        self.UOR['acct'] = 'openid' # 用户的微信openid
        self.UOR['randomstr'] = Utility.getnoncestr()

        # 生成签名
        self.UOR['sign'] = Utility.getsign(self.UOR)
        del self.UOR['key']

    def make_unifie_order(self):    
        response = requests.post(self.url, data=self.UOR)
        print(response.text)

class Utility:

    @classmethod
    def getnoncestr(cls):
        return str(uuid.uuid4()).replace('-', '')

    @classmethod    
    def getsign(cls, kwargs):
        paras = [ '{}={}'.format(key, kwargs[key]) for key in sorted(kwargs) ] #and kwargs[key] != '']
        string = '&'.join(paras)
        sign = encryption.MD5(string).upper()
        
        return sign

guoxue = WechatPay(1000, 580, '127.0.0.1')  
guoxue.make_unifie_order()

   

