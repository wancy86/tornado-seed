import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Integer, Boolean

from .__basemodel__ import Model, Column
import common.form as form

class Underway(Model):
    '''用户表'''
    __tablename__ = 'todo_underway'

    itemid = Column(String(32), primary_key=True)
    userid = Column(String(32), primary_key=True)
    identity = Column(Integer, autoincrement=True)

    class Form(form.Form):
        itemid = form.String(name="任务ID", minlength=32, maxlength=32, message="不符合规则(32位)！")
        userid = form.String(name="负责人ID", pattern="()|(\w{32})", message="不符合规则(32位)！")