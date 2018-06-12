import json
import uuid
from datetime import datetime, timedelta
from sqlalchemy import desc, and_, update
from .models import SessionModel, SessionData
from session import database
from common.db import DB
from importlib import import_module
import config



class Session:

    @property
    def db(self):
        if not hasattr(self, '_db'):
            app = import_module(self.__module__.split('.')[0])
            conf = import_module('config')
            connection = conf.DATABASES[app.database][conf.TEST]
            setattr(self, '_db', DB(**connection).session)
        
        return getattr(self, '_db')

    def __init__(self, session_id=None):
        self.session_id = session_id
        self.status = 0
        if session_id:
            sm = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
            if sm and abs(datetime.now() - sm.update_date).seconds <= sm.keep_time * 60:
                self.status = 1
            else:
                self.status = 2    # 已经失效

    def __getitem__(self, k):
        if self.status == 1:
            data = self.db.query(SessionData).filter(SessionData.session_id == self.session_id)\
                                             .filter(SessionData.k == k)\
                                             .order_by(SessionData.entry_date.desc())\
                                             .first()
            return data.v if data else None
        else:
            return None

    def __setitem__(self, k, v, keep_time=config.SESSION_TIMEOUT):
        try:
            if self.status == 1:
                data = SessionData(session_id=self.session_id, k=k, v=v)
                self.db.add(data)
                self.db.commit()

            elif self.status in(0, 2):
                sm = SessionModel(keep_time=keep_time)
                self.db.add(sm)
                self.db.commit()

                data = SessionData(session_id=sm.id, k=k, v=v)
                self.db.add(data)
                self.db.commit()

                self.session_id = sm.id
                self.status = 1
        except Exception as e:
            print(e)
            self.db.rollback()

    def dispose(self):
        if self.status == 1:
            sm = self.db.query(SessionModel).filter(SessionModel.id == self.session_id)
            sm.update({'update_date': datetime.now()})
            self.db.commit()
            
        if hasattr(self, '_db'):
            self._db.close()    

    def clear(self):
        if self.status == 1:
            self.db.query(SessionData).filter(SessionData.session_id == self.session_id).delete()
            self.db.commit()

    def abandon(self):
        if self.session_id:
            self.db.query(SessionData).filter(SessionData.session_id == self.session_id).delete()
            self.db.query(SessionModel).filter(SessionModel.id == self.session_id).delete()
            self.db.commit()

            self.status = 0
            self.session_id = None
   
                    
