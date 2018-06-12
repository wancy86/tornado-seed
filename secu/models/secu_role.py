import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Integer, Boolean
from sqlalchemy import Column, ForeignKey

from .__basemodel__ import Model, Column
import common.form as form

class Role(Model):
    '''角色表'''
    __tablename__ = 'secu_role'

    id = Column(String(36), default=lambda: str(uuid.uuid4()).replace('-', ''), primary_key=True)
    name = Column(String(50))
    description = Column(String(500))
    rights = Column(String(10000))

    class Form(form.Form):
        name = form.String(name="角色名称", minlength=1, maxlength=50, message="不符合规则(1-50位)！")
        description = form.String(name="角色描述", nullable=True, maxlength=500, message="不符合规则(0-500位)！")
        rights = form.String(name="权限", nullable=True, maxlength=9999, message="不符合规则！")