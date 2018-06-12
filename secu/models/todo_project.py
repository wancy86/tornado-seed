import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Integer, Boolean

from .__basemodel__ import Model, Column 
import common.form as form


class Project(Model):
    '''用户表'''
    __tablename__ = 'todo_project'

    id = Column(String(32), default=lambda: str(uuid.uuid4()).replace('-', ''), primary_key=True)
    name = Column(String(100))
    desp = Column(String(1000))
    cats = Column(String(1000))
    statuses = Column(String(1000))
    priorities = Column(String(1000))
    identity = Column(Integer, autoincrement=True)

    options = {
        "cats": "需求, 缺陷",
        "statuses": "尚未分配, 已分配, 开发中, 开发完成, 测试中, 测试完成, 已验收",
        "priorities": "高, 中, 低",
    }
    
    class Form(form.Form):
        name = form.String(name="项目名称", minlength=2, maxlength=100, message="不符合规则(2-100位)！")
        desp = form.String(name="项目描述", maxlength=1000, message="不符合规则(0-1000位)！")
        cats = form.String(name="项目任务种类", maxlength=1000, message="不符合规则(0-1000位)！")
        statuses = form.String(name="项目任务状态", maxlength=1000, message="不符合规则(0-1000位)！")
        priorities = form.String(name="项目优先级", maxlength=1000, message="不符合规则(0-1000位)！")

    # class PutForm(form.Form):
    #     id = form.String(
    #         pattern="[\w-]{32}",
    #         nullable=True,
    #         example="1131FE28-EABF-4690-B86B-C0FCD3204CA3",
    #         message="非法的用户ID！"
    #     )
    #     username = form.String(
    #         pattern=".{2,18}",
    #         example="someone",
    #         message="用户名长度为2-18个字符！"
    #     )
    #     email = form.Email(
    #         nullable=True,
    #         example="someone@quanqingtouru.com",
    #         message="请输入有效的电子邮件！"
    #     )
    #     mobile = form.Mobile(
    #         example="18877776666",
    #         message="请输入有效的手机号码！"
    #     )
    #     fullname = form.String(
    #         minlength=2,
    #         maxlength=10,
    #         example="Someone",
    #         message="请输入有效的姓名！"
    #     )
    #     roles = form.String(
    #         pattern='[\w-]+',
    #         example="[some-role]",
    #         message="请选择用户角色！"
    #     )
