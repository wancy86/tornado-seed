from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy import DateTime, Column, String, Integer
from datetime import datetime
import uuid


Base = declarative_base()

class Model(AbstractConcreteBase, Base):
    entry_date = Column(DateTime(), onupdate=datetime.now)
    entry_user = Column(String(36), default='')

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

    @property
    def json(self, format='yyyy-MM-dd HH:mm'):
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    data[key] = '{}-{}-{} {}:{}'.format(
                        value.year, value.month, value.day, value.hour, value.minute)
                elif value is None:
                    data[key] = ''
                else:
                    data[key] = str(value)
        return data

    def jn(self, *args):
        data = {}
        for key, value in self.__dict__.items():
            if args and key not in args:
                continue
            else:
                if isinstance(value, datetime):
                    data[key] = '{}-{}-{} {}:{}'.format(
                        value.year, value.month, value.day, value.hour, value.minute)
                else:
                    data[key] = str(value)
        return data