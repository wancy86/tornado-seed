# https://cryptography.io/en/latest/fernet/#

import hashlib
from cryptography.fernet import Fernet

fernetkey = 'juwBY-KjN1kUKrB0BiW609cIEsMV0t6G-T9emST7GwI='

# 获取MD5
def MD5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()

# 获取SHA256
def SHA256(str):
    sha = hashlib.sha256()
    sha.update(str.encode('utf-8'))
    return sha.hexdigest()

# 加密
def encrypt(str):
    f = Fernet(fernetkey)
    return f.encrypt(str.encode('utf-8'))

# 解密
def decrypt(str):
    f = Fernet(fernetkey)
    return f.decrypt(str).decode('utf-8')

# a = fernetencrypt('--')
# b = fernetdecrypt(a)
# print('a:', a)
# print('b:', b)



