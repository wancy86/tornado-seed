import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Integer, Boolean

from .__basemodel__ import Model, Column
import common.form as form

class FavoriteItem(Model):
    ''' '''
    __tablename__ = 'todo_favorite_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    itemid = Column(String(32))
    userid = Column(String(32))

    class Form(form.Form):
        itemid = form.String(name="任务ID", minlength=32, maxlength=32, message="不符合规则(32位)！")
        userid = form.String(name="userID", pattern="()|(\w{32})", message="不符合规则(32位)！")