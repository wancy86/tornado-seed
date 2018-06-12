DATABASES = {
    'cs': [
            {
                'dialect': 'mysql',
                'driver': 'pymysql',
                'user': 'root',
                'password': 'max123@max123',
                'host': '127.0.0.1',
                'database': 'cs'
            },
            {
                'dialect': 'mysql',
                'driver': 'pymysql',
                'user': 'root',
                'password': 'max123@max123',
                'host': '127.0.0.1',
                'database': 'cstest'
            }
    ]
} 

INSTALLED_APPS = ['session', 'secu']

# Session 有效时间(分钟)
SESSION_TIMEOUT = 120 

# 此变量决定tornado的运行模式是否为调试模式，如果为真，则文件发生变化服务立刻重启
DEBUG = True 

# 此变量用于自动化测试，根据此变量决定数据库的选择
TEST = 0 

# 此变量用于自动化测试，根据此变量决定自动化测试的端口号
TEST_PORT = '8888' 

# SQLAlchemy log
ECHO = False 

# 此变量表示在程序报错是否会抛出异常,在测试模式用于需要调试的错误
PROCEDURE_ECHO = False

# 系统报错接收邮箱
ERROR_REPORT_RECEIVERS = ['402851315@qq.com', '379842343@qq.com', '737633175@qq.com', 'wancy86@126.com']

HTTPS_KEY_PATH = '/home/ubuntu/sites/cert/localhost.key'
HTTPS_CRT_PATH = '/home/ubuntu/sites/cert/localhost.crt'

# # 网易短信: 国学
# SMS = {
#     'URL': 'https://api.netease.im/sms/sendcode.action',
#     'AppKey': 'f643a4b27d11876c1e125d08ad9befe6',
#     'AppSecret':'8343544a1549',
#     'Type': {
#         'login': '4042090', #登陆
#         'get-money': '3982120', # 提现申请
#         'change-phone': '4042091', # 更换手机
#         'buy-sucess': '4102132', # 购买成功 
#     }
# }

# # 微信配置基础数据
# WPC = {
#     'APPID': 'wx53c18f32ad626eb8',
#     'APPSECRET': 'ff45bca0fec005462e1d01a9e55182fd',
#     'MCHID': '1397809602',
#     'KEY': 'a7fab967242e4c438a2ba95b9d4db287',
#     'GOODDESC': '泽慧国学-国学课程',
#     'NOTIFY_URL': 'https://service.huizeguoxue.com/service/applesson/wechatordernotice', 
# }

STATIC = {
    # 访问路径
    'URL': 'http://192.168.1.54:8080/',

    # 本地存储路径
    'LOCALPATH': '/home/max/sites/cs/services/medias',

    # 远程存储路径
    'REMOTES': [
    ]
}