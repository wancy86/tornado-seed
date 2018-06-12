from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import AbstractConcreteBase
import sqlalchemy
from sqlalchemy import DateTime, String, Integer
from datetime import datetime
import uuid

def Column(*args,**kwargs):
    kwargs["nullable"] = kwargs.get("nullable", False)

    if isinstance(args[0], String):
        kwargs["default"] = kwargs.get("default", '')  

    if str(args[0]).find('Integer') >= 0:
        kwargs["default"] = kwargs.get("default", 0)              

    return sqlalchemy.Column(*args,**kwargs)

Base = declarative_base()

class Model(AbstractConcreteBase, Base):
    entry_date = Column(DateTime(), default=datetime.now)
    entry_user = Column(String(36))

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