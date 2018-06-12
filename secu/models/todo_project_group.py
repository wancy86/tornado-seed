import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, Integer, Boolean

from .__basemodel__ import Model, Column
import common.form as form


class ProjectGroup(Model):
    __tablename__ = 'todo_project_group'

    userid = Column(String(36), primary_key=True)
    projectid = Column(String(36), primary_key=True)
    identity = Column(Integer, autoincrement=True)

    class Form(form.Form):
        userid = form.String(name="用户ID", minlength=32, maxlength=32, message="不符合规则(32位)！")
        projectid = form.String(name="项目ID", minlength=32, maxlength=32, message="不符合规则(32位)！")
        entry_user = form.String(name="当前使用者ID", minlength=32, maxlength=32, message="不符合规则(32位)！")
