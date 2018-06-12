import uuid
from datetime import datetime

import sqlalchemy as sql
from sqlalchemy import DateTime, String, Integer, Boolean

from .__basemodel__ import Model, Column
import common.form as form


class User(Model):
    '''用户表'''
    __tablename__ = 'secu_user'

    id = Column(String(32), default=lambda: str(uuid.uuid4()).replace('-', ''), primary_key=True)
    username = Column(String(100))
    email = Column(String(100))
    mobile = Column(String(100))
    pwd = Column(String(100), )
    active = Column(Integer, default=1)
    fullname = Column(String(100))
    roles = Column(String(10000))
    wrongtimes = Column(Integer)
    identity = Column(Integer, autoincrement=True)

    class Form(form.Form):
        username = form.String(name="用户名", minlength=0, maxlength=20, message="不符合规则(0-20位)")
        email = form.Email(name="邮箱", nullable=True)
        mobile = form.Mobile(name="手机号码")
        pwd = form.String(name="密码", minlength=6, maxlength=18, message="请输入有效的密码(6-18位)！")
        fullname = form.String(name="姓名", minlength=2, maxlength=6, message="不符合规则(2-6位)")
        roles = form.String(name="角色", nullable=True, minlength=0, maxlength=10000, message="不符合规则(0-10000位)")
    class LoginForm(form.Form):
        mobile = form.Mobile(name="手机号码")
        pwd = form.String(name="密码", minlength=6, maxlength=18, message="请输入有效的密码(6-18位)！")
