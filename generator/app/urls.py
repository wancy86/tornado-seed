from . import controls

urlpatterns = [

    # (r'/service/app/model', handler),
]

'''
JSONResponse基本结构：
{
    "code":"\d{3}",
    "msg": "message",
    "data": [] or {}
}

code通用规则：
    0\d\d：其中000表示请求成功，其它的情况表示非预期的请求失败
    1\d\d：验证不通过
    2\d\d：200表示session过期, 201表示窃取CSRF攻击
    5\d\d：表示服务器内部错误

'''
