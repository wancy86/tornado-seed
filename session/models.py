from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
import uuid


Base = declarative_base()

class Model(AbstractConcreteBase, Base):

    entry_date = Column(DateTime(), default=datetime.now)

class SessionModel(Model):
    __tablename__ = 'session'

    id = Column(String(36), default=lambda:str(uuid.uuid4()), primary_key=True)
    update_date = Column(DateTime(), default=datetime.now)
    keep_time = Column(Integer, default=30)    

class SessionData(Model):
    __tablename__ = 'session_data'

    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), ForeignKey('session.id'), index=True)
    k = Column(String(8000), default='')
    v = Column(String(8000), default='')
    