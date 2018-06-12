import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Integer, Boolean

from .__basemodel__ import Model, Column
import common.form as form


class Item(Model):
    '''用户表'''
    __tablename__ = 'todo_item'

    id = Column(String(32), default=lambda: str(uuid.uuid4()).replace('-', ''), primary_key=True)
    projectid = Column(String(36))
    title = Column(String(255))
    desp = Column(String(10000))
    cat = Column(String(100))
    status = Column(String(100))
    priority = Column(String(100))
    estimated_duration = Column(Integer)
    identity = Column(Integer, autoincrement=True)

    class Form(form.Form):
        projectid = form.String(name="项目ID", minlength=32, maxlength=32, message="不符合规则(32位)！")
        title = form.String(name="任务名称", minlength=2, maxlength=255, message="不符合规则(2-100位)！")
        desp = form.String(name="任务描述", maxlength=10000, message="不符合规则(0-1000位)！")
        cat = form.String(name="任务种类", maxlength=100, message="不符合规则(0-100位)！")
        status = form.String(name="任务状态", maxlength=100, message="不符合规则(0-100位)！")
        priority = form.String(name="优先级", maxlength=100, message="不符合规则(0-100位)！")
        estimated_duration = form.Integer(name="预估时间", message="不符合规则(整数)！")
        person_in_charges = form.List(name="负责人", minlength=1, maxlength=100)


class PersonInCharge(Model):
    '''用户表'''
    __tablename__ = 'todo_person_in_charge'

    itemid = Column(String(32), primary_key=True)
    itemstatus = Column(String(100), primary_key=True)
    person_in_charge = Column(String(32), primary_key=True)
    sequence = Column(Integer)
    identity = Column(Integer, autoincrement=True)

    class Form(form.Form):
        itemid = form.String(name="任务ID", minlength=32, maxlength=32, message="不符合规则(32位)！")
        itemstatus = form.String(name="任务状态", minlength=1, maxlength=100, message="不符合规则(1-100位)！")
        person_in_charge = form.String(name="负责人ID", pattern="()|(\w{32})", message="不符合规则(32位)！")
        sequence = form.Integer(name="排序", message="不符合规则(整数)！")