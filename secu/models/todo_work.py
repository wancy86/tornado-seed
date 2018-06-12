import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, Integer, Boolean

from .__basemodel__ import Model, Column 
import common.form as form

class Work(Model):
    '''工作日志表'''
    __tablename__ = 'todo_work'

    id = Column(String(32), default=lambda: str(uuid.uuid4()).replace('-', ''), primary_key=True)
    itemid = Column(String(32))
    desp = Column(String(1000))
    duration = Column(Integer)
    identity = Column(Integer, autoincrement=True)

    class Form(form.Form):
        itemid = form.String(name="任务ID", pattern="[a-zA-Z0-9]{32}", message="不符合规则(32位)！")
        desp = form.String(name="工作内容", maxlength=1000, message="不符合规则(0-1000位)！")
        duration = form.Integer(name="消耗时间", maxvalue=480, message="不符合规则(0-480)！")
        entry_user = form.String(name="任务ID", pattern="[a-zA-Z0-9]{32}", message="不符合规则(32位)！")

    class PutForm(form.Form):
        desp = form.String(name="工作内容", maxlength=1000, message="不符合规则(0-1000位)！")
        duration = form.Integer(name="消耗时间", maxvalue=480, message="不符合规则(0-480)！")        
