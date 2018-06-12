'''
公众账号ID  appid   是   String(32)  wxd678efh567hg6787  微信支付分配的公众账号ID（企业号corpid即为此appId）
商户号 mch_id  是   String(32)  1230000109  微信支付分配的商户号
随机字符串   nonce_str   是   String(32)  5K8264ILTKCH16CQ2502SI8ZNMTM67VS    随机字符串，长度要求在32位以内。推荐随机数生成算法
签名  sign    是   String(32)  C380BEC2BFD727A4B6845133519F3AD6    通过签名算法计算得出的签名值，详见签名生成算法

商品描述    body    是   String(128) 腾讯充值中心-QQ会员充值   
商户订单号   out_trade_no    是   String(32)  20150806125346  商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*@ ，且在同一个商户号下唯一。详见商户订单号
标价金额    total_fee   是   Int 88  订单总金额，单位为分，详见支付金额
终端IP    spbill_create_ip    是   String(16)  123.12.12.123   APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP。
通知地址    notify_url  是   String(256) http://www.weixin.qq.com/wxpay/pay.php  异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。
交易类型    trade_type  是   String(16)  JSAPI   取值如下：JSAPI，NATIVE，APP等，说明详见参数规定  
'''
# https://api.mch.weixin.qq.com/pay/unifiedorder

import copy
import uuid
from common import encryption
import requests
import json
import config


class Utility:

    @classmethod
    def getnoncestr(cls):
        return str(uuid.uuid4()).replace('-', '')

    @classmethod
    def getxml(cls, kwargs):

        kwargs['sign'] = Utility.getSign(kwargs)

        # 生成xml
        xml = ''
        for key, value in kwargs.items():
            xml += '<{0}>{1}</{0}>'.format(key, value)
        xml = '<xml>{0}</xml>'.format(xml)

        print('xml:'+xml)
        return xml

    @classmethod
    def getSign(cls, kwargs):

        # 计算签名
        keys, paras = sorted(kwargs), []
        paras = ['{}={}'.format(key, kwargs[key]) for key in keys if key != 'appkey']  # and kwargs[key] != '']
        stringA = '&'.join(paras)

        stringSignTemp = stringA + '&key=' + config.WPC['KEY']
        sign = encryption.MD5(stringSignTemp).upper()

        print('sign:'+sign)

        return sign

    @classmethod
    def getOpenID(cls, kwargs):
        param = {
            'code': kwargs['code'],
            'appid': config.WPC['APPID'],
            'secret': config.WPC['APPSECRET'],
            'grant_type': 'authorization_code',
        }

        # 通过code获取access_token
        openIdUrl = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        resp = requests.get(openIdUrl, params=param)
        # {openid, accss_token, refresh_token, openid, scope, expires_in}
        # openId = json.loads(resp.text)['openid']
        print(resp.text)
        return resp.text
